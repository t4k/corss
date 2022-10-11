import arrow
import bleach
import feedparser

from bs4 import BeautifulSoup

print(f"🐞 arrow.utcnow(): {arrow.utcnow()}")
print(f"🐞 arrow.now(): {arrow.now()}")

notices = feedparser.parse("https://libcal.caltech.edu/rss.php?cid=5754&m=day")
for entry in notices.entries:
    datetimetz_string = f'{entry["libcal_date"]} {entry["libcal_end"]} America/Los_Angeles'
    print(f'🐞 arrow.get(): {arrow.get(datetimetz_string, "YYYY-MM-DD HH:mm:ss ZZZ")}')
