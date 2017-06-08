"""
Mr. Huffam and his newspaper.

This is the discription.
"""
from bs4 import BeautifulSoup
import requests
import time
import os
import logging


def get_news():
    """Get the url of the latest news."""
    news_url = os.environ.get('BLOG_URL')
    news_headers = {'user-agent': os.environ.get('USER-AGENT')}

    news_page = BeautifulSoup(
        requests.get(news_url, headers=news_headers).content, 'html.parser')

    list_news = news_page.find('div', 'container blog-index')
    latest_news = list_news.article

    link = latest_news.a['href']
    title = latest_news.a.string
    content = latest_news.find('div', 'entry').p.string

    return link, title, content


def get_cover(link):
    """Get the cover image of the news."""
    headers = {'user-agent': os.environ.get('USER-AGENT')}
    page = BeautifulSoup(requests.get(link, headers=headers).content,
                         'html.parser')

    news_content = page.find('div', 'entry')
    cover = news_content.img['src']
    return cover


def mr_huffam(link, title, content, old_link):
    """Run Main function."""
    headers = {'Content-Type': 'application/json'}
    if old_link != link:
        cover = get_cover(link)
        news = {'content': 'The breaking news is in print now; come and read,\
         delicious friends. \n \n' '**'+title+'**',
                'embeds': [
                    {'title': title, 'description': content, 'url': link,
                     'image': {'url': cover}}
                        ]
                }
        r = requests.post(os.environ.get('HUFFAM'), headers=headers, json=news)
        return True
    return False


if __name__ == "__main__":
    # link, title, content = get_news()
    # old_link = link
    old_link = ''
    while True:
        link, title, content = get_news()
        have_news = mr_huffam(link, title, content, old_link)
        if have_news:
            logging.warning('previous news: %s' % old_link)
            logging.warning('latest news: %s' % link)
            old_link = link
        print('Mr. Huffam is working hard')
        time.sleep(60*20)
