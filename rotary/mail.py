from email.parser import Parser
from email.mime.text import MIMEText
import quopri
import imaplib
import smtplib
import time
import sys

class Mail:

    def __init__(self, sender, reciever, subject, body):
        self.sender = sender
        self.reciever = reciever
        self.subject = subject
        self.body = body

    def to_string(self):
        text = '\r\n'.join([
            'From: %s' % self.sender,
            'To: %s' % self.reciever,
            'Subject: %s' % self.subject,
            '',
            self.body
            ])
        print(text)

        msg = MIMEText(text, 'plain', 'utf-8')
        msg['subject'] = self.subject
        msg['from'] = self.sender
        msg['to'] = self.reciever

        return msg.as_string()


def from_bytes(b):
    msg = Parser().parsestr(b.decode('utf-8'))
    return Mail(
       quopri.decodestring(msg['from']).decode('utf-8'),
       quopri.decodestring(msg['to']).decode('utf-8'),
       quopri.decodestring(msg['subject']).decode('utf-8'),
       msg.get_payload()[0].get_payload(decode=True).decode('utf-8')
        )

class Server:

    def smtp_init(self):
        self.smtp_server = smtplib.SMTP(self.smtp_addr)
        self.smtp_server.ehlo()
        self.smtp_server.starttls()
        self.smtp_server.login(self.user, self.passw)

    def imap_init(self):
        self.imap_server = imaplib.IMAP4_SSL(self.imap_addr)
        self.imap_server.login(self.user, self.passw)

    def send(self, mail):
        try:
           self.smtp_server.sendmail(
                   mail.sender,
                   [mail.reciever],
                   mail.to_string()
                   )
        except:
            print(
                    'Error sending mail: %s' % mail.to_string(),
                    file=sys.stderr
                    )
            self.smtp_init()

    def update(self):
        self.imap_server.select('Inbox')
        typ, recent = self.imap_server.search(None, 'UnSeen')

        if recent[0]:
            for num in recent[0].split():
                typ, data = self.imap_server.fetch(num, '(RFC822)')
                self.mailbox.append(Mail.from_bytes(data[0][1]))
            return True
        else:
            return False

    def __init__(self, u, p, s_a):
        self.user = u
        self.passw = p

        #self.imap_addr = i_a
        self.smtp_addr = s_a

        self.mailbox = []

        #self.imap_init()
        self.smtp_init()
