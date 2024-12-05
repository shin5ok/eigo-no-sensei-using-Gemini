
BUCKET_NAME?=$(PROJECT_ID)


.PHONY: deploy
deploy:
	gcloud run deploy eigo-teacher \
	--source=. \
	--region=asia-northeast1 \
	--cpu=1 \
	--memory=1G \
	--ingress=internal-and-cloud-load-balancing \
	--set-env-vars=PROJECT_ID=${PROJECT_ID} \
	--min-instances=1 \
	--service-account=eigo-teacher@$(PROJECT_ID).iam.gserviceaccount.com \
	--cpu-boost \
	--session-affinity \
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

.PHONY: build-iam
CLOUDBUILD_SA:=$(shell gcloud builds get-default-service-account | grep gserviceaccount | cut -d / -f 4)
build-iam:

	@echo "Grant some authorizations to the service account for Cloud Build"

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(CLOUDBUILD_SA) \
	--role=roles/artifactregistry.repoAdmin

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(CLOUDBUILD_SA) \
	--role=roles/cloudbuild.builds.builder

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(CLOUDBUILD_SA) \
	--role=roles/run.admin

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(CLOUDBUILD_SA) \
	--role=roles/storage.admin
