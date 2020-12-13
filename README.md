# P2
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
  
C. Récupère toutes les catégories et tous les ouvrages du site http://books.toscrape.com/ vers des fichiers CSV organisés en catégories.

## Installation :  

### Installation générique:    
Python3 dois être installé sur votre système depuis https://www.python.org/  
Il est fortement recommandé d'utiliser un environnement virtuel.  
Pour installer les librairies nécessaires vous n'avez ensuite qu'à taper:  
python -m pip -r requirments.txt  

### Installation sous linux:  
Un fichier Makefile fera le travail pour vous, allez simplement dans
le répertoire du projet puis tapez:  
  
make init  
  
Activer l'environnement virtuel:  
  
source venv/bin/activate  
  
Pour nettoyer le projet:  
  
make clean  
  
## Utilisation :  
  
python main.py *OPTIONS* URL  
  
Le logiciel déterminera si l'URL donnée corresponds à un livre, une
catégorie ou au site entier puis collectera les données en
conséquences (voir les cas d'usages A, B ou C).  
  
### Option :  
-- images / -i pour charger les images
