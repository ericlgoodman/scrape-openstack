"""
=== IMPORTS ===
"""

import requests
from bs4 import BeautifulSoup as bs
import urllib
import xlwt
import operator
import time

# Disguise
class AppURLOpener(urllib.FancyURLopener):
    """
    Class to disguise server requests as incoming from Mozilla Firefox
    """
    version = "Mozilla/5.0"

def views_to_int(views):
    if views.isdigit():
        return int(views)
    elif 'k' in views:
        return int(views.split('k')[0])*1000
    else: # Unclear, assume 0
        return 0


def get_all():

    # Url -> Int dictionary
    dic = {}

    for i in xrange(1, 797):

        # Scrape the whole page
        url = 'https://ask.openstack.org/en/questions/scope:all/sort:activity-desc/page:%s/' % i
        html =  bs(urllib.urlopen(url), 'html.parser')

        # Iterate over all question
        items = html.find_all("div", class_="short-summary")
        for item in items:

            # Get question url
            url = 'https://ask.openstack.org' + item.h2.a['href']

            # Find span containing number of views
            info = item.find('div', class_='counts')
            view_div = info.find('div', class_='views')
            views_string = view_div.find('span', class_='item-count').text
            views = views_to_int(views_string)

            # Add to dictionary
            dic[url] = views

        # Wait to not make the server angry
        time.sleep(.2)

    # Remove entries with less than 100 views
    for question, num_views in dic.items():
        if num_views < 100:
            del dic[question]

    # Sort by views, descending
    sorted_dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)

    # Write to Excel
    book = xlwt.Workbook(encoding="utf-8")
    sheet = book.add_sheet("Sheet 1")

    sheet.write(0, 0, "Question")
    sheet.write(0, 1, "Views")

    for index, data in enumerate(sorted_dic):
        question, num_views = data
        sheet.write(index+1, 0, question)
        sheet.write(index+1, 1, num_views)

    book.save("openstack.xls")


if __name__ == '__main__':
    get_all()