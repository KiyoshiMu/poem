# use bs4 to get the link of the Japanese poems
# https://kazahanamirai.com/nihon-shiika-selection.html

import os
import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import re
def get_link():
    if os.path.exists('ja_link.json'):
        with open('ja_link.json', 'r') as f:
            link_list = json.load(f)
        return link_list
    url = 'https://kazahanamirai.com/nihon-shiika-selection.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    link_list = {}
    for link in links:
        if link.get('href').startswith('https://kazahanamirai'):
            link_list[link.text] = link.get('href')
    with open('ja_link.json', 'w') as f:
        json.dump(link_list, f, indent=4)
    return link_list

def safe_file_name(string):
    # replace the invalid characters in the file name
    # https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    return re.sub(r'[/\\:*?"<>|\n]', '', string)

def download_poem(link_list):
    # grab the poem from the link by <blockquote> the first one
    # save the cache as well to cache folder as html
    for title, link in tqdm(link_list.items()) :
        fname = safe_file_name(title)
        if os.path.exists('ja_cache/{}.html'.format(fname)):
            with open('ja_cache/{}.html'.format(fname), 'r', encoding='utf-8') as f:
                html = f.read()
        else:
            html = requests.get(link).text
            with open('ja_cache/{}.html'.format(fname), 'w', encoding='utf-8') as f:
                f.write(html)
        soup = BeautifulSoup(html, 'html.parser')
        poem = soup.find('blockquote')
        
        
        with open('ja_poem/{}.txt'.format(fname), 'w', encoding='utf-8') as f:
            if poem is not None:
                f.write(poem.text)
def remove_empty():
    # 
    dir_ = 'ja_poem'
    for fname in os.listdir(dir_):
        with open(os.path.join(dir_, fname), 'r', encoding='utf-8') as f:
            text = f.read()
        if len(text) < 50:
            os.remove(os.path.join(dir_, fname))       
def remove_duplicate():
    dir_ = 'ja_poem'
    #name is in 「 」
    names =set()
    print(len(os.listdir(dir_)))
    for fname in os.listdir(dir_):

        name = re.findall(r'「(.*)」', fname)
        if len(name) == 0:
            os.remove(os.path.join(dir_, fname))
            continue
        else:
            name = name[0]
            if name in names:
                os.remove(os.path.join(dir_, fname))
                print(name)
            else:
                names.add(name)

    
        
if __name__ == '__main__':
    # download_poem(get_link())
    remove_empty()
    remove_duplicate()