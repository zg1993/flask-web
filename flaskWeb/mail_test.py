from email.mime.text import MIMEText
import os

msg =MIMEText('hello, send by python', 'plain', 'utf-8')

# from_addr = os.environ.get('MAIL_USERNAME')
password = os.environ.get('PASS')
from_addr = 'zhougang@kiyozawa.com'

smtp_server = 'smtp.kiyozawa.com'
print(os.environ.get('PASS'))
#print(os.environ.__dict__)
import smtplib
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [from_addr], msg.as_string())
server.quit()


