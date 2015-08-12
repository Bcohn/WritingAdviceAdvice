from bs4 import BeautifulSoup
import urllib
import pandas as pd
import cookielib
import numpy as np
import seaborn as sns
import matplotlib as plt
import numpy as np
import seaborn as sns
import requests
import codecs


sns.set(style="white")
# %matplotlib inline
sns.set(style="white")
 
AO3_BASE_URL = 'http://archiveofourown.org/'
FANDOM = 'Hetalia:%20Axis%20Powers'
CONSTRUCTED_URL = AO3_BASE_URL + 'tags/' + FANDOM + '/works'
# TODO: construct URL based on filters

def get_last_page_number():
    # first get the first page and count how many pages there are
    first_page = CONSTRUCTED_URL
    r = requests.get(first_page)

    # parse the text with BeautifulSoup to obtain the last page number
    soup = BeautifulSoup(r.text)
    pagination = soup.find('ol', class_='pagination actions')
    return pagination.find_all('a')[-2].text


def get_links_on_page(page_number):
    url = CONSTRUCTED_URL + '?page=%s' % page_number
    r = requests.get(url)
    # get the list of links to fics on this page
    soup = BeautifulSoup(r.text)
    links = soup.find_all('li', class_='work blurb group')
    return [link['id'].split('_')[1] for link in links]

def download_work_ids():
    # A modified version of "get_fandom() to download all work_ids in a fandom 
    last_page_number = 724
    result=list()
    for i in range(1, last_page_number + 1):
        print(i)
        try:
            work_ids = get_links_on_page(i)
            for work_id in work_ids:
                result.append(work_id)
        except Exception:
            pass
    return result


def MakeData(workId):
    # Downloads the statistics associated with a particular work ID, and returns a dictionary 
    r = urllib.urlopen('http://archiveofourown.org/works/'+workId).read()
    soup = BeautifulSoup(r)
    metaData= soup.find("dl",class_="stats")
    categories=list()
    categories.append("WorkID")
    for node in metaData.findAll('dt'):
        categories.append(','.join(node.findAll(text=True)))
    values=list()
    values.append(workId)
    for node in metaData.findAll('dd'):
        values.append(','.join(node.findAll(text=True)))
    output = dict(zip(categories,values))
    return(output)


def MakeListofMetaData(workIds):
    # Takes a list of workIds and returns a list of dictionaries containing their statistics.
    ListofMetaData=list()
    for i in workIds:
        print(i)
        try:
            ListofMetaData.append(MakeData(i))
        except Exception:
            pass
    return ListofMetaData
        

# To Convert List of dictionaries to Pandas Dataframe:

# df=pd.DataFrame(stuff)
