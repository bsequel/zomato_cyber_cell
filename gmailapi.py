import os
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
subject_filter = "Invoice"  # 🔍 Replace with your subject filter

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def download_pdf_attachments(service, output_dir='gmail_api_pdf_by_subject'):
    os.makedirs(output_dir, exist_ok=True)
    query = f'subject:"{subject_filter}" has:attachment filename:pdf'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    if not messages:
        print("No matching emails found.")
        return

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        parts = msg_data['payload'].get('parts', [])
        for part in parts:
            filename = part.get("filename")
            body = part.get("body", {})
            if filename and filename.lower().endswith('.pdf') and body.get("attachmentId"):
                attachment = service.users().messages().attachments().get(
                    userId='me', messageId=msg['id'], id=body['attachmentId']).execute()
                file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
                filepath = os.path.join(output_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                print(f"Downloaded: {filepath}")

if __name__ == '__main__':
    service = authenticate_gmail()
    download_pdf_attachments(service)
