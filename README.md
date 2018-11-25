
# GCF Contact Form

_Stop paying $10 per month for a contact form._

Writes to a sqlite database stored in Google Cloud Storage, hosted on Google Cloud Functions, for ~$0 per month.

## Deployment

Set the following env vars:

- `JWT_SECRET` - used to verify 
- `GCP_PROJECT`
- `GCS_BUCKET`
- `GCS_PATH_PREFIX`
- `IP_STACK_API_KEY` (optional)

I recommend using [direnv](https://direnv.net/) for these.

This will create and update a sqlite database at `gs://$GCS_BUCKET/$GCS_PATH_PREFIX/contacts.sqlite`.  Also, make sure that `./service-account-key.json` is a GCP service account that has sufficient access (GCS admin, IIRC).  Then, to deploy:

```bash
$ make deploy-jwt
$ make deploy-contact
```

## Accessing Contacts

Example:

```bash
$ gsutil cp gs://${GCS_BUCKET}/${GCS_PATH_PREFIX}/contacts.sqlite /tmp/contacts.sqlite
$ sqlite3 /tmp/contacts.sqlite 'select email_address from contacts;'
```

## TODO

- Add IP stack integration to turn IP into location, etc.
- Update function to pull request/domain and insert it along with contact info
- Add proper CORS handling (see main.py - `def cors_wrap`)

## License

**MIT**

Copyright 2018 Stuart Axelbrooke

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
