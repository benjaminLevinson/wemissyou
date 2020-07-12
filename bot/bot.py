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


def tweet(text, **kwargs):
    api = twitter.Api(consumer_key=os.getenv("OBIT_CONSUMER_KEY"),
                      consumer_secret=os.getenv("OBIT_CONSUMER_SECRET"),
                      access_token_key=os.getenv("OBIT_ACCESS_TOKEN_KEY"),
                      access_token_secret=os.getenv("OBIT_ACCESS_TOKEN_SECRET"))
    return api.PostUpdate(text, **kwargs)


def main():
    day = process_date(get_random_date())
    url = "https://en.wikipedia.org/wiki/" + day
    print(url)

    html = requests.get(url)
    section = scraper.scrape_section(html.text, "Deaths")
    rand_person_line = random.choice(section)
    person_link = scraper.scrape_bio_link(rand_person_line)

    person_url = "https://en.wikipedia.org" + person_link
    print(person_url)

    html = requests.get(person_url)
    bio_text = scraper.scrape_bio_text(html.text)
    bio_image = scraper.scrape_bio_image(html.text)
    processed_text = scraper.process_text(bio_text)

    gravestone_sentence = scraper.scrape_gravestone(rand_person_line.get_text())
    shortened_bio = scraper.truncate_to_length(processed_text, 280-len(gravestone_sentence)-len('\n\nRIP'))
    tweet_text = gravestone_sentence + shortened_bio + '\n\nRIP'

    print(tweet_text)
    print(len(tweet_text))
    print(bio_image)
    status = tweet(tweet_text, media=bio_image)
    tweet(person_url, in_reply_to_status_id=status.id)


if __name__ == "__main__":
    main()
