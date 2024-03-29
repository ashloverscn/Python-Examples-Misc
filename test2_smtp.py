import smtplib

#email.mime.multipart is specific to python3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()
msg['From'] = 'synthia<egrere@icloud.com>'
msg['To'] = 'ash.temp.new@gmail.com'
msg['Subject'] = 'Subject'
message = 'Message body'
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('smtp.mail.me.com', 587)
# identify ourselves
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login('egrere@icloud.com', 'yhjn-hkfb-jhkp-tzts')
mailserver.sendmail('egrere@icloud.com', 'ash.temp.new@gmail.com', msg.as_string())
print(f'email sent succesfully')
