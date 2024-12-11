
BUCKET_NAME?=$(PROJECT_ID)
PROJECT_ID?=$(GOOGLE_CLOUD_PROJECT)

NAME := eigo-teacher
RUN_NAME ?= $(NAME)


.PHONY: deploy
deploy:
	gcloud run deploy $(NAME) \
	--source=. \
	--region=asia-northeast1 \
	--cpu=1 \
	--memory=1G \
	--ingress=all \
	--set-env-vars=PROJECT_ID=$(PROJECT_ID) \
	--min-instances=1 \
	--service-account=$(NAME)@$(PROJECT_ID).iam.gserviceaccount.com \
	--cpu-boost \
	--session-affinity \
	--allow-unauthenticated

.PHONY: sa
sa:
	gcloud iam service-accounts create $(NAME)

.PHONY: iam
iam:
	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(NAME)@$(PROJECT_ID).iam.gserviceaccount.com \
	--role=roles/aiplatform.user

	gcloud projects add-iam-policy-binding $(PROJECT_ID) \
	--member=serviceAccount:$(NAME)@$(PROJECT_ID).iam.gserviceaccount.com \
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
