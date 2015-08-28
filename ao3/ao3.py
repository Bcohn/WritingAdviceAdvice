import requests
import codecs
from bs4 import BeautifulSoup
from collections import OrderedDict
import json

AO3_BASE_URL = 'http://archiveofourown.org/'
FANDOM = 'Lewis%20(TV)'
CONSTRUCTED_URL = AO3_BASE_URL + 'tags/' + FANDOM + '/works'


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


def get_work(work_id):
    url = AO3_BASE_URL + 'works/' + work_id + '?view_adult=true'
    r = requests.get(url)
    return r.text


def parse_work(work_id):
    print "Parsing work_id %s" % work_id

    html = BeautifulSoup(get_work(work_id))

    # TODO: extend to multi-chaptered fics

    metadata = html.find('dl', class_='stats')
    # extract out the keys for metadata, such as 'Kudos'
    keys = list()
    for node in metadata.findAll('dt'):
        keys.append(','.join(node.findAll(text=True)))

    # extract out the values for metadata, e.g. the actual number of kudos-es
    values = list()
    for node in metadata.findAll('dd'):
        values.append(','.join(node.findAll(text=True)))
    all_data = OrderedDict(zip(keys, values))

    # extract out the actual text - handles single chapters only
    text = html.find('div', class_='userstuff').get_text()
    all_data['text'] = text

    return all_data


def download_fandom():
    last_page_number = get_last_page_number()
    last_page_number = 1  # DEBUG - remove this line to get all

    all_data = OrderedDict()
    for i in range(1, last_page_number + 1):
        work_ids = get_links_on_page(i)
        for work_id in work_ids:
            all_data[work_id] = parse_work(work_id)

    with open(FANDOM + '.json', 'w') as f:
        f.write(json.dumps(all_data))


download_fandom()
