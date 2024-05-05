import imaplib
import email
import re
from booker import book_room
from users import in_database, add_user, update_password
from email.header import decode_header
    
def get_body(msg):
    if msg.is_multipart(): # handling multipart emails
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
    
    for num in messages[0].split(): # looping through all unseen messages
        status, data = mail.fetch(num, '(RFC822)')
        if status == 'OK':
            msg = email.message_from_bytes(data[0][1])
            subject = decode_header(msg["subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            if 'Book Room' in subject:  
                # getting user email
                username = re.search(r'\<([^>]*)\>',msg['From']) 
                username = username.group(1)

                # getting requests stored in body
                requests = get_body(msg)
                requests = re.split(r'\r\n|\n|\r',requests)

                # getting password 
                password = requests[0]
                del requests[0]

                if in_database(username, password): # ensuring the user is in the database
                    book_room(email,password,requests)
                else:
                    # send email with error
                    pass

            elif 'User' in subject:
                # getting username and password
                credentials = get_body(msg)
                credentials = credentials.split()

                if not in_database(credentials[0],credentials[1]): # adding/updating given the user credentials
                    add_user(credentials[0],credentials[1])
                else:
                    update_password(credentials[0],credentials[1])

