import imaplib
import email
import os
from email.mime.multipart import MIMEMultipart


import os
from pathlib import Path
from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

GMAIL_APP_PASSSWORD = os.getenv('App_Password')

# Gmail IMAP settings
GMAIL_HOST = 'imap.gmail.com'
GMAIL_PORT = 993

# Your credentials
EMAIL = r"beginasnoob1996@gmail.com"
APP_PASSWORD = GMAIL_APP_PASSSWORD  # 16-character app password

def fetch_emails():
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL(GMAIL_HOST, GMAIL_PORT)
    mail.login(EMAIL, APP_PASSWORD)
    
    # Select inbox
    mail.select('inbox')
    
    # Search for all emails (or use specific criteria)
    status, messages = mail.search(None, 'ALL')
    # print(messages)
    # Get email IDs
    email_ids = messages[0].split()
    
    # Create downloads folder
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    
    # Fetch last 5 emails
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        # print(msg_data)
        
        # Parse email
        msg = email.message_from_bytes(msg_data[0][1])
        if "Security alert".lower() not in str(msg["Subject"]).lower():
            print("skip")
            continue
        print(f"From: {msg['From']}")
        print(f"Subject: {msg['Subject']}")
        print(f"Date: {msg['Date']}")
        
        # Process attachments
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    # Save attachment
                    filepath = os.path.join('downloads', filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    print(f"Downloaded: {filename}")
        
        print("-" * 50)
    
    # Close connection
    mail.close()
    mail.logout()

if __name__ == "__main__":
    fetch_emails()