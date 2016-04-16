#!/usr/bin/python
import sys
import subprocess
import re
import urllib.request
import xmltodict
import gzip
import zlib
import re
import feedparser
from io import StringIO
Sources = [{"URL": "https://kat.cr/?rss=1", "gzip": True}]
for URL in Sources:
        full_page = urllib.request.urlopen(URL["URL"]).read()
        print("Page read")
        if URL["gzip"]:
                # command = "gunzip"
                # full_page = subprocess.check_output(command.split(), input=full_page)
                # page_file = StringIO(str(full_page))
                full_page = zlib.decompress(full_page, 15+32)
        data = full_page.decode("utf-8")
        feed = re.findall(r"<item>.*?</item>", data, re.DOTALL)
        for entry in feed:
                title = re.findall(r"<title>(.*)</title>", entry, re.DOTALL)
                tlink = re.findall(r"<enclosure url=\"(.*\.torrent).*/>", entry, re.DOTALL)
                print(title, tlink)
                print("----------------------------------")
