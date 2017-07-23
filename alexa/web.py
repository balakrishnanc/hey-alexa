#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# web.py
# Created by Balakrishnan Chandrasekaran on 2017-07-23 17:50 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balakrishnan.c@gmail.com>.
#

"""
web.py
Utility methods for fetching content from the Alexa Web site and parsing the
data from the fetched content.
"""

__author__  = 'Balakrishnan Chandrasekaran <balakrishnan.c@gmail.com>'
__version__ = '1.0'
__license__ = 'MIT'


from collections import namedtuple as nt
import io
import re
import requests
from urllib.parse import urlparse, urlunparse
from . import constants as const


# Regular expressions to detect the Web site's URL.
SITE_URL_PAT = re.compile(r'<a\s+href="/siteinfo/(.*?)">')

# Regular expressions to extract the country listing.
COUNTRY_LST_PAT = \
    re.compile(r'<a\s+href=["\'](/topsites/countries/.*?)["\']>(.*?)<')

# Regular expressions to extract the category listing.
CATEGORY_LST_PAT = \
    re.compile(r'<a\s+href=["\'](/topsites/category/Top/.*?)["\']>(.*?)<')

# Regular expression to extract country code from 'URL path'
CC_CODE_PAT = re.compile(r'^/topsites/countries/(.*?)$')


# Categories under which Alexa publishes a Top-N list of Web sites.
GLOBAL = 'global'
BY_COUNTRY = 'by-country'
BY_CATEGORY = 'by-category'
MODES = set([GLOBAL, BY_COUNTRY, BY_CATEGORY])


# Web site details.
SiteInfo = nt('SiteInfo', ('rank', 'tag', 'site'))


def get_page(url):
    """Slurp content at the given URL.
    """
    return requests.get(url).text


def fetch_global(url):
    """Fetch top _N_ Web sites from the 'Global' list.
    """
    for rank, site in enumerate(parse_page(get_page(url))):
        yield SiteInfo(rank+1, 'Global', site)


def fetch_by_country(url):
    """Fetch top _N_ Web sites from the 'By Country' list.
    """
    parts = urlparse(url)
    for cc_path, cc_name in parse_country(get_page(url)):
        # Country code in the URL path.
        # cc = CC_CODE_PAT.match(cc_path).groups()[0]

        # URL to fetch the top-N Web sites associated with the country.
        cc_url = urlunparse((parts.scheme, parts.netloc, cc_path, '', '', ''))

        for rank, site in enumerate(parse_page(get_page(cc_url))):
            yield SiteInfo(rank+1, cc_name, site)


def fetch_by_category(url, unsafe=False):
    """Fetch top _N_ Web sites from the 'By Category' list.
    """
    parts = urlparse(url)
    for cat_path, cat_name in parse_category(get_page(url)):
        if not unsafe and cat_name.lower() == 'adult':
            continue

        # URL to fetch the top-N Web sites associated with the category.
        cat_url = urlunparse((parts.scheme, parts.netloc, cat_path, '', '', ''))

        for rank, site in enumerate(parse_page(get_page(cat_url))):
            yield SiteInfo(rank+1, cat_name, site)


def parse_page(page):
    """Parse Web page to retrieve the Web site URLs.
    """
    for line in (line.strip() for line in page.split(const.NEWLINE) if line):
        m = SITE_URL_PAT.match(line)
        if not m:
            continue

        yield m.groups()[0]


def parse_country(page):
    """Parse country listing from the Web page.
    """
    for line in (line.strip() for line in page.split(const.NEWLINE) if line):
        for cc_info in COUNTRY_LST_PAT.findall(line):
            yield cc_info


def parse_category(page):
    """Parse category listing from the Web page.
    """
    for line in (line.strip() for line in page.split(const.NEWLINE) if line):
        for cat_info in CATEGORY_LST_PAT.findall(line):
            yield cat_info
