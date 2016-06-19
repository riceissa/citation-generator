#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup
import re
from tld import get_tld
import datetime
import dateparser
from dateutil.parser import parse

def soup2dict(soup, dictionary):
    """
    Extract info from BeautifulSoup soup into a dictionary.  Return a modified
    dictionary.
    """
    meta = soup.find_all("meta")
    for tag in meta:
        if tag.get("property") == "og:title":
            dictionary["title"] = tag.get("content")
        elif tag.get("name") == "title":
            dictionary["title"] = tag.get("content")
        elif tag.get("name") == "author":
            dictionary["author"] = tag.get("content")
        elif tag.get("name") == "DCSext.author":
            dictionary["author"] = tag.get("content")
        elif tag.get("name") == "dat":
            dictionary["date"] = tag.get("content")
        if tag.get("property") == "og:site_name":
            dictionary["publisher"] = tag.get("content")
        elif tag.get("name") == "cre":
            dictionary["publisher"] = tag.get("content")
        elif tag.get("property") == "article:published_time":
            dictionary["date"] = tag.get("content")
        elif tag.get("property") == "article:modified_time" and "date" not in dictionary:
            dictionary["date"] = tag.get("content")
    if "title" not in dictionary and soup.title is not None:
        dictionary["title"] = soup.title.string
    #print(soup.find_all("span", class_="author")[0].contents)
    #print(soup.find_all("span", class_="date")[0].contents)
    s = soup.get_text()

    m = re.search(r'((January|February|March|May|June|July|August|September|October|November|December) \d+, \d+|\d+ (January|February|March|May|June|July|August|September|October|November|December) \d+)', s)
    if "date" not in dictionary and m is not None:
        dictionary["date"] = m.group(0)

    if "author" not in dictionary:
        author_candidates = []
        author_candidates.extend(soup.find_all("div", class_="author"))
        author_candidates.extend(soup.find_all("span", class_="author"))
        author_candidates.extend(soup.find_all("p", class_="author"))
        author_candidates.extend(soup.find_all("p", class_="byline"))
        author_candidates.extend(soup.find_all("span", class_="byline__author-name"))
        #print(author_candidates)
        if author_candidates:
            dictionary["author"] = author_candidates[0].get_text()
    m = re.search(r'[Bb]y (\b([A-Z]{1}[a-z]+) ([A-Z]{1}[a-z]+)\b)', s)
    if "author" not in dictionary and m is not None:
        dictionary["author"] = m.group(1)

def get_author(dictionary):
    if "author" in dictionary:
        result = dictionary.get("author").strip()
        result = result.replace("\n", "")
        return result

def get_date(dictionary):
    if "date" in dictionary:
        date_str = dictionary.get("date").strip()
        date = parse(date_str)
        if not date:
            # try parsing the date with a different library
            date = dateparser.parse(date_str)
        if not date:
            # dateparser does not like dates that look like
            # '2011-05-26T13:11:14.000Z', so we shave off the last few characters
            # and try again
            date = dateparser.parse(date_str[:4])
        if not date:
            return date_str
        return date.strftime("%B %-d, %Y")

def get_title(dictionary):
    if "title" in dictionary:
        return dictionary.get("title").strip().replace("|", "-")

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
        "nybooks.com": "The New York Review of Books",
        "who.int": "World Health Organization",
        "givewell.org": "GiveWell",
    }

def get_publisher(dictionary, url):
    if get_tld(url) in publisher_map:
        return publisher_map[get_tld(url)]
    elif "publisher" in dictionary:
        return dictionary.get("publisher").strip()

def get_cite_web(dictionary, url=""):
    result = "<ref>{{cite web "
    result += "|url=" + url + " "
    author = get_author(dictionary)
    date = get_date(dictionary)
    title = get_title(dictionary)
    publisher = get_publisher(dictionary, url)
    if author:
        result += "|author=" + author + " "
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
