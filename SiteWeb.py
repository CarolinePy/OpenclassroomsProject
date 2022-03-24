import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
from math import *
import pandas as pd
import os

# initialisation de variables
titres = []  # Tableau dans lequel nous rangeons les titres
liste_categories = []  # Urls relatives de toutes les categories du site
liste_url_categorie = []  # Urls absolues de toutes les categories du site
url_produits = []  # rangement des urls relatives des produits
liste_url_produit_par_categorie = []  # rangement des urls absolues des produits
var_dynamique = "page-"  # initialisation d'une variable pour créer des urls dynamiques

# Declaration des tableaux vides pour le rangement des données et la mise en page CSV

product_page_Url = []
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
    liste_categories.append(
        link_category.get('href'))  # ajout des urls relatives à la liste liste_categories initialisée plus haut

# Transformation des urls relatives des categories en urls absolues pour pouvoir y accéder
for i in liste_categories:  # Création d'une boucle qui parcourt les urls relatives ligne à ligne du tableau liste_categories
    total_categorie = (urllib.parse.urljoin(URL, i))  # on assemble les 2 morceaux d'url à l'aide d'urljoin
    liste_url_categorie.append(total_categorie)  # récupération des urls absolues dans le tableau liste_url_categorie
print("Merci de patienter pendant l'extraction des catégories du site", URL, "...")

for url_categorie_absolue in liste_url_categorie:  # on parcourt les urls absolues du tableau des categories
    url = url_categorie_absolue  # on indique que la variable url doit prendre comme valeur l'url absolue des categories contenues dans le tableau
    response = requests.get(url)
    html = response.content.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'html.parser')
    page = 1
    # Calcul du nombre total de produits et du nombre total de pages pour chaque categorie
    nbr_max_prod_page = 20  # nombre maximum de produits affichés par page
    nbr_produit = soup.form.strong.text  # extraction du nombre de produits total  dans le code source
    nbr_produits = int(nbr_produit)  # transformation du contenu de la balise string en int()
    total_produits_page = nbr_produits / nbr_max_prod_page  # division du nombre total de produits de la catégorie par le nombre maximum de produits par page
    nbr_page = ceil(
        total_produits_page)  # utilisation de la fonction ceil() pour un arrondi supérieur afin de ne pas oublier de pages

    if nbr_produits < 20:  # instruction conditionnelle indiquant que si une page catégorie possède moins de 20 produits alors...
        url = url_categorie_absolue  # la variable url contient l'URL absolue et non dynamique de la catégorie
        response = requests.get(url)
        html = response.content.decode('utf-8', 'ignore')
        soup = BeautifulSoup(html, 'html.parser')

        for link in soup.select(
                "h3 > a"):  # création d'une boucle qui recherche et recupère l'ensemble urls des produits à l'intérieur des balises h3
            url_produits.append(
                link.get('href'))  # j'aoute ces urls relatives à la liste url_produits initialisée plus haut

    while page != nbr_page + 1:  # création d'une boucle qui va itérer jusqu'à atteindre le nombre de pages total pour une categorie donnée.
        if nbr_page > 1:  # création instruction conditionnelle pour ne concerner que les catégories possédant plusieurs pages
            url_dyn = (urllib.parse.urljoin(url_categorie_absolue,
                                            var_dynamique))  # création url dynamique assemble les 2 morceaux d'url à l'aide d'urljoin
            url_dynamique = url_dyn + f"{page}.html"  # utilisation des f-strings qui permettent à {page} de recevoir la valeur actualisée de la page,
            url = url_dynamique  # la variable url contiendra l'URL dynamique de la page
            response = requests.get(url)
            html = response.content.decode('utf-8', 'ignore')
            soup = BeautifulSoup(html, 'html.parser')

            for link in soup.select(
                    "h3 > a"):  # création d'une boucle qui recherche et recupère l'ensemble urls des produits à l'intérieur des balises h3
                url_produits.append(
                    link.get('href'))  # j'aoute ces urls relatives à la liste url_produits initialisée plus haut

        page = page + 1  # augmentation de la valeur de la page de 1 à la fin de chaque itération pour passer à la page suivante.

print("Opération effectuée.")
print("Veuillez patienter pendant la récupération des données produit pour chaque catégorie dans un fichier csv:")

#  Création des fonctions d'extraction des données


def element_extraction(soup):
    # récupération des éléments du tableau "table" de la page produit dans une liste
    element = soup.find('table', class_="table table-striped").findAll(["td"])
    return element

#  UPC
def UPC_extraction(element):
    return element[0]

# price_including_tax
def price_incl_extraction(element):
    return element[3]

# price_excluding_tax
def price_excl_extraction(element):
    return element[2]

# number available
def stock_extraction(element):
    return element[5]

# Review_rating
def review_extraction(element):
    return element[6]

#  product_url
def url_extraction(url):
    return url

# title
def title_extraction(soup):
    return soup.find('h1')

#  descripption
def description_extraction(soup):
    description_soup = soup.find("article", class_="product_page").findAll(["p"])
    return description_soup[3]

#  categorie
def cat_extraction(soup):
    cat = soup.find('ul', class_="breadcrumb").findAll(["li"])
    return cat[2]

# image
def image_extraction(base_url, soup):
    # image_url
    return soup.find('img')


def extraction_donnees_site_web(base_url, soup, url, element):
    return url_extraction(url), UPC_extraction(element), title_extraction(soup), price_incl_extraction(element), price_excl_extraction(element), stock_extraction(element), description_extraction(soup), cat_extraction(soup), review_extraction(element), image_extraction(base_url, soup)

def save_to_csv(product_page_Url, universal_product_code, title, price_including_tax, price_excluding_tax,
                number_available, product_description, category, review_rating, image_url, temp_category):
    book_to_scrape = pd.DataFrame(
        {'Product_page_url': product_page_Url, 'Universal_product_code': universal_product_code, 'Title': title,
         'Price_including_tax': price_including_tax, 'Price_excluding_tax': price_excluding_tax,
         'Number_available': number_available, 'Product_description': product_description, 'category': category,
         'Review_rating': review_rating, 'Image_url': image_url})
    filename = '{0}.csv'.format(temp_category)
    print(filename)
    book_to_scrape.to_csv(filename, index=False, encoding='utf-8')


# assemblage des urls relatives pour créer des urls absolues des produits

for i in url_produits:  # on parcourt les urls relatives ligne à ligne de tous les produits
    total_url = (urllib.parse.urljoin(url_categorie_absolue, i))  # on assemble les 2 morceaux d'url à l'aide d'urljoin
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
    product_page_url, UPC, titre, price_incl, price_excl, stock, description, catego, review, image = extraction_donnees_site_web(base_url, soup, url, element)
    format_catego = str(catego.text).strip()

    if not temp_category:  # si temp_category n'est pas defini ou est vide
        temp_category = format_catego  # Alors on affecte la valeur de la variable catego à la variable temp_category

    # ajout des données aux tableaux créées plus haut
    if temp_category != format_catego:
        save_to_csv(product_page_Url, universal_product_code, title, price_including_tax, price_excluding_tax,
                    number_available, product_description, category, review_rating, image_url, temp_category)

        temp_category = format_catego
        product_page_Url = []
        universal_product_code = []
        title = []
        price_including_tax = []
        price_excluding_tax = []
        number_available = []
        product_description = []
        category = []
        review_rating = []
        image_url = []

    product_page_Url.append(url)
    universal_product_code.append(UPC.text)
    title.append(titre.text)
    price_including_tax.append(price_incl.text)
    price_excluding_tax.append(price_excl.text)
    number_available.append(stock.text)
    product_description.append(description.text)
    category.append(format_catego)
    review_rating.append(review.text)
    image_url.append(base_url + image["src"].replace("../", ""))

    #  Téléchargement et enregistrement des images de chaque produit dans un dossier dédié nommé "images"

    for img in image_url:  #  création d'une boucle pour recupérer les lien url de toutes les images du site
        ROOT_DIRECTORY = "images"  #  création d'une constante pour le nom du dossier qui contient les images
        url = img
        file_name = img.split("/")[-1]  #  les noms des fichiers images ne contiendront que la fin de l'url.
        category_image = format_catego #  création d'une variable qui récupère la nom de la cétégorie de l'image


        def save_image(file_name, url, category_image):  #  création d'une fonction pour récupérer et enregistrer les img
            new_directory = "{0}{1}{2}".format(ROOT_DIRECTORY, os.sep, category_image)  # création d'un répertoire par catégorie
            new_file = "{0}{1}{2}.jpg".format(new_directory, os.sep, file_name)  #  création
            if not os.path.isdir(new_directory):  # Si le répertoire n'existe pas...
                os.makedirs(new_directory, exist_ok=True)  # alors on crée le répertoire de manière récursive

            response = requests.get(url, stream=True)
            f = open(new_file, 'wb')  # nom du fichier + wb (écriture en mode binaire)
            f.write(response.content)
            f.close()

        save_image(file_name, url, category_image)

save_to_csv(product_page_Url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available,
            product_description, category, review_rating, image_url, temp_category)

print("Opération terminée. Merci pour votre patience ;-)")
