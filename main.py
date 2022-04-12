import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
from math import *
import pandas as pd
import os
from datetime import datetime

start_date = datetime.now()

# initialisation de variables
titres = []  # Tableau dans lequel nous rangeons les titres
liste_url_categorie = []  # Urls absolues de toutes les categories du site
url_produits = []  # rangement des urls relatives des produits
liste_url_produit_par_categorie = []  # rangement des urls absolues des produits
var_dynamique = "page-"  # initialisation d'une variable pour créer des urls dynamiques

# Declaration des tableaux vides pour le rangement des données et la mise en page CSV

product_pages_url = []
universal_product_code = []
title = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url = []

# Initialisation des variables pour accéder au site et extraire les données
URL = 'https://books.toscrape.com'
r = requests.get(URL)
soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'html.parser')

# création d'une boucle qui recupère l'ensemble des urls des catégories du site
for link_category in soup.find("ul", class_='nav nav-list').ul.findAll("a"):
    total_categorie = (urllib.parse.urljoin(URL, link_category.get('href')))  # on assemble les 2 morceaux d'url à l'aide d'urljoin
    liste_url_categorie.append(total_categorie)  # récupération des urls absolues dans le tableau liste_url_categorie

print("Merci de patienter nous procédons à l'extraction des catégories du site", URL, "...")

for url_categorie_absolue in liste_url_categorie:  # on parcourt les urls absolues du tableau des categories
    url = url_categorie_absolue  # on indique que la variable url doit prendre comme valeur l'url absolue des categories
    response = requests.get(url)
    html = response.content.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'html.parser')
    page = 1
    # Calcul du nombre total de produits et du nombre total de pages pour chaque categorie
    nbr_max_prod_page = 20  # nombre maximum de produits affichés par page
    nbr_produit = soup.form.strong.text  # extraction du nombre de produits total  dans le code source
    nbr_produits = int(nbr_produit)  # transformation du contenu de la balise string en int()
    total_produits_page = nbr_produits / nbr_max_prod_page  # nbr total de produits categorie / nbr de produits par page
    nbr_page = ceil(
        total_produits_page)  # utilisation de la fonction ceil() pour un arrondi supérieur et avoir le bon nbr de pages

    if nbr_produits < 20:  # condition indiquant que si une page catégorie possède moins de 20 produits alors...
        url = url_categorie_absolue  # la variable url contient l'URL absolue et non dynamique de la catégorie
        response = requests.get(url)
        html = response.content.decode('utf-8', 'ignore')
        soup = BeautifulSoup(html, 'html.parser')

        for link in soup.select(
                "h3 > a"):  # Boucle qui recherche et recupère les urls des produits à l'intérieur des balises h3
            url_produits.append(
                link.get('href'))  # Ajout  de ces urls relatives à la liste url_produits initialisée plus haut

    while page != nbr_page + 1:  # boucle qui itère jusqu'à atteindre le nombre de pages total pour une categorie donnée
        if nbr_page > 1:  # Condition créée pour les catégories possédant plusieurs pages
            url_dyn = (urllib.parse.urljoin(url_categorie_absolue,
                                            var_dynamique))  # création  d'une url dynamique à l'aide d'urljoin
            url_dynamique = url_dyn + f"{page}.html"  # utilisation des f-strings pour actualiser la valeur de {page}
            url = url_dynamique  # la variable url contiendra l'URL dynamique de la page
            response = requests.get(url)
            html = response.content.decode('utf-8', 'ignore')
            soup = BeautifulSoup(html, 'html.parser')

            for link in soup.select(
                    "h3 > a"):  # Boucle qui recupère l'ensemble des urls des produits à l'intérieur des balises h3
                url_produits.append(
                    link.get('href'))  # j'aoute ces urls relatives à la liste url_produits initialisée plus haut

        page = page + 1  # augmentation de 1 à la fin de chaque itération pour passer à la page suivante.

print("Opération effectuée.")
print("Veuillez patienter pendant la récupération des données produit et des images pour chaque catégorie :")

#  Création des fonctions d'extraction des données

# Extraction des éléments du tableau de la page produit regroupant une partie des informations à récupérer.


def element_extraction(soup):
    # récupération des éléments du tableau "table" de la page produit dans une liste
    element = soup.find('table', class_="table table-striped").findAll(["td"])
    return element


# Extraction product_page_url


def url_extraction(url):
    return url


# Extraction UPC (universal_product_code)


def upc_extraction(element):
    return element[0]


# Extraction titre


def title_extraction(soup):
    return soup.find('h1')


# Extraction price_including_tax


def price_incl_extraction(element):
    return element[3]

# Extraction price_excluding_tax


def price_excl_extraction(element):
    return element[2]

# Extraction number available


def stock_extraction(element):
    return element[5]


#  Extraction description


def description_extraction(soup):
    description_soup = soup.find("article", class_="product_page").findAll(["p"])
    return description_soup[3]


#  Extraction catégorie


def cat_extraction(soup):
    cat = soup.find('ul', class_="breadcrumb").findAll(["li"])
    return cat[2]


# Extraction Review_rating


def review_extraction(element):
    return element[6]


# Extraction image


def image_extraction(soup):
    # image_url
    return soup.find('img')


def extraction_donnees_site_web(base_url, soup, url, element):
    return url_extraction(url), upc_extraction(element), title_extraction(soup), price_incl_extraction(element),\
           price_excl_extraction(element), stock_extraction(element), description_extraction(soup),\
           cat_extraction(soup), review_extraction(element), image_extraction(soup)

ROOT_DIRECTORY_CSV = "csv"


def save_to_csv(product_pages_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                number_available, product_description, category, review_rating, image_url, temp_category):
    book_to_scrape = pd.DataFrame(
        {'Product_page_url': product_pages_url, 'Universal_product_code': universal_product_code, 'Title': title,
         'Price_including_tax': price_including_tax, 'Price_excluding_tax': price_excluding_tax,
         'Number_available': number_available, 'Product_description': product_description, 'category': category,
         'Review_rating': review_rating, 'Image_url': image_url})
    filename = '{0}{1}{2}.csv'.format(ROOT_DIRECTORY_CSV, os.sep, temp_category)
    if not os.path.isdir(ROOT_DIRECTORY_CSV):  # Si le répertoire n'existe pas...
        os.makedirs(ROOT_DIRECTORY_CSV, exist_ok=True)  # alors on crée le répertoire de manière récursive
    print(filename)
    book_to_scrape.to_csv(filename, index=False, encoding='utf-8')

# Récupération des images


ROOT_DIRECTORY = "Images"  # création de la constante ROOt-Directory "images" pour la création du dossier de rangement


def save_image(file_name, url, category_image):  # création d'une fonction pour récupérer et enregistrer les img
    file_name = str(file_name).replace('/', '-')
    new_directory = "{0}{1}{2}".format(ROOT_DIRECTORY, os.sep, category_image)  # création d'un répertoire par catégorie
    new_file = "{0}{1}{2}.jpg".format(new_directory, os.sep, file_name)  # création
    if not os.path.isdir(new_directory):  # Si le répertoire n'existe pas...
        os.makedirs(new_directory, exist_ok=True)  # alors on crée le nouveau répertoire de manière récursive

    response = requests.get(url, stream=True)
    f = open(new_file, 'wb')  # nom du fichier + wb (écriture en mode binaire)
    f.write(response.content)
    f.close()


# assemblage des urls relatives pour créer des urls absolues des produits
URL_CATEGORIE_ABSOLUE = "https://books.toscrape.com/catalogue/"
for i in url_produits:  # on parcourt les urls relatives ligne à ligne de tous les produits
    total_url = "{0}{1}".format(URL_CATEGORIE_ABSOLUE, i.replace("../../../", ""))
    liste_url_produit_par_categorie.append(
        total_url)  # récupération des urls absolues dans le tableau liste_url_produit_par_categorie

temp_category = None
for urli in liste_url_produit_par_categorie:  # on parcourt les urls absolues des produits dans le tableau
    url = urli  # on indique que la variable url doit prendre comme valeur les urls absolues des produits
    response = requests.get(url)
    html = response.content.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'html.parser')
    base_url = "https://books.toscrape.com/"  # variable pour reconstitution url absolue des images

    element = element_extraction(soup)
    product_page_url, upc, titre, price_incl, price_excl, stock, description, catego, review, image = \
        extraction_donnees_site_web(base_url, soup, url, element)
    format_catego = str(catego.text).strip()
    lien_url_images = base_url + image["src"].replace("../", "")
    save_image(titre.text, lien_url_images, format_catego)  # appel de la fonction save_image pour chaque produit
    if not temp_category:  # si temp_category n'est pas defini ou est vide
        temp_category = format_catego  # Alors on affecte la valeur de la variable catego à la variable temp_category

    # ajout des données aux tableaux créées plus haut
    if temp_category != format_catego:
        save_to_csv(product_pages_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                    number_available, product_description, category, review_rating, image_url, temp_category)

        temp_category = format_catego
        product_pages_url = []
        universal_product_code = []
        title = []
        price_including_tax = []
        price_excluding_tax = []
        number_available = []
        product_description = []
        category = []
        review_rating = []
        image_url = []

    product_pages_url.append(url)
    universal_product_code.append(upc.text)
    title.append(titre.text)
    price_including_tax.append(price_incl.text)
    price_excluding_tax.append(price_excl.text)
    number_available.append(stock.text)
    product_description.append(description.text)
    category.append(format_catego)
    review_rating.append(review.text)
    image_url.append(lien_url_images)


save_to_csv(product_pages_url, universal_product_code, title, price_including_tax, price_excluding_tax,
            number_available, product_description, category, review_rating, image_url, temp_category)

print("Opération terminée. Toutes les données et images ont été extraites. Merci pour votre patience ;-)")

end_date = datetime.now()
print("le programme s'est exécuté en", end_date - start_date)
