import requests
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
from math import *
import pandas as pd

# initialisation de variables
titres = [] # Tableau dans lequel nous rangeons les titres
urlProduits = [] # tableau dans lequel nous rangeons les urls relatives
listeUrlProduitParCategorie = [] # tableau dans lequel nous rangeons les urls absolues après reconstitution
#nbrTotalPage = []
nbrTotalProduitsCat =[]
listeCategories = [] # Urls relatives de toutes les categories du site
listeUrlCategorie = [] # #Urls absolues de toutes les categories du site
listeUrlCategorieDyn = []
varDynamique = "page-" # initialisation d'une variable  utilisée pour transformer certaines urls en urls dynamiques
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

# Initialisation des variables pour accéder au site et extraire les données
url = 'http://books.toscrape.com'
r = requests.get(url)
soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'html.parser')



# création d'une boucle qui recherche et recupère l'ensemble des urls des catégories du site Book To Scrape
for linkCategorie in soup.find("ul", class_='nav nav-list').ul.findAll("a"):
   listeCategories.append(linkCategorie.get('href'))  # j'ajoute ces urls relatives à la liste listeCategories initialisée plus haut

# Transformation des urls relatives des categories en urls absolues pour pouvoir y accéder
for i in listeCategories:  # Création d'une boucle qui parcourt les urls relatives ligne à ligne du tableau listeCategories
    totalCategorie = (urllib.parse.urljoin(url, i)) # on assemble les 2 morceaux d'url à l'aide d'urljoin
    listeUrlCategorie.append(totalCategorie) # récupération des urls absolues dans le tableau listeUrlProduitParCategorie
print("Merci de patienter pendant l'extraction des catégories du site https://books.toscrape.com/...")
for urlCategorieAbsolue in listeUrlCategorie: # on parcourt les urls absolues du tableau contenant la liste des urls absolues
    url = urlCategorieAbsolue # on indique que la variable url doit prendre comme valeur l'url absolue des categories contenues dans le tableau
    response = requests.get(url)
    html = response.content.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'html.parser')
    page = 1
    # Calcul du nombre total de produits et du nombre total de pages pour chaque categorie
    nbrMaxProdPage = 20  # nombre maximum de produits affichés par page
    nbrProduit = soup.form.strong.text  # extraction du nombre de produits total  dans le code source
    nbrProduits = int(nbrProduit)  # transformation du contenu de la balise string en int()
    totalProduitsPage = nbrProduits / nbrMaxProdPage  # division du nombre total de produits de la catégorie par le nombre maximum de produits par page
    nbrPage = ceil(totalProduitsPage) # utilisation de la fonction ceil() pour un arrondi supérieur afin de ne pas oublier de pages

    if nbrProduits < 20: # instruction conditionnelle indiquant que si une page catégorie possède moins de 20 produits alors...
        url = urlCategorieAbsolue  # la variable url contient l'URL absolue et non dynamique de la catégorie
        response = requests.get(url)
        html = response.content.decode('utf-8', 'ignore')
        soup = BeautifulSoup(html, 'html.parser')
        #print(url)

        for link in soup.select("h3 > a"):  # création d'une boucle qui recherche et recupère l'ensemble urls des produits à l'intérieur des balises h3
            urlProduits.append(link.get('href'))  # j'aoute ces urls relatives à la liste urlProduits initialisée plus haut

    while page != nbrPage + 1: # création d'une boucle qui va itérer jusqu'à atteindre le nombre de pages total pour une categorie donnée.
        if nbrPage > 1: # création instruction conditionnelle pour ne concerner que les catégories possédant plusieurs pages
            urlD = (urllib.parse.urljoin(urlCategorieAbsolue,varDynamique))  # création url dynamique assemble les 2 morceaux d'url à l'aide d'urljoin
            urlDynamique = urlD + f"{page}.html" # utilisation des f-strings qui permettent à {page} de recevoir la valeur actualisée de la page,
            url = urlDynamique  # la variable url contiendra l'URL dynamique de la page
            response = requests.get(url)
            html = response.content.decode('utf-8', 'ignore')
            soup = BeautifulSoup( html, 'html.parser')

            for link in soup.select("h3 > a"):  # création d'une boucle qui recherche et recupère l'ensemble urls des produits à l'intérieur des balises h3
                urlProduits.append(link.get('href'))  # j'aoute ces urls relatives à la liste urlProduits initialisée plus haut


        page = page + 1  # augmentation de la valeur de la page de 1 à la fin de chaque itération pour passer à la page suivante.
print("Opération effectuée.")
print("Veuillez patienter quelques instants, nous récupérons les données pour chaque produit et les écrivons dans un fichier csv:")
def fonction_extraction_donnees_livre(baseUrl, soup, url):
    # produit description
    description = soup.find("article", class_="product_page").findAll(["p"])

    # récupération des éléments du tableau "table" de la page produit dans une liste
    element = soup.find('table', class_="table table-striped").findAll(["td"])

    # category
    cat = soup.find('ul', class_="breadcrumb").findAll(["li"])

    # product_page_url
    url = url
    #print(url)

    # UPC
    UPC = element[0]
    #print(UPC.text)

    # title
    titre = soup.find('h1')
    #print(titre.text)

    # price_including_tax
    price_incl = element[3]
    price_including = price_incl.encode('utf-8', errors='ignore')
    #print(price_incl.text)

    # price_excluding_tax
    price_excl = element[2]
    price_excluding = price_excl.encode('utf-8', errors='ignore')
    #print(price_excl.text)

    # number available
    stock = element[5]
    #print(stock.text)

    # product_description
    description = description[3]
    #print(description.text)

    # category
    catego = cat[2]
    #print(catego.text)

    # Review_rating
    review = element[6]
    #print(review.text)

    # image_url
    image = soup.find('img')
    #print(baseUrl + image["src"])

    return UPC, titre, price_incl, price_excl, stock, description, catego, review, image
def save_to_csv(product_page_url, universal_product_code, title,price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url, tempCategory):
    BookToScrape = pd.DataFrame(
        {'Product_page_url': product_page_url, 'Universal_product_code': universal_product_code, 'Title': title,
         'Price_including_tax': price_including_tax, 'Price_excluding_tax': price_excluding_tax,
         'Number_available': number_available, 'Product_description': product_description, 'category': category,
         'Review_rating': review_rating, 'Image_url': image_url})
    filename = '{0}.csv'.format(tempCategory)
    print(filename)
    BookToScrape.to_csv(filename, index=False, encoding='utf-8')

#assemblage des urls relatives pour créer des urls absolues des produits
url1 = "https://books.toscrape.com/catalogue/category/books/romance_8/index.html"
for i in urlProduits:  # on parcourt les urls relatives ligne à ligne de tous les produits
    totalUrl = (urllib.parse.urljoin(url1, i)) # on assemble les 2 morceaux d'url à l'aide d'urljoin
    #print(totalUrl)
    listeUrlProduitParCategorie.append(totalUrl) # récupération des urls absolues dans le tableau listeUrlProduitParCategorie
    #print(listeUrlProduitParCategorie)
tempCategory = None
for urli in listeUrlProduitParCategorie: # on parcourt les urls absolues des produits dans le tableau
    url = urli # on indique que la variable url doit prendre comme valeur les urls absolues des produits
    response = requests.get(url)
    html = response.content.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html, 'html.parser')
    baseUrl = "https://books.toscrape.com/" # variable pour reconstitution url absolue des images

    UPC, titre, price_including, price_excluding, stock, description, catego, review, image = fonction_extraction_donnees_livre(baseUrl, soup, url)
    format_catego = str(catego.text).strip()

    if not tempCategory: # si tempCategory n'est pas defini ou est vide
        tempCategory = format_catego #Alors on affecte la valeur de la variable catego à la variable tempCategory

    # ajout des données aux tableaux créées plus haut
    if tempCategory != format_catego:
        save_to_csv(product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax,
                    number_available, product_description, category, review_rating, image_url, tempCategory)

        tempCategory = format_catego
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
    product_page_url.append(url)
    universal_product_code.append(UPC.text)
    title.append(titre.text)
    price_including_tax.append(price_including.text)
    price_excluding_tax.append(price_excluding.text)
    number_available.append(stock.text)
    product_description.append(description.text)
    category.append(format_catego)
    review_rating.append(review.text)
    image_url.append(baseUrl + image["src"].replace("../", ""))

save_to_csv(product_page_url, universal_product_code, title,price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url, tempCategory)

print("L'opération s'est bien déroulée. Merci pour votre patience ;-)")


