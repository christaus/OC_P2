*French version follows*

# P2 - ScrapeIt

Prices extraction software  

## This is :

A scraping software for extracting data from an online library :  

- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

## Usage cases :  

A. Get a single book datas from the website http://books.toscrape.com/ .  
  
B. Get all books datas from a specific category of http://books.toscrape.com/ .  
  
C. Get all datas from every categories and books from http://books.toscrape.com/ .  
  
Data will be stored in csv/category/category.csv files. Images will be
included or not.  
  
## Install :  
  
### Generic install :  
  
Python3 must be installed on your operating system. You can get it from https://www.python.org/ .
Consider installing and use a virtualenv, not your main python install.  
To install the needed libs, just use :  
python -m pop -r requirments.txt  
  
### Linux install :  
  
A Makefile will do the work for you, just go on the application directory and use :  
  
make init  
  
To activate the virtualenv :  
  
source venv/bin/activate  
  
To clean the project :  
  
make clean  
  
## Use :  
  
python main.py *OPTIONS* URL  
  
The software will guess if the given URL is one for a book, a category or the whole website.  
  
### Option :  
  
-- images / -i before the url to download images.  
  
# P2 - ScrapeIt  
  
Programme d'extraction des prix  
  
## Descriptif :  
  
Extraire les données suivantes:  
  
- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url
  
## Cas d'usage:  
  
A. Récupère une page (un ouvrage) du site http://books.toscrape.com/ vers un fichier CSV.  
  
B. Récupère tous les ouvrages d'une catégorie du site http://books.toscrape.com/ vers un fichier CSV.  
  
C. Récupère toutes les catégories et tous les ouvrages du site http://books.toscrape.com/ vers des fichiers CSV
organisés en catégories.  
  
## Installation :  
  
### Installation générique:  
  
Python3 dois être installé sur votre système depuis https://www.python.org/    
Il est fortement recommandé d'utiliser un environnement virtuel.  
Pour installer les librairies nécessaires vous n'avez ensuite qu'à taper:    
  
python -m pip -r requirments.txt  
  
### Installation sous linux:  
  
Un fichier Makefile fera le travail pour vous, allez simplement dans le répertoire du projet puis tapez:  
  
make init  
  
Activer l'environnement virtuel:  
  
source venv/bin/activate  
  
Pour nettoyer le projet:  
  
make clean  
  
## Utilisation :  
  
python main.py *OPTIONS* URL  
  
Le logiciel déterminera si l'URL donnée corresponds à un livre, une catégorie ou au site entier puis collectera les
données en conséquences (voir les cas d'usages A, B ou C).  
  
### Option :  
  
-- images / -i pour charger les images  
  