import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def redefine_rate(str):
    #1,470 total ratings
    r = str.split(' ')[0]
    return r.replace(',','')

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    section = soup.find_all('section')[1] #popular plugins
    plugins = section.find_all('article')

    for plug in plugins:
        body = plug.find('h2')
        name = body.text
        url = body.find('a').get('href')
        rating = redefine_rate(plug.find('span', class_ = 'rating-count').find('a').text)

        data = {'name':name, 'url':url, 'reviews':rating} #create dictionary
        write_csv(data)

def write_csv(dictionary):
    with open('plugins.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((dictionary['name'], dictionary['url'], dictionary['reviews']))

def main():
    url = 'https://wordpress.org/plugins/'
    html = get_html(url)
    get_data(html)



if __name__ == '__main__':
    main()