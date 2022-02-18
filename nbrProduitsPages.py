import requests
from requests import get
from bs4 import BeautifulSoup
from math import *
import urllib.parse
import urllib.request
import pandas as pd
import csv

url = 'https://books.toscrape.com/catalogue/category/books/romance_8/index.html'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
soupString = str(soup)

#calcul du nombre de pages par catégorie
nbrTotalPage = []
nbrMaxProdPage = 20 #nombre maximum de produits par page
nbrProduit = soup.form.strong.text #recupération du nombre de produits total d'une catégorie dans le code source
nbrProduits = int(nbrProduit) #transformation du contenu de la balise string en int()
totalProduitsPage = nbrProduits / nbrMaxProdPage #division du nombre total de produits de la catégorie par le nombre maximum de produits par page
nbrTotalPage.append(ceil(totalProduitsPage)) # ajout du résultat au tableau nbrTotalPage et utilisation de la fontion d'arrondis supérieur pour obtenir le nombre total de pages d'une catégorie donnée.
print(nbrTotalPage)
