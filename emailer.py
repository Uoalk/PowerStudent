#

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
def send_email(user, pwd, recipient, subject, body):#https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = recipient


    msg.attach(MIMEText(body, 'html'))

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(user,pwd)
    mail.sendmail(user, recipient, msg.as_string())
    mail.quit()
