import requests
import codecs
from bs4 import BeautifulSoup

AO3_BASE_URL = 'http://archiveofourown.org/'
FANDOM = 'Lewis%20(TV)'
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


def get_work(work_id):
    url = AO3_BASE_URL + 'works/' + work_id
    r = requests.get(url)
    return r.text


def parse_work(work_id):
    html = BeautifulSoup(get_work(work_id))

    # TODO: limit to single-chaptered fics

    # rating
    # archive warnings
    # categories
    # characters
    # relationships
    # additional tags
    # published date

    # is in series???

    # kudos
    # comments
    # hits
    # number of bookmarks

    # actual people who kudos-ed? - some kind of network analysis

    # title
    # text
    print work_id
    text = html.find('div', class_='userstuff')
    print text

    # notes


def download_fandom():
    last_page_number = get_last_page_number()
    last_page_number = 3  # DEBUG
    for i in range(1, last_page_number + 1):
        work_ids = get_links_on_page(i)
        for work_id in work_ids:
            parse_work(work_id)


print download_fandom()
