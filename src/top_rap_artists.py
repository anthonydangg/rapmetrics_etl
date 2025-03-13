import requests
from bs4 import BeautifulSoup

import random
import re
import pandas as pd
import numpy as np

from datetime import datetime


def scrape(link):
    headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0)',
            ])
        }
    
    html_text = requests.get(link, headers=headers).text

    return BeautifulSoup(html_text, 'lxml')

def get_top_monthly_listeners():
    kworb_link = 'https://kworb.net/spotify/listeners.html'

    soup = scrape(kworb_link)
    table = soup.select('tbody')[0].select('tr')

    data = {}
    for rank, row in enumerate(table[:500]):
        artist = row.select('td')[0].text.encode("latin-1").decode("utf-8")
        data[artist] = {}
        data[artist]["ranking"] = int(rank + 1)
        data[artist]["monthly_listners"] = int(str.replace(row.select('td')[1].text, ",", ""))

    return data

def get_rap_albums():
    wiki_link = 'https://en.wikipedia.org/wiki/2025_in_hip-hop'

    soup = scrape(wiki_link)
    wiki_scrape = soup.select('div.mw-heading.mw-heading3,table.wikitable')

    data = {}
    prev_header = None

    for n in wiki_scrape:
        if n.get('class') == ['mw-heading', 'mw-heading3']:
            prev_header = n.find('h3').get('id')
        elif n.get('class') == ['wikitable']:
            data[prev_header] = pd.read_html(str(n))[0]

    df_lst = []
    for month, table in data.items():
        table['Month'] = re.sub('[^a-zA-Z]+', '', month)
        df_lst.append(table)

    albums_release_data = pd.concat(df_lst)
    albums_release_data = albums_release_data[['Artist(s)','Album','Record label(s)', 'Month', 'Day']]
    albums_release_data['Month'] = albums_release_data['Month'].replace('UnscheduledandTBA', np.nan)
    albums_release_data['Day'] = albums_release_data['Day'].replace('TBA', np.nan)

    return albums_release_data

def top_rap_intersection():    
    top_artists = get_top_monthly_listeners()
    albums_release_data = get_rap_albums()

    lowercase_artists =  {k.lower(): v for k, v in top_artists.items()}
    top_rap_artists = albums_release_data[albums_release_data['Artist(s)'].str.lower().isin(lowercase_artists)]

    return top_rap_artists

print(top_rap_intersection())