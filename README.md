
# GCF Contact Form

A contact form that writes to a sqlite database hosted on Google Cloud Functions.

## Deployment

Set the following env vars:

- `JWT_SECRET`
- `GCP_PROJECT`
- `GCS_BUCKET`
- `GCS_PATH_PREFIX`
- `IP_STACK_API_KEY` (optional)

This will create a sqlite database at `gs://$GCS_BUCKET/$GCS_PATH_PREFIX/contacts.sqlite`.  Also, make sure that `./service-account-key.json` is a GCP service account that has sufficient access (GCS admin, IIRC).  Then to deploy:

```bash
$ make deploy-jwt
$ make deploy-contact
```

## TODO

- Add IP stack integration to turn IP into location, etc.
- Update function to pull request/domain and insert it along with contact info

## License

**MIT**

Copyright 2018 Stuart Axelbrooke

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.