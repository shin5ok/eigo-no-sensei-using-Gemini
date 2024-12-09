# eigo-no-sensei-using-Gemini
How to deploy

1. Sigin in Google Cloud with gcloud
   ```bash
   gcloud auth login
   gcloud config set project <your PROJECT ID>
   ```

2. Enable services
   ```bash
    gcloud services enable aiplatform.googleapis.com run.googleapis.com
   ```

3. Just type as below to deploy
   ```bash
   make sa iam
   make build-iam
   make deploy
   ```
