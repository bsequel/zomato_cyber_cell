import imaplib
import email
from email.header import decode_header
import os

def download_attachments(msg, email_id):
    """Download attachments from email message"""
    attachments = []
    
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    # Decode filename if needed
                    if decode_header(filename)[0][1] is not None:
                        filename = decode_header(filename)[0][0].decode()
                    
                    # Create downloads folder
                    os.makedirs('downloads', exist_ok=True)
                    
                    # Save attachment
                    filepath = os.path.join('downloads', f"{email_id}_{filename}")
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    
                    attachments.append(filename)
    
    return attachments

def fetch_emails_imap(username, password, max_emails=10, subject_filter=None):
    """Fetch emails and download attachments using IMAP"""
    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    
    try:
        # Login
        mail.login(username, password)
        
        # Select inbox
        mail.select('inbox')
        
        # Search for emails
        if subject_filter:
            # Search by subject
            status, messages = mail.search(None, f'SUBJECT "{subject_filter}"')
        else:
            # Search for all emails
            status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        
        # Get latest emails
        latest_emails = email_ids[-max_emails:]
        
        for email_id in reversed(latest_emails):  # Reverse to get newest first
            # Fetch email
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            
            # Parse email
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Decode subject
            subject = decode_header(msg['Subject'])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            
            # Get sender
            sender = msg['From']
            
            # Download attachments
            attachments = download_attachments(msg, email_id.decode())
            
            print(f"From: {sender}")
            print(f"Subject: {subject}")
            if attachments:
                print(f"Attachments: {', '.join(attachments)}")
            else:
                print("No attachments")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mail.logout()

if __name__ == "__main__":
    # Replace with your Gmail credentials
    username = "your_email@gmail.com"
    password = "your_app_password"  # Use Gmail App Password
    
    
    fetch_emails_imap(username, password, subject_filter="report")


































# Examples:
    # Fetch all emails
    # fetch_emails_imap(username, password)
    
    # Fetch emails with specific subject
    # fetch_emails_imap(username, password, subject_filter="invoice")
    
    # Fetch emails with subject containing "report"