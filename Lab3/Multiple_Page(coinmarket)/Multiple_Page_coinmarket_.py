import requests
from bs4 import BeautifulSoup
import csv
import re #для регулярных выражений

def get_html(url):
    response = requests.get(url)
    if response.ok: # 200
        return response.text
    print(response.status_code)


def write_csv(data):
    with open("coin_market_pages.csv", "a", encoding= 'utf-8', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow((data['name'],
                         data['url'],
                         data['price']))

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
        write_csv(data)
def main():
    file = open("coin_market_pages.csv", "w", encoding= 'utf-8', newline = '')
    writer = csv.writer(file)
    writer.writerow(('Имя',
                     'Ссылка',
                     'Цена'))
    file.close()
    url = 'https://coinmarketcap.com/'
    #get_page_data(get_html(url))

    tmp = 0
    while True:
        html = get_html(url)
        get_page_data(html)
        soup = BeautifulSoup(html, 'lxml')
        try:
            pattern = 'Next' #pattern for regular expression(Button Next)
            url = 'https://coinmarketcap.com/' + soup.find('ul',class_ ='pagination').find('a', 
            text=re.compile(pattern)).get('href')
        except:
            break


if __name__ == '__main__':
    main()

