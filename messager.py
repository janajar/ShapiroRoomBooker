import imaplib
import email

from bs4 import BeautifulSoup
from users import check_user, add_user
from email.header import decode_header

    
def check_email(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    print(mail.login(username, password))
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
            if 'User' in subject:
                pass
                
