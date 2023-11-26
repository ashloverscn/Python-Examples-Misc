import time
import socket
import socks
import requests

socks.setdefaultproxy(socks.SOCKS5, 'geo.iproyal.com', 32325, True, 'aTtK3zBio1zplQyB', 'xJo9aGmyF6m4nGbb_streaming-1')
socket.socket = socks.socksocket
#url = 'https://ifconfig.me'
url = 'http://ip.42.pl/raw'

#for x in range(6):
while True:
    r = requests.get(url)    
    print(f'Status Code Proxied: {r.status_code}')
    print(f'Raw Respones Proxied: {r.text}')
    time.sleep(1)
