import ssl
import smtplib
import socks

#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr=socks_active['ip'], port=socks_active['port'],username=socks_active['username'],password=socks_active['password'])

# Fails to connect to Gmail through Rotating Proxy with error: socks.SOCKS5Error: 0x02: Connection not allowed by ruleset #
#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr='geo.iproyal.com' , port=32325 , rdns=True, username='aTtK3zBio1zplQyB' ,password='xJo9aGmyF6m4nGbb_streaming-1' )

# Local proxy with Every Proxy on Google Play Store #
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, addr='192.168.85.221' , port=1080 ,rdns=True, username='ash' ,password='ash')  

socks.wrapmodule(smtplib)

smtpserver = 'smtp.gmail.com'
AUTHREQUIRED = 1 
smtpuser = 'ashloverscn@gmail.com'  
smtppass = 'gckb lspa bjzg xrna'  

RECIPIENTS = 'ash.temp.new@gmail.com'
SENDER = 'ashloverscn@gmail.com'
mssg = "test message"
s = mssg   

server = smtplib.SMTP(smtpserver, 587 )
server.ehlo()
server.starttls() 
server.ehlo()
server.login(smtpuser,smtppass)
server.set_debuglevel(1)
server.sendmail(SENDER, [RECIPIENTS], s)
server.quit()
