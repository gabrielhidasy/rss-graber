# RSS getter

## A simple script to download torrent files from RSS feeds.

It exists because I could not make rssdler work well.

It enables downloading multiple feeds, filtering torrents by regexes.
* Required: A feed must match the required regex.
* Forbidden: A feed cannot match the forbidden regex

Yes, thats many, regexes are powerful

Can save each feed to an specific folder.

It works only on feeds that provide magnet links


# TODO

* Make sources an external resorce (JSON? YAML? XML?)
* Use docopt to make an usable program (with functions to add, edit
  and remove sources)
* Migrate downloaded-list to a real DB or at least keep the list in memory
* Fetch feeds in parallel (will need to work on logging first, or else race conditions)
* Better exception handling (more try: excepts, and specify the excepts)
