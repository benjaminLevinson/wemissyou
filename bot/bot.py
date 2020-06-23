from datetime import date
from scraper import scraper
import random
import requests
import twitter
import os


def process_date(date_):
    day = date_.strftime("%d").strip("0")
    month = date_.strftime("%B_")
    return month + day


def get_random_date():
    start_dt = date.today().replace(day=1, month=1).toordinal()
    end_dt = date.today().replace(day=31, month=12).toordinal()
    rand_date = date.fromordinal(random.randint(start_dt, end_dt))
    return rand_date


def tweet(text):
    api = twitter.Api(consumer_key=os.getenv("OBIT_CONSUMER_KEY"),
                      consumer_secret=os.getenv("OBIT_CONSUMER_SECRET"),
                      access_token_key=os.getenv("OBIT_ACCESS_TOKEN_KEY"),
                      access_token_secret=os.getenv("OBIT_ACCESS_TOKEN_SECRET"))
    api.PostUpdate(text)


def main():
    day = process_date(date.today())
    url = "https://en.wikipedia.org/wiki/" + day

    html = requests.get(url)
    section = scraper.scrape_section(html.text, "Deaths")
    rand_person = random.choice(section)
    person_link = scraper.scrape_person_line(rand_person)

    person_url = "https://en.wikipedia.org" + person_link
    print(person_url)

    html = requests.get(person_url)
    bio_text = scraper.scrape_bio_text(html.text)
    processed_text = scraper.process_text(bio_text)
    tweet_text = scraper.truncate_to_tweet(processed_text)

    print(tweet_text)
    print(len(tweet_text))
    tweet(tweet_text)


if __name__ == "__main__":
    main()
