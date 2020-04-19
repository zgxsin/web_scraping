import requests
from bs4 import BeautifulSoup
import pandas
import lxml


def parse_single_url(url):
    response_obj = requests.get(url)
    soup_obj = BeautifulSoup(response_obj.text, 'lxml')
    return soup_obj


def print_pandas_data(pandas_data):
    print(pandas_data.to_string())
