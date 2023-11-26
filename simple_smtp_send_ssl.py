import ssl
import smtplib

smtpserver = 'smtp.gmail.com'
AUTHREQUIRED = 1 
smtpuser = 'ashloverscn@gmail.com'  
smtppass = 'gckb lspa bjzg xrna'  

RECIPIENTS = 'ash.temp.new@gmail.com'
SENDER = 'ashloverscn@gmail.com'
mssg = "test message"
s = mssg

context = ssl.create_default_context()

server = smtplib.SMTP_SSL(smtpserver, 465, context=context )
server.login(smtpuser,smtppass)
server.set_debuglevel(1)
server.sendmail(SENDER, [RECIPIENTS], s)
server.quit()
