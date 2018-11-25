import requests
from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find('div', id = 'home-welcome').find('h1')
    return h1.text

def main():
    url = 'https://wordpress.org/'

    pageSrc = get_html(url)
    data = get_data(pageSrc)
    print(data)

if __name__ == '__main__':
    main()
