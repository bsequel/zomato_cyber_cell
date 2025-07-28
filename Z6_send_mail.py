import smtplib
from email.message import EmailMessage

def send_email(subject, body, sender_email, receiver_email, password):
    """
    Sends an email using Gmail's SMTP server.

    Parameters:
    - subject (str): Subject of the email.
    - body (str): Body content of the email.
    - sender_email (str): Sender's email address.
    - receiver_email (str or list): Receiver's email address(es).
    - password (str): App password or email password.
    """
    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email if isinstance(receiver_email, str) else ', '.join(receiver_email)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


