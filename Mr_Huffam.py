from bs4 import BeautifulSoup
import requests
import time
import os
import logging

def Get_News():
    news_url = os.environ.get('BLOG_URL')
    news_headers = {'user-agent': os.environ.get('USER-AGENT')}

    news_page = BeautifulSoup(requests.get(news_url, headers=news_headers).content, 'html.parser')

    list_news = news_page.find('div', 'container blog-index')
    latest_news = list_news.article

    link = latest_news.a['href']
    title = latest_news.a.string
    content = latest_news.find('div', 'entry').p.string

    return link, title, content

def Get_Cover(link):
    headers = {'user-agent': os.environ.get('USER-AGENT')}
    page = BeautifulSoup(requests.get(link, headers=headers).content, 'html.parser')

    news_content = page.find('div', 'entry')
    cover = news_content.a['href']
    return cover


def Mr_Huffam(link, title, content, old_link):
    headers = {'Content-Type': 'application/json'}
    if old_link != link:
        cover = Get_Cover(link)
        news = {'content': 'The breaking news is in print now; come and read, delicious friends. @here \n \n' '**'+title+'**',
                'embeds':[
                    {'title':title, 'description':content, 'url':link, 'image':{'url':cover}}
                        ]
                }
        r = requests.post(os.environ.get('HUFFAM'), headers=headers, json=news)
        return True
    return False

if __name__ == "__main__":
    old_link = os.environ.get('PREVIOUS_NEWS_LINK')
    while True:
        link, title, content = Get_News()
        have_news = Mr_Huffam(link, title, content, old_link)
        if have_news:
            logging.warning('previous news: %s' %old_link)
            logging.warning('latest news: %s' %link)
            old_link = link
            os.environ['PREVIOUS_NEWS_LINK'] = old_link
        logging.warning('Mr. Huffam is working hard')
        time.sleep(60*20)
