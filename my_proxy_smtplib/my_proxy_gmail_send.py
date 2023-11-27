from my_proxy_smtplib import ProxySMTP

email_server = ProxySMTP('smtp.gmail.com', 587, proxy_addr='192.168.85.221', proxy_port=1080)

email_server.starttls()
email_server.login('ashloverscn@gmail.com', 'gckb lspa bjzg xrna')
email_server.sendmail('ashloverscn@gmail.com', 'ash.temp.new@gmail.com', "test message")
email_server.quit()
