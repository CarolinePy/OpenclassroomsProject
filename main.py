import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = 'http://books.toscrape.com/catalogue/you-are-a-badass-how-to-stop-doubting-your-greatness-and-start-living-an-awesome-life_508/index.html'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
baseUrl = "https://books.toscrape.com/"
#produit description
description = soup.find("article", class_="product_page").findAll(["p"])
#print(description)

#récupération des éléments du tableau "table" de la page produit dans une liste
element = soup.find('table', class_="table table-striped").findAll(["td"])
#print(element)

#category
cat = soup.find('ul', class_="breadcrumb").findAll(["li"])
#print(cat)

#Declaration des variables pour la mise en page CSV

product_page_url = []
universal_product_code = []
title = []
price_including_tax = []
price_excluding_tax = []
number_available = []
product_description = []
category = []
review_rating = []
image_url =[]

#product_page_url
url = url
print(url)

#UPC
UPC = element[0]
print(UPC.text)

#title
titre = soup.find('h1')
print(titre.text)

#price_including_tax
price_incl = element[3]
print(price_incl.text)

#price_excluding_tax
price_excl = element[2]
print(price_excl.text)

#number available
stock = element[5]
print(stock.text)

#product_description
description = description[3]
print(description.text)

#category
catego= cat[2]
print(catego.text)

#Review_rating
review = element[6]
print(review.text)

#image_url
image = soup.find('img')
print(baseUrl + image["src"])

product_page_url.append(url)
universal_product_code.append(UPC)
title.append(titre.text)
price_including_tax.append(price_incl.text)
price_excluding_tax.append(price_excl.text)
number_available.append(stock.text)
product_description.append(description.text)
category.append(catego.text)
review_rating.append(review.text)
image_url.append(baseUrl + image["src"].replace("../", ""))

# pandas dataframe
Livre = pd.DataFrame({
    'product_page_url': product_page_url,
    'universal_product_code': UPC,
    'title': title,
    'price_including_tax': price_including_tax,
    'price_excluding_tax' : price_excluding_tax ,
    'number_available': number_available,
    'product_description': product_description,
    'category': category,
    'review_rating': review_rating,
    'image_url': image_url,
})

# add dataframe to csv file named 'Livre.csv'
Livre.to_csv('livre.csv')

