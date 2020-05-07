
# backup_script

## 概要

サーバーの特定のフォルダをzipで固めて、Google Drive上にアップロードするスクリプトです。
Driveの容量がいっぱいにならないよう、古いファイルは削除するような機能も付けてあります。

## 必要なモジュール

必要なモジュールは、以下のコマンドでインストールします。

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
