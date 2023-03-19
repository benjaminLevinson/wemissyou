from datetime import date
from ai import ai
from scraper import scraper
import random
import requests
import twitter
import os

MAX_TOKENS = 4097


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
    api = twitter.Api(
        consumer_key=os.getenv("OBIT_CONSUMER_KEY"),
        consumer_secret=os.getenv("OBIT_CONSUMER_SECRET"),
        access_token_key=os.getenv("OBIT_ACCESS_TOKEN_KEY"),
        access_token_secret=os.getenv("OBIT_ACCESS_TOKEN_SECRET"),
    )
    return api.PostUpdate(text, **kwargs)


obituary_types = [
    "interesting part of obituary in a tweet by leftist twitter account",
    "sarcastic obitaury in a tweet by leftist twitter account",
    "funny obituary in a tweet by leftist twitter account",
    "haiku obituary in a tweet by leftist twitter account",
    "funny limerick obituary in a tweet by leftist twitter account",
    "rude limerick obituary in a tweet by leftist twitter account",
    "poem obituary in a tweet by leftist twitter account",
    "obituary in the style of a tweet by Cormac McCarthy",
    "obituary in the style of a tweet by Jorge Luis Borges",
]


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
    article = scraper.whole_article(html.text)
    bio_image = scraper.scrape_bio_image(html.text)

    length = len(article.split(" "))
    if length > MAX_TOKENS:
        print(length)
        exit(1)

    obituary_type = random.choice(obituary_types)

    identity = "You are a Twitter bot"
    prompt = (
        "Process a person's biography in the following ways:"
        + "First line: [Name] ([short descriptor]). Example: John de Vere (14th Earl of Oxford)"
        + "Second line: [birth year]-[death year] ([age]). Example: 1231-1255 (age 24)"
        + "Third line: blank"
        + f"Fourth line: [{obituary_type}]. Do not include hashtags. Be sure to fit the tweet character limit."
    )
    print(obituary_type)
    result = ai.prompt(identity, prompt, article)
    print(result)
    tweet_text = strip_hashtags(result)
    print(tweet_text)
    print(len(tweet_text))
    status = tweet(tweet_text, media=bio_image)
    tweet(person_url, in_reply_to_status_id=status.id)


if __name__ == "__main__":
    main()


def strip_hashtags(text: str) -> str:
    return text.split("#")[0]
