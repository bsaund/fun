import io
import os.path
from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.file']

flashcards_filename = 'flashcards.csv'


def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_file = Path.home() / '.gcp_credentials' / 'credentials.json'
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file.absolute().as_posix(), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_flashcards_files_on_drive(service):
    files = service.files().list(q="name = 'Flashcards'",
                                 spaces='drive').execute()
    return files.get('files', [])


def upload_flashcards(service):
    file_metadata = {'name': 'Flashcards', 'mimeType': 'application/vnd.google-apps.spreadsheet'}
    media = MediaFileUpload(flashcards_filename, mimetype='text/csv', resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print(f"Uploaded File id {file.get('id')}")


def sync_from_drive(file, service):
    file_id = file['id']
    request = service.files().export_media(fileId=file_id,
                                           mimeType='text/tab-separated-values')
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print(f"Download: {int(status.progress() * 100)}")
    with open(flashcards_filename, 'wb') as f:
        f.write(fh.getvalue())
        f.write(b'\r\n')



def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    creds = get_creds()
    service = build('drive', 'v3', credentials=creds)
    files = get_flashcards_files_on_drive(service)
    if len(files) > 1:
        raise RuntimeError("Multiple flashcard files found. Not sure what to do.")

    if not files:
        print("No Flashcard files found on drive. Uploading...", end='')
        upload_flashcards(service)
        print("Done")

    else:
        sync_from_drive(files[0], service)

    # # Call the Drive v3 API
    # results = service.files().list(
    #     pageSize=10, fields="nextPageToken, files(id, name)").execute()
    # items = results.get('files', [])
    #
    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))


if __name__ == '__main__':
    main()
