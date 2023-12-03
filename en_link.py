# https://100.best-poems.net/top-100-best-poems.html

import os
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import re
from selenium import webdriver
import requests


def get_link():
    driver = webdriver.Chrome()
    if os.path.exists("en_link.json"):
        with open("en_link.json", "r") as f:
            link_list = json.load(f)
        return link_list
    url = "https://100.best-poems.net/top-100-best-poems.html"
    driver.get(url)
    html = driver.page_source
    with open("en_cache/top-100-best-poems.html", "w", encoding="utf-8") as f:
        f.write(html)
    soup = BeautifulSoup(html, "html.parser")
    # id="content"
    links = soup.find("div", id="content").find_all("a")
    link_list = {}
    for link in links:
        if link.get("href").startswith("/"):
            link_list[link.text] = link.get("href")
    with open("en_link.json", "w") as f:
        json.dump(link_list, f, indent=4)
    return link_list


def safe_file_name(string):
    # replace the invalid characters in the file name
    # https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    return re.sub(r'[/\\:*?"<>|\n]', "", string)


def download_poem(link_list):
    # grab the poem from the link by class="content-poetry"
    # save the cache as well to cache folder as html
    # no javascript, no images, no css
    option = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values": {"images": 2, "javascript": 2}}
    option.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=option)
    for title, link in tqdm(link_list.items()):
        fname = safe_file_name(title)
        if os.path.exists("en_cache/{}.html".format(fname)):
            with open("en_cache/{}.html".format(fname), "r", encoding="utf-8") as f:
                html = f.read()
        else:
            driver.get(f"https://100.best-poems.net/{link}")
            html = driver.page_source
            with open("en_cache/{}.html".format(fname), "w", encoding="utf-8") as f:
                f.write(html)
        soup = BeautifulSoup(html, "html.parser")
        poem = soup.find("div", class_="content-poetry")

        with open("en_poem/{}.txt".format(fname), "w", encoding="utf-8") as f:
            if poem is not None:
                f.write(poem.text)
                
# love, sadness, happiness, anger, hope, disgust, fear, surprise

if __name__ == "__main__":
    link_list = get_link()
    download_poem(link_list)
    print(len(os.listdir("en_poem")))
