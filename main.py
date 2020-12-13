#!/usr/bin/env python3
import csv
import sys
from dataclasses import dataclass
import shutil
import bs4
import requests

include_images = False
bibliotheque = []


@dataclass
class Livre:
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


def ecrire_csv(nom_fichier = "default.csv"):
    # Ecriture du fichier csv
    global bibliotheque

    with open(nom_fichier, "w", newline="") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",")
        for livre in bibliotheque:
            spamwriter.writerow(livre)


class P2:
    def __init__(self, argv):
        global include_images, bibliotheque

        for el in argv[1:]:
            el = el.lower()
            del bibliotheque[:]

            # Doit-on charger les iamges ?
            if "-i" == el or "--images" == el:
                include_images = True
                continue

            # Passage en https
            if el.startswith("http://"):
                # Passage au https, il est grand temps !
                print("Vivons au présent, passage en https")
                el = "https://" + el[7:]

            if not el.startswith("https://"):
                print(f"{el} ne semble pas être une url valide")
                continue

            if el.startswith("https://books.toscrape.com/catalogue/category/"):
                # Téléchargement d'une catégorie
                print("Chargement d'une catégorie")
                self.chargement_categorie(el)
                fichier = bibliotheque[0][7] + ".csv"
                ecrire_csv(fichier)
                continue
            elif el.startswith("https://books.toscrape.com/catalogue/"):
                # Téléchargement d'un livre
                print("Chargement d'un livre")
                fichier = self.chargement_livre(el) + ".csv"
                ecrire_csv(fichier)
                continue
            elif el == "https://books.toscrape.com/" or el == "https://books.toscrape.com":
                # Téléchargement du site entier
                print("Chargement du site entier")
                self.chargement_site(el)
                continue
            else:
                print(f"Argument {el} non reconnu")

    def chargement_categorie(self, el):
        # Chargement d'une catégorie
        try:
            requete = requests.request("get", el)
        except:
            print(f"Ne peux pas traiter {el}")
            return 1

        if requete.status_code != 200:
            print(f"Erreur HTML status_code: {requete.status_code} pour {el}")
            return 1

        # Parse HTML
        soup = bs4.BeautifulSoup(requete.text, 'html.parser')

        # Extrait les données des articles un par un
        a_visiter = False
        for article in soup.select("article a"):
            page_article = "https://books.toscrape.com/catalogue/" + article.attrs.get("href")[9:]
            a_visiter = not a_visiter
            if a_visiter:
                self.chargement_livre(page_article)

        # Passe à la page suivante
        for suivante in soup.select(".next a"):
            if suivante:
                suivante = requete.url[:requete.url.rfind("/")] + "/" + suivante.attrs.get("href")
                self.chargement_categorie(suivante)

    def chargement_images(self):
        # Chargement des images
        global bibliotheque

        for livre in bibliotheque:
            print(f"Chargement de l'image {livre.image_url}")

    def chargement_livre(self, el):
        # Chargement d'un livre
        global bibliotheque
        print(f"Visite de l'URL: {el}")
        nouveau_livre = Livre(product_page_url=el,
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
        except:
            print(f"Ne peux pas traiter {el}")
            return 1

        if requete.status_code != 200:
            print(f"Erreur HTML status_code: {requete.status_code} pour {el}")
            return 1

        # Parse HTML
        soup = bs4.BeautifulSoup(requete.text, 'html.parser')

        # Extraction des champs
        for element in soup.select(".table-striped"):
            for ligne in element.select("tr"):
                if ligne.th.text == "UPC":
                    nouveau_livre.universal_product_code_upc = ligne.td.text
                elif ligne.th.text == "Price (excl. tax)":
                    nouveau_livre.price_excluding_tax = float(ligne.td.text[2:])
                elif ligne.th.text == "Price (incl. tax)":
                    nouveau_livre.price_including_tax = float(ligne.td.text[2:])
                elif ligne.th.text == "Availability":
                    nouveau_livre.number_available = int(''.join(c for c in ligne.td.text if c.isdigit()))
        nouveau_livre.title = soup.select(".product_main h1")[0].text
        nouveau_livre.product_description = soup.select("article > p")[0].text.strip(" \n\r")
        nouveau_livre.category = soup.select("body > div > div > ul > li > a")[2].text
        nombre_etoiles = str(soup.select(".star-rating")[0])
        position = nombre_etoiles.find("star-rating")
        nombre_etoiles = nombre_etoiles[position:position + 15]
        etoiles = 0
        if "One" in nombre_etoiles:
            etoiles = 1
        elif "Two" in nombre_etoiles:
            etoiles = 2
        elif "Thr" in nombre_etoiles:
            etoiles = 3
        elif "Fou" in nombre_etoiles:
            etoiles = 4
        elif "Fiv" in nombre_etoiles:
            etoiles = 5
        nouveau_livre.review_rating = etoiles
        image_url = str(soup.select("article > div > div > div > div > div > div > img")[0])
        image_url = "https://books.toscrape.com/" + image_url[image_url.find("src=\"")+11:image_url.find("\"/>")]
        nouveau_livre.image_url = image_url

        bibliotheque.append([nouveau_livre.product_page_url,
                             nouveau_livre.universal_product_code_upc,
                             nouveau_livre.title,
                             nouveau_livre.price_including_tax,
                             nouveau_livre.price_excluding_tax,
                             nouveau_livre.number_available,
                             nouveau_livre.product_description,
                             nouveau_livre.category,
                             nouveau_livre.review_rating,
                             nouveau_livre.image_url])

        if include_images:
            # Recupère l'image
            print(f"Chargement de l'image: {nouveau_livre.image_url}")
            reponse = requests.get(nouveau_livre.image_url, stream=True)
            if reponse.status_code == 200:
                with open(nouveau_livre.image_url[nouveau_livre.image_url.rfind("/")+1:], 'wb') as f:
                    reponse.raw.decode_content = True
                    shutil.copyfileobj(reponse.raw, f)
        return nouveau_livre.title

    def chargement_site(self, el):
        # Chargement du site entier
        print(f"Récupération du site entier: {el}")

        try:
            requete = requests.request("get", el)
        except:
            print(f"Ne peux pas traiter {el}")
            return 1

        if requete.status_code != 200:
            print(f"Erreur HTML status_code: {requete.status_code} pour {el}")
            return 1

        # Parse HTML
        soup = bs4.BeautifulSoup(requete.text, 'html.parser')
        for element in soup.select("aside div ul li ul a"):
            print(element)


if __name__ == '__main__':
    app = P2(sys.argv)
