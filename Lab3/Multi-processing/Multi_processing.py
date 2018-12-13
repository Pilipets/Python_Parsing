import requests
import csv
from bs4 import BeautifulSoup
from multiprocessing import Pool

def get_html(url):
    response = requests.get(url)
    return response.text

def write_csv(name, data):
    with open(name,'a',encoding='utf-8',newline='') as file:
        order = ['name','url','price']
        writer = csv.DictWriter(file,fieldnames=order)
        writer.writerow(data)

def create_newCSV(name):
    file = open(name,'w',encoding='utf-8',newline='')
    writer = csv.writer(file)
    writer.writerow(('name','url','price'))
    file.close()

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', id = 'currencies').find('tbody').find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        try:
            name = tds[1].find('a', class_ = 'currency-name-container link-secondary').text.strip() 
            #.strip() remove ' ', '\t', from the start and end
        except:
            name = ''
        try:
            url = 'https://coinmarketcap.com' + tds[1].find('a', class_ = 'currency-name-container link-secondary').get('href')
        except:
            url = ''
        try:
            price = tds[3].find('a').get('data-usd').strip()
        except:
            price = ''
        data = {'name': name,
                'url': url,
                'price': price}
        write_csv('coin_market_pages.csv',data)

def make_all(url):
    text = get_html(url)
    get_page_data(text)

def main():
    create_newCSV('coin_market_pages.csv')

    url = 'https://coinmarketcap.com/%d'

    pagesAmount = 10
    urls = [url % (i) for i in range(1,pagesAmount)]

    with Pool(200) as p:
        p.map(make_all,urls)
    
if __name__ == '__main__':
    main()

