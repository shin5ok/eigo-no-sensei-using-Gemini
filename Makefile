
BUCKET_NAME?=$(PROJECT_ID)


.PHONY: deploy
deploy:
	gcloud run deploy eigo-teacher \
	--source=. \
	--region=asia-northeast1 \
	--cpu=1 \
	--memory=512M \
	--ingress=internal-and-cloud-load-balancing \
	--set-env-vars=PROJECT_ID=${PROJECT_ID} \
	--min-instances=1 \
	--service-account=eigo-teacher@$(PROJECT_ID).iam.gserviceaccount.com \
	--allow-unauthenticated

.PHONY: sa
sa:
	gcloud iam service-accounts create eigo-teacher

.PHONY: iam
iam:
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:eigo-teacher@$(PROJECT_ID).iam.gserviceaccount.com \
	--role=roles/aiplatform.user

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:eigo-teacher@$(PROJECT_ID).iam.gserviceaccount.com \
	--role=roles/storage.objectUser

