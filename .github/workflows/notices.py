import arrow
import bleach
import feedparser

from bs4 import BeautifulSoup

print(f"🐞 arrow.utcnow(): {arrow.utcnow()}")
print(f"🐞 arrow.now(): {arrow.now()}")

def create_notice(entry):
    soup = BeautifulSoup(f'<div>{bleach.clean(entry["libcal_description"], tags=["a", "b", "code", "em", "i", "span", "strong"], attributes={"a": ["href"], "span": ["class"]}, strip=True)}</div>', "html.parser")
    level = entry["libcal_location"].split()[-1].lower()
    print(soup)
    soup.div.wrap(soup.new_tag("div", attrs={"class": "alert alert-dismissible", "role": "alert"}))
    soup.div["class"].append(f"alert-{level}")
    soup.div.div.insert_before(soup.new_tag("button", attrs={"aria-label": "Close", "class": "close", "data-dismiss": "alert", "type": "button"}))
    print(soup)
    soup.button.insert_before("\n  ")
    soup.button.append(soup.new_tag("span", attrs={"aria-hidden": "true"}))
    soup.button.span.append("×")
    soup.button.insert_after("\n  ")
    if soup.a:
        soup.a["class"] = "alert-link"
    soup.div.div.unwrap()
    print(soup)
    return str(soup)

notices = feedparser.parse("https://libcal.caltech.edu/rss.php?cid=5754&m=day")
with open("fragments/notices.html", "w") as fp:
    for entry in notices.entries:
        datetimetz_string = f'{entry["libcal_date"]} {entry["libcal_end"]} America/Los_Angeles'
        print(f'🐞 arrow.get(): {arrow.get(datetimetz_string, "YYYY-MM-DD HH:mm:ss ZZZ")}')
        if arrow.get(datetimetz_string, "YYYY-MM-DD HH:mm:ss ZZZ") < arrow.now():
            print(f"🐞 {datetimetz_string} < arrow.now(): {arrow.now()}")
            # TODO we need to hide this entry
        else:
            print(f"🐞 {datetimetz_string} > arrow.now(): {arrow.now()}")
            fp.write(f"{create_notice(entry)}\n")
