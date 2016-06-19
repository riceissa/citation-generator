#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup
import re
from tld import get_tld
import datetime

def soup2dict(soup, dictionary):
    """
    Extract info from BeautifulSoup soup into a dictionary.  Return a modified
    dictionary.
    """
    meta = soup.find_all("meta")
    for tag in meta:
        if tag.get("property") == "og:title":
            dictionary["title"] = tag.get("content").strip()
        elif tag.get("name") == "title":
            dictionary["title"] = tag.get("content").strip()
        elif tag.get("name") == "author":
            dictionary["author"] = tag.get("content").strip()
        elif tag.get("name") == "dat":
            dictionary["date"] = tag.get("content").strip()
        elif tag.get("name") == "cre":
            dictionary["publisher"] = tag.get("content").strip()
    if "title" not in dictionary and soup.title is not None:
        dictionary["title"] = soup.title.string.strip()
    #print(soup.find_all("span", class_="author")[0].contents)
    #print(soup.find_all("span", class_="date")[0].contents)
    s = soup.get_text()
    m = re.search(r'By (\w* \w*)', s)
    if "author" not in dictionary and m is not None:
        dictionary["author"] = m.group(1)
    m = re.search(r'((January|February|March|May|June|July|August|September|October|November|December) \d+, \d+|\d+ (January|February|March|May|June|July|August|September|October|November|December) \d+)', s)
    if "date" not in dictionary and m is not None:
        dictionary["date"] = m.group(0)

def get_author(dictionary):
    return dictionary.get("author")

def get_date(dictionary):
    return dictionary.get("date")

def get_title(dictionary):
    return dictionary.get("title")

publisher_map = {
        "huffingtonpost.com": "The Huffington Post",
        "lesswrong.com": "LessWrong",
        "nytimes.com": "The New York Times",
        "huffingtonpost.ca": "Huffington Post Canada",
        "washingtonpost.com": "The Washington Post",
        "indiatimes.com": "The Times of India",
        "bostonglobe.com": "The Boston Globe",
        "mirror.co.uk": "Mirror",
        "telegraph.co.uk": "The Telegraph",
        "bloomberg.com": "Businessweek",
        "ft.com": "Financial Times",
        "economist.com": "The Economist",
        "arstechnica.com": "Ars Technica",
        "wsj.com": "The Wall Street Journal",
        "theguardian.com": "The Guardian",
        "independent.co.uk": "The Independent",
        "theregister.co.uk": "The Register",
    }

def get_publisher(dictionary, url):
    if get_tld(url) in publisher_map:
        return publisher_map[get_tld(url)]
    else:
        return dictionary.get("publisher")

def get_cite_web(dictionary, url=""):
    result = "<ref>{{cite web "
    result += "|url=" + url + " "
    date = get_date(dictionary)
    title = get_title(dictionary)
    publisher = get_publisher(dictionary, url)
    if date:
        result += "|date=" + date + " "
    if title:
        result += "|title=" + title + " "
    if publisher:
        result += "|publisher=" + publisher + " "
    result += "|accessdate=" + datetime.date.today().strftime("%B %-d, %Y")
    result = result.strip()
    result += "}}</ref>"
    return result

if __name__ == "__main__":
    soup = BeautifulSoup(sys.stdin, "html.parser")
    d = dict()
    soup2dict(soup, d)
    print(get_cite_web(d, sys.argv[1]))
