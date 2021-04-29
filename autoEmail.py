import email, smtplib, ssl
from email.message import EmailMessage
import datetime


def sendEmail(body, userEmail, senderEmail, password, attachedImage=None, subject):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = senderEmail
    msg['To'] = userEmail
    s = smtplib.SMTP() # put appropriate parameters in SMTP function (removed for security reasons)
    msg.add_attachment(attachedImage)
    s.send_message(msg)
    s.quit()

def getTime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y, %H:%M:%S")