# Gemini による英語の先生アプリ

## デプロイ方法

1. このリポジトリを clone します
   ```bash
   cd
   git clone https://github.com/kawanos/eigo-no-sensei-using-Gemini.git
   ```

2. Google Cloud に環境設定
   gcloud への権限付与
   ```bash
   gcloud auth login
   ```
   プロジェクトID の設定
   ```bash
   gcloud config set project <your PROJECT ID>
   ```
   環境変数にも設定
   ```bash
   export PROJECT_ID=<your PROJECT ID>
   ```

4. 必要なサービスを有効化
   ```bash
    gcloud services enable aiplatform.googleapis.com run.googleapis.com
   ```

5. デプロイ前の準備
   Cloud Run が利用するサービスアカウントの作成
   ```bash
   make sa
   ```
   サービスアカウントへの権限付与
   ```bash
   make iam
   ```

   Cloud Build が利用するサービスアカウントへの権限付与
   ```bash
   make build-iam
   ```

7. Cloud Run へのデプロイ
   名前を指定（ここでは chatapp という Cloud Run サービスとする）
   ```bash
   export RUN_NAME=chatapp
   ```

   デプロイ
   ```bash
   make deploy
   ```


8. 完了後、割り当てられたURLにアクセスして動作確認します
