import requests
from requests import get
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import pandas as pd
import csv

# Declaration des tableaux vides pour le rangement des futures données et la mise en page CSV

product_page_url = []
universal_product_code = []
title = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url = []

# création de la variable page qui contient 1 comme valeur initiale (pour commencer à la première page),
page = 1

#initialisation du tableau dans lequel nous rangeons les titres
titres = []

#initialisation du tableau dans lequel nous rangeons les urls relatives
urlProduits = []

#initialisation du tableau dans lequel nous rangeons les urls absolues apres reconstitution
listeUrlProduitParCategorie = []

# Récupération des titres et des liens
while page != 3: # boucle while pour indiquer le nombre de pages à parcourir
    url = f"http://books.toscrape.com/catalogue/category/books/romance_8/page-{page}.html"  # la variable url contiendra l'URL de la page produit à chaque itération dans un format de chaîne ; utilisation des f-strings qui permettent à {page} de recevoir la valeur actualisée de la page,
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(response.text, 'html.parser')

    for h3 in soup.find_all("h3"):  # je parcours tous les h3 de chaque url pour obtenir les titres
        titres.append(h3.get_text(strip=True)) # puis j'ajoute chaque titre à la liste des titres créée plus haut.
    for titre in titres[:35]: # je parcours tous les titres de la liste
        print(titre)
    for link in soup.select("h3 > a"): # création d'une boucle qui recherche et recupère l'ensemble urls des produits à l'intérieur des balises h3
        urlProduits.append(link.get('href')) # j'aoute ces urls relatives à la liste urlProduits créée plus haut
        #print(link)
    page = page + 1  # augmentation de la valeur de la page de 1 à la fin de chaque itération pour passer à la page suivante.

    #assemblage des urls relatives pour créer des urls absolues
    url1 = "https://books.toscrape.com/catalogue/category/books/romance_8/index.html"
    for i in urlProduits:  # on parcourt les urls relatives ligne à ligne
        totalUrl = (urllib.parse.urljoin(url1, i)) # on assemble les 2 morceaux d'url à l'aide d'urljoin
        print(totalUrl)
        listeUrlProduitParCategorie.append(totalUrl) # récupération des urls absolues dans le tableau listeUrlProduitParCategorie
    print(listeUrlProduitParCategorie)

for urli in listeUrlProduitParCategorie:
    url = urli
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(response.text, 'html.parser')
    baseUrl = "https://books.toscrape.com/"

    # produit description
    description = soup.find("article", class_="product_page").findAll(["p"])

    # récupération des éléments du tableau "table" de la page produit dans une liste
    element = soup.find('table', class_="table table-striped").findAll(["td"])

    # category
    cat = soup.find('ul', class_="breadcrumb").findAll(["li"])

    # product_page_url
    url = url
    print(url)

    # UPC
    UPC = element[0]
    print(UPC.text)

    # title
    titre = soup.find('h1')
    print(titre.text)

    # price_including_tax
    price_incl = element[3]
    print(price_incl.text)

    # price_excluding_tax
    price_excl = element[2]
    print(price_excl.text)

    # number available
    stock = element[5]
    print(stock.text)

    # product_description
    description = description[3]
    print(description.text)

    # category
    catego = cat[2]
    print(catego.text)

    # Review_rating
    review = element[6]
    print(review.text)

    # image_url
    image = soup.find('img')
    print(baseUrl + image["src"])

# ajout des données aux tableaux créés plus haut
    product_page_url.append(url)
    universal_product_code.append(UPC.text)
    title.append(titre.text)
    price_including_tax.append(price_incl.text)
    price_excluding_tax.append(price_excl.text)
    number_available.append(stock.text)
    product_description.append(description.text)
    category.append(catego.text)
    review_rating.append(review.text)
    image_url.append(baseUrl + image["src"].replace("../", ""))

df = pd.DataFrame({'product_page_url':product_page_url, 'universal_product_code':universal_product_code, 'title':title,'price_including_tax':price_including_tax, 'price_excluding_tax':price_excluding_tax,'number_available':number_available, 'product_description':product_description, 'category':category, 'review_rating':review_rating, 'image_url':image_url})
df.to_csv('Categorie.csv', index=False, encoding='UTF-8')

