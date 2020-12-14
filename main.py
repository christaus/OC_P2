#!/usr/bin/env python3
import csv
import os
import shutil
import sys
from dataclasses import dataclass

import bs4
import requests

include_images = False
library = []


@dataclass
class Book:
    # Un livre
    product_page_url: str
    universal_product_code_upc: str
    title: str
    price_including_tax: float
    price_excluding_tax: float
    number_available: int
    product_description: str
    category: str
    review_rating: int
    image_url: str = "https://image.url"


def create_directory(directory):
    # Create a directory
    if os.path.isdir(directory):
        return 1
    else:
        os.mkdir(directory)


def write_csv(nom_fichier="default.csv"):
    # Writing csv file
    global library

    create_directory("csv" + os.sep + library[0][7])

    with open("csv" + os.sep + library[0][7] + os.sep + nom_fichier, "w", newline="") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")
        for livre in library:
            spamwriter.writerow(livre)


class ScrapeIt:
    ''' Class that scrape:
    A. A book if URL matching
    B. A category if URL matching
    C. The whole categories and books if URL matching

    Data will be recorded as csv files.
    '''

    def __init__(self, argv):
        global include_images, library

        # Create directory to store csv files
        create_directory("csv")

        for el in argv[1:]:
            el = el.lower()
            del library[:]

            # Do we need to download images ?
            if "-i" == el or "--images" == el:
                include_images = True
                continue

            # Forced use of https
            if el.startswith("http://"):
                print("Let's use https")
                el = "https://" + el[7:]

            if not el.startswith("https://"):
                print(f"{el} is not a valid URL")
                continue

            if el.startswith("https://books.toscrape.com/catalogue/category/"):
                # Scraping a category
                print("Scraping a category...")
                self.scraping_category(el)
                fichier = library[0][7] + ".csv"
                write_csv(fichier)
                continue
            elif el.startswith("https://books.toscrape.com/catalogue/"):
                # Scraping a book
                print("Scraping a single book...")
                fichier = self.load_book(el) + ".csv"
                write_csv(fichier)
                continue
            elif el == "https://books.toscrape.com/" or el == "https://books.toscrape.com":
                # Scraping the whole site
                print("Scraping the whole site...")
                self.load_site(el)
                continue
            else:
                print(f"Unknown Argument {el}")

    def scraping_category(self, el):
        # Scraping a category
        try:
            requete = requests.request("get", el)
        except BaseException:
            print(f"Cannot load {el}")
            return 1

        if requete.status_code != 200:
            print(f"Error HTML status_code: {requete.status_code} at {el}")
            return 1

        # HTML Parsing
        soup = bs4.BeautifulSoup(requete.text, 'html.parser')

        # Extrait articles data
        to_visit = False
        for article in soup.select("article a"):
            article_page = "https://books.toscrape.com/catalogue/" + \
                           article.attrs.get("href")[9:]
            to_visit = not to_visit
            if to_visit:
                self.load_book(article_page)

        # Go to next page
        for next_page in soup.select(".next a"):
            if next_page:
                next_page = requete.url[:requete.url.rfind(
                    "/")] + "/" + next_page.attrs.get("href")
                self.scraping_category(next_page)

    """def load_images(self):
        # Download images
        global library

        for livre in library:
            print(f"Downloading image {livre.image_url}")"""

    def load_book(self, el):
        # Download a book
        global library
        print(f"Visiting URL: {el}")
        new_book = Book(product_page_url=el,
                        universal_product_code_upc="string",
                        title="string",
                        price_including_tax=11.32,
                        price_excluding_tax=9.43,
                        number_available=16,
                        product_description="string",
                        category="string",
                        review_rating=2
                        )

        try:
            requete = requests.request("get", el)
        except BaseException:
            print(f"Can't load {el}")
            return 1

        if requete.status_code != 200:
            print(f"Error HTML status_code: {requete.status_code} at {el}")
            return 1

        # Parsing HTML
        soup = bs4.BeautifulSoup(requete.text, 'html.parser')

        # Fields extraction
        for element in soup.select(".table-striped"):
            for line in element.select("tr"):
                if line.th.text == "UPC":
                    new_book.universal_product_code_upc = line.td.text
                elif line.th.text == "Price (excl. tax)":
                    new_book.price_excluding_tax = float(line.td.text[2:])
                elif line.th.text == "Price (incl. tax)":
                    new_book.price_including_tax = float(line.td.text[2:])
                elif line.th.text == "Availability":
                    new_book.number_available = int(
                        ''.join(c for c in line.td.text if c.isdigit()))
        new_book.title = soup.select(".product_main h1")[0].text
        new_book.product_description = soup.select(
            "article > p")[0].text.strip(" \n\r")
        new_book.category = soup.select(
            "body > div > div > ul > li > a")[2].text
        stars = str(soup.select(".star-rating")[0])
        offset = stars.find("star-rating")
        stars = stars[offset:offset + 15]
        rating = 0
        if "One" in stars:
            rating = 1
        elif "Two" in stars:
            rating = 2
        elif "Thr" in stars:
            rating = 3
        elif "Fou" in stars:
            rating = 4
        elif "Fiv" in stars:
            rating = 5
        new_book.review_rating = rating
        image_url = str(
            soup.select("article > div > div > div > div > div > div > img")[0])
        image_url = "https://books.toscrape.com/" + \
                    image_url[image_url.find("src=\"") + 11:image_url.find("\"/>")]
        new_book.image_url = image_url

        library.append([new_book.product_page_url,
                        new_book.universal_product_code_upc,
                        new_book.title,
                        new_book.price_including_tax,
                        new_book.price_excluding_tax,
                        new_book.number_available,
                        new_book.product_description,
                        new_book.category,
                        new_book.review_rating,
                        new_book.image_url])

        if include_images:
            # Download image if needed
            create_directory("csv" + os.sep + new_book.category)
            print(f"Downloading image: {new_book.image_url}")
            reponse = requests.get(new_book.image_url, stream=True)
            if reponse.status_code == 200:
                with open("csv" + os.sep + new_book.category + os.sep + new_book.image_url[
                                                                        new_book.image_url.rfind("/") + 1:], 'wb') as f:
                    reponse.raw.decode_content = True
                    shutil.copyfileobj(reponse.raw, f)
        return new_book.title

    def load_site(self, el):
        # Loading site
        print(f"Downloading the whole site: {el}")

        try:
            requete = requests.request("get", el)
        except BaseException:
            print(f"Can't load {el}")
            return 1

        if requete.status_code != 200:
            print(f"Error HTML status_code: {requete.status_code} pour {el}")
            return 1

        # Parsing HTML
        soup = bs4.BeautifulSoup(requete.text, 'html.parser')
        for element in soup.select("aside div ul li ul a"):
            print(element)


if __name__ == '__main__':
    app = ScrapeIt(sys.argv)
