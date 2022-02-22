import requests
from requests import get
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
from math import *
import pandas as pd
import csv

#initialisation du tableau dans lequel nous rangeons les titres
titres = []
#initialisation du tableau dans lequel nous rangeons les urls relatives
urlProduits = []

#initialisation du tableau dans lequel nous rangeons les urls absolues apres reconstitution
listeUrlProduitParCategorie = []

nbrTotalPage = []
nbrTotalProduitsCat =[]
#recupération de l'ensemble des catégories du site dans une liste

#initialisation de variable
listeCategories = []
listeUrlCategorie = []
listeUrlCategorieDyn = []
url = 'http://books.toscrape.com'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
baseUrl = "https://books.toscrape.com/"

# Declaration des tableaux vides pour le rangement des futures données et la mise en page CSV

category = []

for linkcategorie in soup.find("ul", class_='nav nav-list').ul.findAll("a"):  # création d'une boucle qui recherche et recupère l'ensemble urls des produits à l'intérieur des balises h3
   listeCategories.append(linkcategorie.get('href'))  # j'aoute ces urls relatives à la liste urlProduits créée plus haut
   #print(listeCategories)
#assemblage des urls relatives pour créer des urls absolues
urlIndex = "https://books.toscrape.com/index.html"
for i in listeCategories:  # on parcourt les urls relatives ligne à ligne
    totalCategorie = (urllib.parse.urljoin(urlIndex, i)) # on assemble les 2 morceaux d'url à l'aide d'urljoin
    #print(totalCategorie)
    listeUrlCategorie.append(totalCategorie) # récupération des urls absolues dans le tableau listeUrlProduitParCategorie
#print(listeUrlCategorie)
page = 1
varDynamique = "page-"

for urlCategorieI in listeUrlCategorie: # on parcourt les urls absolues du tableau contenant la liste des urls absolues
    url = urlCategorieI # on indique que la variable url doit prendre comme valeur une url absolue contenue dans le tableau
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(response.text, 'html.parser')
    baseUrl = "https://books.toscrape.com/"
    #print(urlCategorieI)

    # listing du nombre total de produit pour chaque categorie et du nombre total de pages par catégorie
    nbrMaxProdPage = 20  # nombre maximum de produits par page
    nbrProduit = soup.form.strong.text  # recupération du nombre de produits total d'une catégorie dans le code source
    nbrProduits = int(nbrProduit)  # transformation du contenu de la balise string en int()
    totalProduitsPage = nbrProduits / nbrMaxProdPage  # division du nombre total de produits de la catégorie par le nombre maximum de produits par page
    nbrPage = ceil(totalProduitsPage)
    #nbrPages = (f"{nbrPage}")

    if nbrPage > 1:
        urlD = (urllib.parse.urljoin(urlCategorieI, varDynamique))  # on assemble les 2 morceaux d'url à l'aide d'urljoin
        urlDynamique = urlD + f"{page}.html"
        print(urlDynamique)
        print(nbrPage)
        listeUrlCategorieDyn.append(urlDynamique)
        for h3 in soup.find_all("h3"):  # je parcours tous les h3 de chaque url pour obtenir les titres
            titres.append(h3.get_text(strip=True))  # puis j'ajoute chaque titre à la liste des titres créée plus haut.
        for titre in titres[:nbrProduits]:  # je parcours tous les titres de la liste
            print(titre)


"""page = 1
    while page != nbrPageDyn:
        url = urlDynamique  # la variable url contiendra l'URL de la page produit à chaque itération dans un format de chaîne ; utilisation des f-strings qui permettent à {page} de recevoir la valeur actualisée de la page,
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(response.text, 'html.parser')

    page = page + 1  # augmentation de la valeur de la page de 1 à la fin de chaque itération pour passer à la page suivante.
"""