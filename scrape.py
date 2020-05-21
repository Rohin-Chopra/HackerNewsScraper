import requests
from bs4 import BeautifulSoup
import pprint

response = requests.get('https://news.ycombinator.com/news')
response2 = requests.get('https://news.ycombinator.com/news?p=2')

soup =  BeautifulSoup(response.text, 'html.parser')
links = soup.select('.storylink')
subtext = soup.select('.subtext')

soup2 =  BeautifulSoup(response2.text, 'html.parser')
links2 = soup2.select('.storylink')
subtext2 = soup2.select('.subtext')

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


page1 = create_cus_hn(links, subtext)
page2 = create_cus_hn(links2, subtext2)

def response_creator(num_pages):
    response_arr = []
    response_arr.append(requests.get('https://news.ycombinator.com/news'))
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
    another_arr = []
    for item in arr:
        another_arr.append(create_cus_hn(item['links'], item['subtext']))
    super_arr = another_arr[0] + another_arr[1]  +  another_arr[2]  +  another_arr[3]  +  another_arr[4]
    super_arr = sort_stories_by_votes(super_arr)     
    pprint.pprint(super_arr)   
print(response_creator(5))



