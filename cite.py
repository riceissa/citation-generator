#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup
import re

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
    if "author" not in dictionary:
        dictionary["author"] = m.group(1)

def get_author(dictionary):
    return "hi"

def get_date(dictionary):
    pass

def get_title(dictionary):
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
