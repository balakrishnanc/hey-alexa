#!/usr/bin/env python
# -*- mode: python; coding: utf-8; fill-column: 80; -*-
#
# hey-alexa.py
# Created by Balakrishnan Chandrasekaran on 2017-07-23 17:23 +0200.
# Copyright (c) 2017 Balakrishnan Chandrasekaran <balakrishnan.c@gmail.com>.
#

"""
hey-alexa.py
Utility to scrape the top _N_ Web sites that are freely available on Alexa's
 Web site.


Examples:

§ ./hey-alexa.py global
1,GLOBAL,google.com
2,GLOBAL,youtube.com
...

§ ./hey-alexa.py by-country --url http://www.alexa.com/topsites/countries
1,Afghanistan,google.com.af
2,Afghanistan,google.com
...

§ ./hey-alexa.py by-category --url http://www.alexa.com/topsites/category
1,Arts,youtube.com
2,Arts,facebook.com/#!/JeffDunham
...
"""

__author__  = 'Balakrishnan Chandrasekaran <balakrishnan.c@gmail.com>'
__version__ = '1.0'
__license__ = 'MIT'


import argparse
import sys
from alexa import constants, utils, web


def main(params):
    """Run the script with the supplied parameters.
    """
    if params.mode not in web.MODES:
        raise ValueError("Unsupported mode '%s'!" % (params.mode))

    if params.mode == web.GLOBAL:
        res = web.fetch_global(params.url)
    elif params.mode == web.BY_COUNTRY:
        res = web.fetch_by_country(params.url)
    else:
        res = web.fetch_by_category(params.url, params.unsafe)


    out = params.out_file
    if not params.out_file:
        out = sys.stdout
    else:
        out = utils.fwrite(params.out_file)

    with out:
        for site_info in res:
            out.write(u"%s\n" % constants.COMMA.join(str(v) for v in site_info))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Retrieve the top N Web sites from Alexa's Web site")
    parser.add_argument('mode', metavar='mode',
                        type=str,
                        help='<global|by-country|by-category>')
    parser.add_argument('--unsafe', dest='unsafe',
                        action='store_true',
                        default=False,
                        help='Include even Web sites in the "adult" category')
    parser.add_argument('--url', dest='url', metavar='url',
                        type=str,
                        default='http://www.alexa.com/topsites',
                        help=('Web page containing the relevant details'))
    parser.add_argument('--out', dest='out_file', metavar='output',
                        type=str,
                        help=('Output file path'))
    main(parser.parse_args())
