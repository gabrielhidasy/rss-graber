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
                mlink = re.findall(r"<torrent:magnetURI><!\[CDATA\[(.*)\]\].*</torrent:magnetURI>", entry, re.DOTALL)[0]
                if not re.search(URL["regex-yes"], title, re.DOTALL):
                        continue
                if URL["regex-not"] and re.search(URL["regex-not"], title, re.DOTALL):
                        continue
                try:
                        with open("download_log.dat", "r") as f:
                                if mlink in f.read():
                                        print("Skipping {} (already downloaded)".format(title))
                                        continue
                except:
                        pass
                print("Downloading {}".format(title))
                # Generate torrent from magnet on the fly, it seems more
                # reliable then trying to download the .torrent, might be useful
                # to import a library to generate more complete torrent files
                with open("meta-{}.torrent".format("_".join(title.split(" "))),"w") as f:
                          f.write("d10:magnet-uri{}:{}e\n".format(len(mlink), mlink))

                          with open("download_log.dat", "a+") as f:
                        f.write(mlink)
                        f.write("\n")
                # I know file handling here is sketchy at best, will probably
                # change it for sqlite soon

