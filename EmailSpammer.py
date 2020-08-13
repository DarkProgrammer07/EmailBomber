import smtplib
import argparse

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

class EmailSpammer:
    def __init__(self, smtpHost:str, smtpPort:int, email:str, _pass:str):
        self.email, self._pass = email, _pass

        self.server = smtplib.SMTP(smtpHost, smtpPort)

        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()

    def attack(self, iteration:int, authorFromName:str, targetEmail:str, spamSubject:str, spamBody:bytes, spamImage:str=None):
        self.server.login(self.email, self._pass)

        self.msg = MIMEMultipart()

        self.msg['From'] = authorFromName
        self.msg['To'] = targetEmail
        self.msg['Subject'] = spamSubject
        
        self.msg.attach(MIMEText(spamBody.decode('ascii')))

        if spamImage is not None:
            self.p = MIMEBase('application', 'octet-stream')
            self.p.set_payload(open(spamImage, 'rb').read())

            encoders.encode_base64(self.p)
            
            self.p.add_header('Content-Disposition', f'attachment; filename={spamImage}')

            self.msg.attach(self.p)

        for _ in range(iteration):
            self.server.sendmail(self.email, targetEmail, self.msg.as_string())

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-sh', '--host', dest='host', required=True, help='smtp server host')
    parser.add_argument('-sp', '--port', dest='port', type=int, required=True, help='smtp server port')
    parser.add_argument('-e', '--email', dest='email', required=True, help='attacker\'s email')
    parser.add_argument('-pwd', '--pass', dest='_pass', required=True, help='attacker\'s password')

    parser.add_argument('-i', '--iteration', dest='iteration', type=int, required=True, help='number of emails to be sent')
    parser.add_argument('-f', '--from', dest='_from', required=True, help='name to be displayed on the email header')
    parser.add_argument('-t', '--to', dest='to', required=True, help='the receiver\'s email')
    parser.add_argument('-s', '--subject', dest='subject', required=True, help='subject to be displayed on the email header')
    parser.add_argument('-b', '--body', dest='body', required=True, help='the text to be displayed on the email body')
    parser.add_argument('-img', '-image', dest='image', required=False, help='an optional image attachment')

    args = parser.parse_args()

    spammer = EmailSpammer(args.host, args.port, args.email, args._pass)
    spammer.attack(args.iteration, args._from, args.to, args.subject, bytes(args.body, 'utf-8'), args.image)