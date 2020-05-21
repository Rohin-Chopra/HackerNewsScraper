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
    print(response_arr)
    huge_arr = []
    huge2_arr = []
    for index, item in enumerate(response_arr):
        huge_arr.append({'soup':BeautifulSoup(item.text, 'html.parser') })
        huge2_arr.append({ 'soup' : huge_arr[index]['soup'],'links': huge_arr[index]['soup'].select('.storylink'), 'subtext':  huge_arr[index]['soup'].select('.storylink')})
    pprint.pprint(huge2_arr)    



response_creator(5)




#joined_li = page1 + page2
#big_list = sort_stories_by_votes(joined_li)


#pprint.pprint(big_list)