import imaplib
import email
from bs4 import BeautifulSoup
from users import in_database, add_user, update_password
from email.header import decode_header
    
def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload()
    else:
        return msg.get_payload()

def check_email(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select('inbox')
    status, messages = mail.search(None, '(UNSEEN)')

    if status != 'OK': # no booking requests
        return
    
    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        if status == 'OK':
            msg = email.message_from_bytes(data[0][1])
            subject = decode_header(msg["subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            if 'Book Room' in subject:  
                pass
            elif 'User' in subject:
                credentials = get_body(msg)
                credentials = credentials.split()
                if not in_database(credentials[0], credentials[1]):
                    add_user(credentials[0], credentials[1])
                else:
                    update_password(credentials[0], credentials[1])

