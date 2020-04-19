#! usr/bin/env python

from setuptools import find_packages
from setuptools import setup
import os

install_requires = [
      'requests',
      'pandas',
      'selenium',
      'bs4',
      'feedparser',
      'pprint',
      'lxml'
]

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='eth_web_scraping',
      version='0.1.0',
      packages=find_packages(),
      package_data={  # Optional
        'eth_web_scraping': ['files/*'],
      },
      author="Guoxiang Zhou",
      author_email="harigxzhou@gmail.com",
      url="https://github.com/zgxsin/web_scraping",
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords=['Web Scrapping', 'ETH Students'],
      description="Search ETH Rooms for ETH Students",
      install_requires=install_requires,
      python_requires='>=3.6',
      entry_points={  # Optional
            'console_scripts': [
                  'eth_web_scrape=eth_web_scraping.main:main',
            ],
      },

)