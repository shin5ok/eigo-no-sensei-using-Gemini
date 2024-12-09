# Gemini による英語の先生アプリ

## デプロイ方法

1. Google Cloud に環境設定
   gcloud への権限付与
   ```bash
   gcloud auth login
   ```
   プロジェクトID の設定
   ```bash
   gcloud config set project <your PROJECT ID>
   ```

2. 必要なサービスを有効化
   ```bash
    gcloud services enable aiplatform.googleapis.com run.googleapis.com
   ```

3. デプロイ前の準備
   Cloud Run が利用するサービスアカウントの作成と、権限付与
   ```bash
   make sa iam
   ```

   Cloud Build が利用するサービスアカウントへの権限付与
   ```bash
   make build-iam
   ```

4. Cloud Run へのデプロイ
   名前を指定（ここでは chat という Cloud Run サービスとする）
   ```bash
   export NAME=chat
   ```

   デプロイ
   ```bash
   make deploy
   ```


5. 完了後、割り当てられたURLにアクセスして動作確認します
