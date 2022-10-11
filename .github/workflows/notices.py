import arrow
import bleach
import feedparser

from bs4 import BeautifulSoup

notices = feedparser.parse("https://libcal.caltech.edu/rss.php?cid=5754&m=day")

print(f"🐞 arrow.utcnow(): {arrow.utcnow()}")
print(f"🐞 arrow.now(): {arrow.now()}")

def create_notice(entry):
    # wrap description in a div initially for ease in working with soup
    soup = BeautifulSoup(f'<div>{bleach.clean(entry["libcal_description"], tags=["a", "b", "code", "em", "i", "span", "strong"], attributes={"a": ["href"], "span": ["class"]}, strip=True)}</div>', "html.parser")
    level = entry["libcal_location"].split()[-1].lower()
    # wrap with bootstrap 3 alert markup
    soup.div.wrap(soup.new_tag("div", attrs={"class": "alert alert-dismissible", "role": "alert"}))
    soup.div["class"].append(f"alert-{level}")
    soup.div.div.insert_before(soup.new_tag("button", attrs={"aria-label": "Close", "class": "close", "data-dismiss": "alert", "type": "button"}))
    soup.div.div.insert_after("\n")  # prettify
    soup.button.insert_before("\n  ")  # prettify
    soup.button.append(soup.new_tag("span", attrs={"aria-hidden": "true"}))
    soup.button.span.append("×")
    soup.button.insert_after("\n  ")  # prettify
    # there will not always be links in the description
    if soup.a:
        soup.a["class"] = "alert-link"
    # remove the helper div around description
    soup.div.div.unwrap()
    return str(soup)

with open("fragments/notices.html", "w") as fp:
    for entry in notices.entries:
        # create date/time/tz string from feed entry elements
        datetimetz_string = f'{entry["libcal_date"]} {entry["libcal_end"]} America/Los_Angeles'
        print(f'🐞 arrow.get(): {arrow.get(datetimetz_string, "YYYY-MM-DD HH:mm:ss ZZZ")}')
        if arrow.get(datetimetz_string, "YYYY-MM-DD HH:mm:ss ZZZ") > arrow.now():
            print(f"🐞 {datetimetz_string} > arrow.now(): {arrow.now()}")
            fp.write(f"{create_notice(entry)}\n")
