#!/usr/bin/env python
# Source: https://towardsdatascience.com/an-introduction-to-web-scraping-with-python-a2601e8619e5

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd



def getAndParseSingleURL(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    return (soup)


def getSpecificURLs(main_url, element_name="article", element_class_="product_pod"):
    specificURLs = []
    pages_urls = getAllPageURLs(main_url)
    for page in pages_urls:
        # remove the index.html part of the base url before returning the results
         specificURLs.extend(["/".join(main_url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in
                              getAndParseSingleURL(page).findAll(element_name, class_=element_class_)])
    return specificURLs


def getAllPageURLs(main_url):
    pages_urls = [main_url]
    soup = getAndParseSingleURL(main_url)
    while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:
        # get the new complete url by adding the fetched URL to the base URL (and removing the .html part of the base URL)
        new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[-1].get(
            "href")

        # add the URL to the list
        pages_urls.append(new_url)

        # parse the next page
        soup = getAndParseSingleURL(new_url)
    return pages_urls

def organizeData(specificURLs):
    names = []
    prices = []
    nb_in_stock = []
    img_urls = []
    categories = []
    ratings = []
    # scrape data for every book URL: this may take some time
    for url in specificURLs:
        if requests.get(url).status_code != 404:
            soup = getAndParseSingleURL(url)
            # product name
            names.append(soup.find("div", class_=re.compile("product_main")).h1.text)
            # product price
            prices.append(soup.find("p", class_="price_color").text[2:])  # get rid of the pound sign
            # number of available products
            nb_in_stock.append(re.sub("[^0-9]", "", soup.find("p",
                                                              class_="instock availability").text))  # get rid of non numerical characters
            # image url
            img_urls.append(url.replace("index.html", "") + soup.find("img").get("src"))
            # product category
            categories.append(soup.find("a", href=re.compile("../category/books/")).get("href").split("/")[3])
            # ratings
            ratings.append(soup.find("p", class_=re.compile("star-rating")).get("class")[1])

    scraped_data = pd.DataFrame(
        {'name': names, 'price': prices, 'nb_in_stock': nb_in_stock, "url_img": img_urls,
         "product_category": categories,
         "rating": ratings})
    # scraped_data.head()
    return scraped_data.to_string()



main_url = "http://books.toscrape.com/index.html"
specificURLs = getSpecificURLs(main_url)
print(str(len(specificURLs)) + " fetched specific URLs")
print(organizeData(specificURLs[0:2]))











