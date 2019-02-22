
const ENDPOINT_URL = 'https://us-central1-axelbrooke-com.cloudfunctions.net/';

const jwtPromise = fetch(ENDPOINT_URL + 'contact_form_jwt');

const submitForm = (evt) => {
    const formData = {
        'email_address': 'foo@bar.com',
    }

    return jwtPromise
        .then(resp => resp.json())
        .then(data => 
            fetch(ENDPOINT_URL + 'contact_form_put', {
                method: "POST",
                mode: "cors",
                headers: {"Content-Type": "application/json", "Authorization": "Bearer " + data.jwt},
                body: JSON.stringify(formData),
            })
        )
};

submitForm(null).then(resp => resp.json()).then(console.log);
