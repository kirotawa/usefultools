#!/usr/bin/python3

import sys
import random
import argparse
import requests

from bs4 import BeautifulSoup


URL_BASE = "https://www.whatsmydns.net/"
QENTRY="?q="


def get_random_ua():
    ua_list = [
            "Windows-AzureAD-Authentication-Provider/1.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 musical_ly_25.1.1 JsSdk/2.0 NetType/WIFI Channel/App Store ByteLocale/en Region/US ByteFullLocale/en isDarkMode/0 WKWebView/1 BytedanceWebview/d8a21c6 FalconTag/",
    ]

    return random.choice(ua_list)

user_agent = {'User-agent': get_random_ua()}


def get_url(opt_type, domain):

    url = ''
    opt_types = {
            'exp': 'domain-expiration',
            'avail': 'domain-availability'
    }

    if opt_type in opt_types.keys():
        url = "{}{}{}{}".format(URL_BASE, opt_types[opt_type], QENTRY, domain)
        return url

    if not url:
        print("Error while getting the URL")
        sys.exit(1)


def get_page_content(url):
    page = requests.get(url, headers = user_agent)

    soup = None
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    if not soup:
        print("Error getting the URL content page")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--expiring", default=False, action="store_true",
            help="To check the expiring info")
    parser.add_argument("-d", "--domain", dest="domain", default=None,
            help="The domain to be checked against")
    parser.add_argument("-a", "--availability", default=False,
            action="store_true", help="Checks if the domain is available")
    (opt, args) = parser.parse_known_args()

    if not opt.domain:
        parser.print_help()
        sys.exit(1)

    if opt.expiring:
        url = get_url('exp', opt.domain)
        soup = get_page_content(url)

        info = soup.find_all('strong')
        if not info:
            print("Error in getting info from thr URL content")
            sys.exit(1)

        if info:
            if len(info) == 1:
                print("Invalid domain")
            else:
                info_filtered = [entry.text for entry in info]
                print("Site: {}".format(info_filtered[0]))
                print("Expires on: {}".format(info_filtered[1]))

    if opt.availability:
        url = get_url('avail', opt.domain)
        soup = get_page_content(url)
        info = soup.find_all('strong')

        if info:
            info_filtered = [entry.text for entry in info]
            print("Site: {}".format(info_filtered[0]))
            print("Situation is: {}".format(info_filtered[1]))


if __name__ == "__main__":
    main()
