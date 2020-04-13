#!/usr/bin/env python3
# Based on: https://towardsdatascience.com/how-to-get-the-latest-covid-19-news-using-google-news-feed-950d9deb18f1
import feedparser
from pprint import pprint
from bs4 import BeautifulSoup

url = "http://news.google.com/news?q=covid-19&hl=en-US&sort=date&gl=US&num=100&output=rss"

class ParseFeed:

    def __init__(self, url):
        self.feed_url = url

    def clean(self, html):
        '''
        Get the text from html and do some cleaning
        '''
        soup = BeautifulSoup(html, features="lxml")
        text = soup.get_text()
        # text = text.replace('\xa0', ' ')
        return text

    def parse(self):
        '''
        Parse the URL, and print all the details of the news 
        '''
        feeds = feedparser.parse(self.feed_url).entries
        for f in feeds:
            pprint({
                'Description': self.clean(f.get("description", "")),
                'Published Date': f.get("published", ""),
                'Title': f.get("title", ""),
                'Url': f.get("link", "")
            })

feed = ParseFeed(url)
feed.parse()
