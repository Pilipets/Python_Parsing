import requests
from bs4 import BeautifulSoup
import csv

def create_newCSV(name):
    file = open(name,'w',encoding='utf-8',newline='')
    writer = csv.writer(file)
    writer.writerow(('name','since'))
    file.close()


def get_html(url):
    user_agent={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'\
    '537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    r = requests.get(url,headers=user_agent)
    return r.text

def write_csv(name, data):
    with open(name,'a',encoding='utf-8',newline='') as file:
        order = ['author','since']
        writer = csv.DictWriter(file,fieldnames=order)
        writer.writerow(data)

def get_articles(html):
    soup = BeautifulSoup(html,'lxml')
    ts = soup.find('div',class_='testimonial-container').find_all('article')
    return ts #[] or [a,b,c]    

def get_page_data(ts):
    for t in ts:
        try:
            since = t.find('p',class_='traxer-since').text.strip()
        except:
            since = ''
        try:
            author = t.find('p',class_='testimonial-author').text.strip()
        except:
            author = ''
        data = {'author':author,'since':since}
        print(data)
        write_csv('feedbacks.csv', data)
def main():
    create_newCSV('feedbacks.csv')

    page = 1
    while True: 
        url = 'https://catertrax.com/why-catertrax/traxers/page/{}/'.format(page)

        articles = get_articles(get_html(url)) #[] or [1,2,3]
        if articles:
            get_page_data(articles)
            page += 1
        else:
            break

if __name__ == '__main__':
    main()

