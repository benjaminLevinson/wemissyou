import unittest
import requests
from scraper import scraper


class ScrapeBioText(unittest.TestCase):
    def test_without_infobox(self):
        test_cases = [
            {
                "name": "no infobox",
                "person_url": "https://en.wikipedia.org/wiki/Leo_Passianos",
                "expected_tweet": "Leo Passianos (died 22 June 1017) was the Byzantine general sent by the Catapan of "
                                  "Italy Leo Tornikios Kontoleon to fight the Lombard rebel Melus of Bari in 1017",
            },
            {
                "name": "infobox",
                "person_url": "https://en.wikipedia.org/wiki/Jacqueline_Audry",
                "expected_tweet": "Jacqueline Audry (September 25, 1908 – June 22, 1977) was a French film director "
                                  "who began making films in post-World War II France and specialised in literary "
                                  "adaptations.[1] She was the first commercially successful female director of "
                                  "post-war France"
            },
            {
                "name": "advanced infobox",
                "person_url": "https://en.wikipedia.org/wiki/Saints_Cyril_and_Methodius",
                "expected_tweet": "Cyril (born Constantine, 826–869) and Methodius (815–885) were two brothers and "
                                  "Byzantine Christian theologians and missionaries. For their work evangelizing the "
                                  "Slavs, they are known as the \"Apostles to the Slavs\""
            },
        ]

        for test_case in test_cases:
            html = requests.get(test_case["person_url"])
            bio_text = scraper.scrape_bio_text(html.text)
            tweet_text = scraper.truncate_to_tweet(bio_text)
            self.assertEqual(test_case["expected_tweet"], tweet_text, test_case["name"])


if __name__ == '__main__':
    unittest.main()
