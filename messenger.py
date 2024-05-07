import imaplib
import email
import re
import yaml
import smtplib
import booker
from users import in_database, add_user, update_password
from email.header import decode_header
from email.message import EmailMessage


with open('config.yaml', 'r') as file:
    booking_account = yaml.safe_load(file)
    

def get_body(msg):
    if msg.is_multipart(): # handling multipart emails
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload()
    else:
        return msg.get_payload()

def check_email():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(booking_account['username'], booking_account['password'])
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
                    booker.book(username, password, requests)
                else:
                    send_email(username, 'Error as Occured', 
                               '''
                               You are not in our database, send an email with your credentials
                               with 'User' in the subject.
                               ''')
                    pass

            elif 'User' in subject:
                # getting username and password
                credentials = get_body(msg)
                credentials = credentials.split()

                if not in_database(credentials[0],credentials[1]): # adding/updating given the user credentials
                    add_user(credentials[0],credentials[1])
                else:
                    update_password(credentials[0],credentials[1])


def send_email(reciever, subject, message):
    # construct email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = booking_account['username']
    msg['To'] = reciever
    msg.set_content(message)

    # send the amil
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(booking_account['username'], booking_account['password'])
        smtp.send_message(msg)