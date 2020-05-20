import requests
from bs4 import BeautifulSoup
import pprint

response = requests.get('https://news.ycombinator.com/news')

soup =  BeautifulSoup(response.text, 'html.parser')
links = soup.select('.storylink')
subtext = soup.select('.subtext')

def create_cus_hn(links, subtext):
    hn = []
    for i, item in enumerate(links):
        title = links[i].getText()
        href = links[i].get('href',None)
        vote = subtext[i].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace('points', ''))
            hn.append({'title':title, 'href':href, 'votes':points})
    return hn

def filter_news(hn):
    for spam in hn:
        if spam['votes'] > 100:
            print(spam)

hn = (create_cus_hn(links, subtext))
filter_news(hn)
