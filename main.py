
import sqlite3
from typing import Optional, NamedTuple
import os
from google.cloud import storage
import jwt
from flask import abort
import time

storage_client = storage.Client.from_service_account_json("service-account-key.json")

IP_STACK_API_KEY = os.getenv("IP_STACK_API_KEY")
JWT_SECRET = os.environ["JWT_SECRET"]

CONTACT_FIELD_NAMES = "email_address, name, phone_number, job_title, ip_address, continent, " "country, country_code, region_name, city, submission_token"
CONTACT_PLACEHOLDERS = "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"

Contact = NamedTuple(
    "Contact",
    [
        ("email_address", str),
        ("name", Optional[str]),
        ("phone_number", Optional[str]),
        ("job_title", Optional[str]),
        ("ip_address", Optional[str]),
        ("continent", Optional[str]),
        ("country", Optional[str]),
        ("country_code", Optional[str]),
        ("region_name", Optional[str]),
        ("city", Optional[str]),
        ("submission_token", Optional[str]),
    ],
)


def create_database() -> sqlite3.Connection:
    conn = sqlite3.connect("contacts.sqlite")
    conn.execute(
        """
        create table contacts (
            contact_id integer primary key,
            email_address text not null,
            name text,
            phone_number text,
            job_title text,
            ip_address text,
            continent text,
            country text,
            country_code text,
            region_name text,
            city text,
            created_at text not null,
            submission_token text not null
        );
    """
    )
    conn.commit()
    return conn


def fetch_database() -> Optional[sqlite3.Connection]:
    """ Attempts to fetch the database, returns None if not found """
    blob = storage_client.get_bucket(os.environ["GCS_BUCKET"]).get_blob(
        os.environ["GCS_PATH_PREFIX"] + "/contacts.sqlite"
    )
    if blob is None:
        return None

    blob.download_to_filename("/tmp/contacts.sqlite")
    return sqlite3.connect("/tmp/contacts.sqlite")


def fetch_or_create_database() -> sqlite3.Connection:
    conn = fetch_database()
    if conn is not None:
        return conn

    print("No database found, creating one now.")
    return create_database()


def upload_database():
    with open("/tmp/contacts.sqlite", "rb") as db_file:
        return (
            storage_client.get_bucket(os.environ["GCS_BUCKET"])
            .blob(os.environ["GCS_PATH_PREFIX"] + "/contacts.sqlite")
            .upload_from_file(db_file)
        )


def get_jwt(request) -> str:
    auth_string = request.headers.get("Authorization")
    if auth_string is None:
        return None
    auth_type, token = auth_string.split(" ", 1)
    if auth_type != "Bearer":
        raise ValueError("Only Bearer authorization valid")
    decoded = jwt.decode(token, JWT_SECRET)
    if "ip_address" not in decoded:
        raise ValueError("Malformed authorization token")
    if decoded["ip_address"] != get_ip(request):
        raise ValueError("Requestor doesn't match provided token")
    return token


def get_ip(request):
    headers_list = request.headers.getlist("X-Forwarded-For")
    return headers_list[0] if headers_list else request.remote_addr


def parse_contact(request) -> Contact:
    """ Parse a contact from the request """
    jwt = get_jwt(request)

    result = request.get_json()
    result["ip_address"] = get_ip(request)
    result["submission_token"] = jwt

    if IP_STACK_API_KEY:
        pass

    for key in dir(Contact):
        if key == "index" or key == "count" or key.startswith("_"):
            continue
        if key not in result:
            result[key] = None

    return Contact(**result)


def save_contact(contact: Contact):
    conn = fetch_or_create_database()
    conn.execute(
        f"insert into contacts ({CONTACT_FIELD_NAMES}, created_at) values ({CONTACT_PLACEHOLDERS}, datetime('now'));",
        contact,
    )
    conn.commit()
    upload_database()


def issue_jwt(request):
    return (
        '{"jwt": "'
        + jwt.encode({"ip_address": get_ip(request), "iat": time.time()}, JWT_SECRET).decode()
        + '"}'
    )


def contact_form_put(request):
    """ Accept contact PUT request """
    try:
        save_contact(parse_contact(request))
    except jwt.InvalidSignatureError:
        abort(403)
    except ValueError as e:
        print(e)
        abort(400)
    return '{"status": "ok"}'
