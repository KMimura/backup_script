from __future__ import print_function
import pickle
import os.path
import datetime
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
# バックアップを補完する世代数
GENERATIONS = 3
# バックアップデータのディレクトリ
DATA_DIR = '/home/minecraft/server/newworld'

def main():
    # 認証情報の取得
    creds = get_creds()
    # サービスの作成
    service = build('drive', 'v3', credentials=creds)
    # 既にアップロードされているファイルの確認
    existing_files = get_existing_files(service)
    if len(existing_files) >= GENERATIONS:
        #必要以上保管されていれば、古いものを削除する
        delete_unnecessary_files(service,existing_files)
    # アップロードするファイルをzipに固める
    file_to_upload = create_zip_file()
    # ファイルをアップロードする
    upload_file(service)

def get_creds():
    creds = None
    # 認証ファイルを開いてみる
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # 失敗したら、新しく作る
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_existing_files(service):
    # Call the Drive v3 API
    results = service.files().list(fields="nextPageToken, files(id, name, createdTime)", q="'1fPMSAy2HszkLaG6IYFhqqs6y8dMvLkZ3' in parents").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
        return {}
    else:
        return items

def delete_unnecessary_files(service,existing_files):
    # 各ファイルの作成時間を取得し、datetimeオブジェクトに変換
    for f in existing_files:
        f['datetime_createdTime'] = datetime.datetime.strptime(f['createdTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
    sorted_files = sorted(existing_files, key=lambda x: x['datetime_createdTime'])          
    delete_len = len(sorted_files) - (GENERATIONS - 1)
    for i in range(delete_len):
        service.files().delete(fileId=sorted_files[i]['id']).execute()

def create_zip_file():
    pass

def upload_file(service):
    pass

if __name__ == '__main__':
    main()
