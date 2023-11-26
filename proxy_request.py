import time
import requests

proxies = {
    #'http': 'socks5://ash:ash@192.168.85.221:1080',
    #'https': 'socks5://ash:ash@192.168.85.221:1080'
    'http': 'socks5://aTtK3zBio1zplQyB:xJo9aGmyF6m4nGbb_streaming-1@geo.iproyal.com:32325',
    'https': 'socks5://aTtK3zBio1zplQyB:xJo9aGmyF6m4nGbb_streaming-1@geo.iproyal.com:32325'
}

#url = 'https://ifconfig.me'
url = 'http://ip.42.pl/raw'

#for x in range(6):
while True:
    r = requests.get(url)
    print(f'Status Code Direct: {r.status_code}')
    print(f'Raw Respones Direct: {r.text}')
    r = requests.get(url,  proxies=proxies)
    print(f'Status Code Proxied: {r.status_code}')
    print(f'Raw Respones Proxied: {r.text}')
    time.sleep(1)
