import requests
from bs4 import BeautifulSoup
from random import choice

def get_html(url):
    #proxies = {'https':'ipaddress:5000'}
    p = get_proxy('https://free-proxy-list.net/') #{'schema':'','adress':''}
    proxy = {p['schema']:p['adress']}
    r = requests.get(url,proxies = proxy,timeout = 5)
    return r.text

def get_proxy(url):
    html = requests.get(url).text
    
    soup = BeautifulSoup(html,'lxml')
    table = soup.find('table',id='proxylisttable')
    trs = table.find('tbody').find_all('tr')

    proxies =[]
    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip() 
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        proxy={'schema':schema,'adress':ip+':'+port}
        proxies.append(proxy)
    return choice(proxies)

def main():
    url = 'https://free-proxy-list.net/'
    print(get_proxy(url))

if __name__ == '__main__':
    main()

