
.PHONY: deploy-contact deploy-jwt test fmt


deploy-jwt:
	gcloud functions deploy contact_form_jwt --entry-point=contact_form_jwt --runtime=python37 --trigger-http --memory=128MB --set-env-vars JWT_SECRET=$$JWT_SECRET --project=$(GCP_PROJECT)


deploy-contact:
	gcloud functions deploy contact_form_put --entry-point=contact_form_put --runtime=python37 --trigger-http --memory=128MB --set-env-vars JWT_SECRET=$$JWT_SECRET,GCS_BUCKET=$(GCS_BUCKET),GCS_PATH_PREFIX=$(GCS_PATH_PREFIX),IP_STACK_API_KEY=$$IP_STACK_API_KEY,MAILGUN_API_KEY=$$MAILGUN_API_KEY,MAILGUN_DOMAIN=$$MAILGUN_DOMAIN,MAIL_FROM=$$MAIL_FROM,MAIL_TO=$$MAIL_TO,MAILGUN_SMTP_USER=$$MAILGUN_SMTP_USER,MAILGUN_SMTP_PASSWORD=$$MAILGUN_SMTP_PASSWORD --project=$(GCP_PROJECT)


fmt:
	black -l 100 main.py
