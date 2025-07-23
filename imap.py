import imaplib
import email
from email.header import decode_header
import os

EMAIL = "your_email@gmail.com"
PASSWORD = "your_app_password"  # Use app password if 2FA is enabled
subject_filter = "Invoice"      # 🔍 Replace with your target subject keyword

output_dir = "imap_pdf_by_subject"
os.makedirs(output_dir, exist_ok=True)

imap = imaplib.IMAP4_SSL("imap.gmail.com")
imap.login(EMAIL, PASSWORD)
imap.select("inbox")

status, messages = imap.search(None, 'ALL')
email_ids = messages[0].split()

print(f"Searching {len(email_ids)} emails...")

for email_id in email_ids:
    res, msg_data = imap.fetch(email_id, "(RFC822)")
    for part in msg_data:
        if isinstance(part, tuple):
            msg = email.message_from_bytes(part[1])
            subject, encoding = decode_header(msg.get("Subject"))[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")
            if subject_filter.lower() in subject.lower():
                print("Matched Subject:", subject)
                if msg.is_multipart():
                    for subpart in msg.walk():
                        content_disposition = str(subpart.get("Content-Disposition"))
                        if "attachment" in content_disposition:
                            filename = subpart.get_filename()
                            if filename and filename.lower().endswith(".pdf"):
                                filename = decode_header(filename)[0][0]
                                if isinstance(filename, bytes):
                                    filename = filename.decode()
                                filepath = os.path.join(output_dir, filename)
                                with open(filepath, "wb") as f:
                                    f.write(subpart.get_payload(decode=True))
                                print("Downloaded:", filepath)

imap.logout()
