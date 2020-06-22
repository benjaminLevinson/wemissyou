from datetime import date
from scraper import scraper
import random
import requests
import re
import twitter
import os


def tweet(text):
    api = twitter.Api(consumer_key=os.getenv("OBIT_CONSUMER_KEY"),
                      consumer_secret=os.getenv("OBIT_CONSUMER_SECRET"),
                      access_token_key=os.getenv("OBIT_ACCESS_TOKEN_KEY"),
                      access_token_secret=os.getenv("OBIT_ACCESS_TOKEN_SECRET"))
    api.PostUpdate(text)


def main():
    today = date.today()
    day = today.strftime("%d").strip("0")
    month = today.strftime("%B_")
    url = "https://en.wikipedia.org/wiki/" + month + day

    html = requests.get(url)
    section = scraper.scrape_section(html.text, "Deaths")
    rand_person_line = random.choice(section)
    line_links = rand_person_line.find_all('a')

    person_link = line_links[0]
    if line_links[0].string.isnumeric() and len(line_links) >= 2:
        person_link = line_links[1]

    person_url = "https://en.wikipedia.org" + person_link.get("href")
    print(person_url)

    html = requests.get(person_url)
    first_p = scraper.scrape_first_p(html.text)
    text_without_refs = re.sub(r'\[.*?\]', "", first_p)
    tweet_text = scraper.truncate_to_tweet(text_without_refs)
    print(tweet_text)
    print(len(tweet_text))
    tweet(tweet_text)


if __name__ == "__main__":
    main()
