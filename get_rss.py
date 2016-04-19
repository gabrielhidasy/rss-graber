#!/usr/bin/python
import re
import urllib.request
import yaml
import zlib

config = yaml.load(open("config.yaml").read())
Sources = config["Sources"]
log_path = config.get("log_path", "./")

for URL in Sources:
        full_page = urllib.request.urlopen(URL["URL"]).read()
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
                        with open("{}download_log.dat".format(log_path), "r") as f:
                                if mlink in f.read():
                                        print("Skipping {} (already downloaded)".format(title))
                                        continue
                except:
                        pass
                print("Downloading {}".format(title))
                # Generate torrent from magnet on the fly, it seems more
                # reliable then trying to download the .torrent, might be useful
                # to import a library to generate more complete torrent files
                with open("{}/meta-{}.torrent".format(URL["store-torrents"], "_".join(title.split(" "))),"w") as f:
                          f.write("d10:magnet-uri{}:{}e\n".format(len(mlink), mlink))

                with open("download_log.dat", "a+") as f:
                        f.write(mlink)
                        f.write("\n")
                # I know file handling here is sketchy at best, will probably
                # change it for sqlite soon

