from email.mime.text import MIMEText
import smtplib 
from threading import Timer
from datetime import datetime

email = "mhcapstone22@outlook.com"
password = "Project22$"
envelope = MIMEText('test email')
envelope['Subject']  = 'test email'
envelope['From'] = email
envelope['To'] = 'mhcapstone22@outlook.com'
server = smtplib.SMTP(host="smtp.office365.com", port=587)
server.starttls()
server.login(email, password)
server.sendmail(email, email, envelope.as_string())
server.quit()