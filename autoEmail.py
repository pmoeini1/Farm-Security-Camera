import email, smtplib, ssl


def sendSimpleEmail(body, userEmail, senderEmail, password):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com" # SMTP server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(senderEmail, password) # login to email
        server.sendmail(senderEmail, userEmail, body) # send alert email

