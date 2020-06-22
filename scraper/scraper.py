from bs4 import BeautifulSoup


# Returns a list of items in section
def scrape_section(html_doc, header):
    soup = BeautifulSoup(html_doc, 'html.parser')
    section_body = soup.find(id=header).parent.find_next_sibling("ul").children
    ls_section_items = list(section_body)

    return [item for item in ls_section_items if item != '\n']


# Apply to a list item from scrape_section(...)
def scrape_link(soup):
    links = soup.split(' – ')
    return links[1]


def scrape_first_p(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    pars = soup.find(id="mw-content-text").find_all("p")

    for par in map(lambda x: x.get_text(), pars):
        if par and len(par.split(' ')) > 3:
            return par


def truncate_to_tweet(p):
    if len(p) <= 280:
        return p

    sentence = p.split('.')
    while len('.'.join(sentence)) > 280:
        sentence = sentence[:len(sentence)-1]
        print(sentence)
    sentence = '.'.join(sentence)
    if len(sentence) == 0:
        raise Exception("Too short")
    return sentence
