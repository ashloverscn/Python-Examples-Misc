import smtplib

smtpserver = 'smtp.gmail.com'
AUTHREQUIRED = 1 
smtpuser = 'ashloverscn@gmail.com'  
smtppass = 'gckb lspa bjzg xrna'  

RECIPIENTS = 'ash.temp.new@gmail.com'
SENDER = 'ashloverscn@gmail.com'
mssg = "test message"
s = mssg   

server = smtplib.SMTP(smtpserver,587)
server.ehlo()
server.starttls() 
server.ehlo()
server.login(smtpuser,smtppass)
server.set_debuglevel(1)
server.sendmail(SENDER, [RECIPIENTS], s)
server.quit()
