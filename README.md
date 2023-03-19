## Wikipedia Obituary Twitter Bot
This Twitter bot tweets obituaries for notable people who died
on this day in history. The bot works by scraping the "Deaths"
section of a Wikipedia entry for a day. For example, Wikipedia
has a section for notable deaths on June 21st of any year at 
https://en.wikipedia.org/wiki/June_21#Deaths.

The bot can be found at https://twitter.com/obituary_bot.

## Setup
Checkout this package and navigate to the root code directory.
To setup the virtual environment and install dependencies, run:
```
python -m venv venv
make init
```
Add a file to the root directory called keys.env with the following
contents to export the Twitter keys corresponding to your app:
```
export OBIT_CONSUMER_KEY=[your consumer key]
export OBIT_CONSUMER_SECRET=[your consumer secret]
export OBIT_ACCESS_TOKEN_KEY=[your access token key]
export OBIT_ACCESS_TOKEN_SECRET=[your access token secret]
export OPENAI_API_KEY=[your open AI secret]
```
Now, if you run `tweet.sh` your bot should send out its first
Tweet! To truly automate your bot, setup a cron job to execute
`tweet.sh` on a regular schedule.