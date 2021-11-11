import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import regex as re
from bs4 import BeautifulSoup
import datetime
import pandas as pd 

# account credentials
username = ""
password = ""

imap = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)

status, messages = imap.select("INBOX")

# total number of emails
messages = int(messages[0])


subjects, froms, qtys, times, ies = [], [], [], [], []
for i in range(messages, 0, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            print("Subject:", subject)
            print("From:", From)
            # if the email message is multipart
            if msg.is_multipart():
                # iterate over email parts
                for part in msg.walk():
                    # extract content type of email
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    try:
                        # get the email body
                        body = part.get_payload(decode=True).decode()
                        
                    except:
                        pass
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # print text/plain emails and skip attachments
                        with open(str(i)+'.txt', 'w', encoding='utf-8') as f:
                            f.write(body)

            else:
                # extract content type of email
                content_type = msg.get_content_type()
                # get the email body
                body = msg.get_payload(decode=True).decode()
                if content_type == "text/plain":
                    with open(str(i)+'.txt', 'w', encoding='utf-8') as f:
                            f.write(body)

            soup = BeautifulSoup(body, "html.parser")
            qty = re.search(r'\d+', soup.text)
            
            if qty:
                print('Qty: '+ qty.group())
                qty = qty.group()
            else:
                print('No match')
            time = datetime.datetime.now()
            print('Time: '+ str(time))

            number = str(i)

            subjects.append(subject)
            froms.append(From)
            qtys.append(qty)
            times.append(time)
            ies.append(str(i))

df = pd.DataFrame(list(zip(subjects, froms, qtys, times, ies)), columns=['subjects', 'froms', 'qtys', 'times', 'ies'])

df.to_excel('data_retrieved_and_parsed.xlsx', index=False)


# close the connection and logout
imap.close()
imap.logout()