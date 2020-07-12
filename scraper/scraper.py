import requests
from bs4 import BeautifulSoup
import re


# Returns a list of items in a Wikipedia section
def scrape_section(html_doc, header):
    soup = BeautifulSoup(html_doc, 'html.parser')
    section_body = soup.find(id=header).parent.find_next_sibling("ul").children
    ls_section_items = list(section_body)

    return [item for item in ls_section_items if item != '\n']


# Scrape line for person who died
# example formatting:
#    <a href="...">1208</a> – <a href="...">Philip of Swabia</a> (b. 1177)
def scrape_bio_link(person_line):
    links = person_line.find_all('a')

    # If year is a link (like above), get the 2nd link
    if links[0].string.isnumeric() and len(links) >= 2:
        person_link = links[1]
    else:
        person_link = links[0]

    return person_link.get("href")


# Extract info from item list returned by scrape_section. Return info as "gravestone" string
# Example line:
#    1775 – Karl Ludwig von Pöllnitz, German adventurer and author (b. 1692)
def scrape_gravestone(person_line):
    # Separate death year and rest of sentence
    death_year, remaining_sentence = person_line.split(' – ')
    # Separate full name and rest of sentence
    comma_split = remaining_sentence.split(', ')
    if remaining_sentence != comma_split[0]:
        full_name, remaining_sentence = comma_split[0], ', '.join(comma_split[1:])
    else:
        epithet_name, remaining_sentence = remaining_sentence.split(' (b. ')
        birth_year = remaining_sentence.strip(')')
        age = str(int(death_year) - int(birth_year))
        gravestone = \
            epithet_name + ', ' + age + '\n' + \
            birth_year + '—' + death_year + '\n\n'
        return gravestone

    # Extract birth year and epithet
    matches = re.match(r'(?P<epithet>.*)\(\D*(?P<birth_year>\d*)\)', remaining_sentence)
    if matches:
        epithet = matches.group("epithet").strip()
        birth_year = matches.group("birth_year").strip()
        age = str(int(death_year) - int(birth_year))
        gravestone = \
            full_name + ', ' + age + ' (' + epithet + ')' '\n' + \
            birth_year + '—' + death_year + '\n\n'
    else:
        epithet = remaining_sentence.strip()
        gravestone = \
            full_name + ' (' + epithet + ')' '\n' + \
            "?-" + death_year + '\n\n'

    return gravestone


def scrape_bio_image(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    infobox = soup.find(class_="infobox")
    if not infobox:
        return ""
    img_link_tag = infobox.find("a", class_="image")
    if img_link_tag:
        return scrape_hq_image("https://en.wikipedia.org" + img_link_tag.get("href"))

    img_tag = infobox.find("img")
    if not img_tag:
        return ""
    img_src = "https:" + img_tag.get("src")
    return img_src


# Scrape high-quality image from image file page
def scrape_hq_image(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    file_div = soup.find(id="file")
    if not file_div:
        return ""
    image_link_tag = file_div.find("a")
    if not image_link_tag:
        return ""
    return "https:" + image_link_tag.get("href")


def scrape_bio_text(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    infobox = soup.find(class_="infobox")
    if infobox:
        pars = infobox.find_next_siblings("p")
    else:
        # No infobox
        print("No infobox found!")
        pars = soup.find(id="mw-content-text").find_all("p")

    pars_text = map(lambda x: x.get_text(), pars)
    # Remove singleton newline strings
    pars_no_newlines = [sentence for sentence in pars_text if sentence != '\n']
    # Strip whitespace
    pars_stripped = list(map(lambda x: x.strip(), pars_no_newlines))

    return ' '.join(pars_stripped)


def process_text(text):
    # Remove references example: [1]
    text_no_references = re.sub(r'\[.*?\]', "", text)
    # Remove prompts to listen to pronunciation and possibly some preceding data
    # text_no_listen_prompt = re.sub(r'\(.*listen[;) ]+', "(", text_no_references)
    # Remove parentheticals example: (1994-2014)
    text_no_parentheticals = re.sub(r'\s\(.*?\)', "", text_no_references)

    return text_no_parentheticals


# Drops sentences in a paragraph until paragraph is tweet length
def truncate_to_length(p, length):
    if length < 0:
        raise Exception("Negative truncation length")

    if len(p) <= length:
        return p

    sentence = p.split('.')
    while len('.'.join(sentence)) > length:
        sentence = sentence[:-1]
    sentence = '.'.join(sentence)

    # First sentence was larger than LENGTH characters
    if len(sentence) == 0:
        raise Exception("Too short")

    return sentence
