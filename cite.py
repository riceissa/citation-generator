#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup

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

def get_author(soup):
    return "hi"

def get_date(soup):
    pass

def get_title(soup):
    pass



def get_cite_web(soup, url=""):
    result = "{{cite web "
    result += "|url=" + url + " "
    date = get_date(soup)
    title = get_title(soup)
    if date:
        result += "|date=" + date + " "
    if title:
        result += "|title=" + title + " "
    result = result.strip()
    result += "}}"
    return result

if __name__ == "__main__":
    soup = BeautifulSoup(sys.stdin, "html.parser")
    d = dict()
    soup2dict(soup, d)
    print(d)
    print(sys.argv[1])
