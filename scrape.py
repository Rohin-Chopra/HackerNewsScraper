import requests
from bs4 import BeautifulSoup
import pprint
import sys

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key = lambda k: k['votes'], reverse=True)

def create_cus_hn(links, subtext):
    hn = []
    for i, item in enumerate(links):
        title = links[i].getText()
        href = links[i].get('href',None)
        vote = subtext[i].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace('points', ''))
            if points > 100:
                hn.append({'title':title, 'href':href, 'votes':points})
    return sort_stories_by_votes(hn)



def response_creator(num_pages):
    response_arr = [] 
    response_arr.append(requests.get('https://news.ycombinator.com/news'))
    if num_pages < 1:
        print('Number of pages has to be greater than 1.')
    elif num_pages == 1:
        soup_creator(response_arr)
    elif num_pages > 1:
        for i in range(2, num_pages + 1):
            responses = requests.get('https://news.ycombinator.com/news?p='+str(i))
            response_arr.append(responses)
        soup_creator(response_arr)
  

def soup_creator(response_arr):
    huge_arr = []
    huge2_arr = []
    for index, item in enumerate(response_arr):
        dump = BeautifulSoup(item.text, 'html.parser')
        huge2_arr.append({ 'soup' : dump,'links': dump.select('.storylink'), 'subtext':  dump.select('.subtext')})

    multiple_create_cus_hn(huge2_arr)    

def multiple_create_cus_hn(arr):
    cus_hn_arr = []
    super_cus_hn_arr = []
    for item in arr:
        cus_hn_arr.append(create_cus_hn(item['links'], item['subtext']))
    for i in range(len(cus_hn_arr)):
        super_cus_hn_arr += cus_hn_arr[i]
    super_cus_hn_arr = sort_stories_by_votes(super_cus_hn_arr)
    pprint.pprint(super_cus_hn_arr)


def main():
    num_pages = sys.argv[1]
    response_creator(int(num_pages))

main()


