#This file contains the a simple function to send emails

#from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


#This function is a super simple way to send a quick email, using the specified arguments. Note: it will currently only work for gmail because of the hardcoded smtp
def send_email(user, pwd, recipient, subject, body):#https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python
    msg = MIMEMultipart('alternative')#set up a mime template
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = recipient


    msg.attach(MIMEText(body, 'html'))#add mime template to body

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)#connect to gmail and send email
    mail.ehlo()
    mail.starttls()
    mail.login(user,pwd)
    mail.sendmail(user, recipient, msg.as_string())
    mail.quit()
