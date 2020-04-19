from eth_web_scraping.helper_functions import parse_single_url
from eth_web_scraping.helper_functions import print_pandas_data
import re
import requests
import pandas as pd


class Example:
    """
    This is a class for demonstrating examples.
    """

    def __init__(self, main_url="http://books.toscrape.com/index.html"):
        self.main_url = main_url

    def get_interested_urls_from_pages(self, pages_urls, element_name="article", element_class_="product_pod"):
        result_urls = []
        for page in pages_urls:
            # Remove the index.html part of the base url before returning the results.
            result_urls.extend(["/".join(self.main_url.split("/")[:-1]) + "/" + x.div.a.get('href') for x in
                                parse_single_url(page).findAll(element_name, class_=element_class_)])
        return result_urls

    def get_all_page_urls(self):
        pages_urls = [self.main_url]
        soup = parse_single_url(self.main_url)
        while len(soup.findAll("a", href=re.compile("page"))) == 2 or len(pages_urls) == 1:
            # Get the new complete url by adding the fetched URL to the main URL (and removing the .html part of the
            # main URL).
            new_url = "/".join(pages_urls[-1].split("/")[:-1]) + "/" + soup.findAll("a", href=re.compile("page"))[
                -1].get(
                "href")

            # Add the URL to the list.
            pages_urls.append(new_url)

            # Parse the next page.
            soup = parse_single_url(new_url)
        return pages_urls

    def organize_data(self, input_urls):
        names = []
        prices = []
        nb_in_stock = []
        img_urls = []
        categories = []
        ratings = []
        # Scrape data for every book URL: this may take some time.
        for url in input_urls:
            if requests.get(url).status_code != 404:
                soup = parse_single_url(url)
                # Get product name.
                names.append(soup.find("div", class_=re.compile("product_main")).h1.text)
                # Get product price.
                prices.append(soup.find("p", class_="price_color").text[2:])  # get rid of the pound sign
                # Get number of available products.
                nb_in_stock.append(re.sub("[^0-9]", "", soup.find("p",
                                                                  class_="instock availability").text))  # get rid of non numerical characters
                # Get image url.
                img_urls.append(url.replace("index.html", "") + soup.find("img").get("src"))
                # Get product category.
                categories.append(soup.find("a", href=re.compile("../category/books/")).get("href").split("/")[3])
                # Get ratings.
                ratings.append(soup.find("p", class_=re.compile("star-rating")).get("class")[1])

        scraped_data = pd.DataFrame(
            {'Name': names, 'Price': prices, 'Number in Stock': nb_in_stock, "Image URL": img_urls,
             "Product Category": categories,
             "Rating": ratings})
        return scraped_data


if __name__ == "__main__":
    example_obj = Example()
    all_page_urls = example_obj.get_all_page_urls()
    interested_urls = example_obj.get_interested_urls_from_pages(all_page_urls)
    print(str(len(interested_urls)) + " fetched interested urls")
    pandas_data = example_obj.organize_data(interested_urls)
    print_pandas_data(pandas_data)
