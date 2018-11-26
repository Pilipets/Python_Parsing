import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    response = requests.get(url)
    if response.ok: # 200
        return response.text
    print(response.status_code)

def write_csv(data):
    file = open("olx_catalog.csv", "a", encoding='UTF-8', newline = '')
    writer = csv.writer(file)
    writer.writerow((data['name'],
                     data['url'],
                     data['price']))
    file.close()

def process_Price(price):
    price = price.replace('грн.','')
    return price.replace(' ','')

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', class_ = 'fixed offers breakword redesigned').find_all('tr', {'class':'wrap'})

    for tr in trs:
        object_top = tr.find('td', valign = 'top')
        try:
            name = object_top.find('strong').text.strip() #очистка от пробелов,\n,\t перед и после строки
        except:
            name = ''
        try:
            url = object_top.find('a').get('href')
        except:
            url = ''
        
        try:
            tmp_price = tr.find('p', class_ = 'price').find('strong').text
        except:
            tmp_price = ''
        price = process_Price(tmp_price)
        data = {'name': name,
                'url': url,
                'price': price}
        print(name)
        write_csv(data)

def main():

    pattern = 'https://www.olx.ua/uk/list/q-invicta/?page={}'

    for i in range(1,6):
        url = pattern.format(str(i))
        #print(url)
        html = get_html(url)
        get_page_data(html)

if __name__ == '__main__':
    main()