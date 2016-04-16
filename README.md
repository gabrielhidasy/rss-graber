# RSS getter

## A simple script to download torrent files from RSS feeds.

It exists because I could not make rssdler work well.

For now its a bad solution, relying on curl and gunzip instead
of downloading and decompressing in pure python. And it does
not save the torrent files, just display their URLS, but that's
an start.

It will have in future the possibility to filter feeds in many ways, namely:

* Required: A feed must match all required regexes.
* Sufficient: A feed must match one of the sufficient regexes
* Forbidden: A feed cannot have any forbidden regexes
