#!/usr/bin/python
import re
import urllib.request
import zlib

Sources = [
        {
                "URL": "https://fakeurl.to/?rss=1",
                "gzip": True,
                "regex-yes": r"(Serie I like)",
                "regex-not": r"(Codec I hate)"
        }
]

for URL in Sources:
        full_page = urllib.request.urlopen(URL["URL"]).read()
        print("Page read")
        if URL["gzip"]:
                # Magic +47 bytes required here
                full_page = zlib.decompress(full_page, 15+32)
        data = full_page.decode("utf-8")
        feed = re.findall(r"<item>.*?</item>", data, re.DOTALL)
        for entry in feed:
                title = re.findall(r"<title>(.*)</title>", entry, re.DOTALL)[0]
                tlink = re.findall(r"<enclosure url=\"(.*\.torrent).*/>", entry, re.DOTALL)
                if not re.search(URL["regex-yes"], title, re.DOTALL):
                        continue
                if URL["regex-not"] and re.search(URL["regex-not"], title, re.DOTALL):
                        continue
                print(title, tlink)
                print("----------------------------------")
