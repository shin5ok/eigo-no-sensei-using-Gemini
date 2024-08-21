import os
  
PROJECT_ID = os.environ.get("PROJECT_ID")

BUCKET_NAME = os.environ.get("BUCKET_NAME", PROJECT_ID)
LOCATION = os.environ.get("LOCATION", "us-central1")
