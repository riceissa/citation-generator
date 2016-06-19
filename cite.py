#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup

def soup2dict(soup, dictionary):
    """
    Extract info from BeautifulSoup soup into a dictionary.  Return a modified
    dictionary.
    """
    m = soup.find_all("meta")
    for i in m:
        if i.get("property") is not None and "og:" in i.get("property"):
            print(i)
    if "title" not in dictionary:
        dictionary["title"] = soup.title.string

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
