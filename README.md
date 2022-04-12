# OpenclassroomsProject
P2-BookToScrape project
Outil de sraping de données en ligne à partir du site Book to Scrape.

#Ce que fait cette application

Récupration des données des livres à partir de books.toscrape.com. Utilisation de ces données pour remplir les fichiers csv par catégorie ainsi que le téléchargement de l'image de couverture du livre.
Les images de couvertures sont enregistrées dans un fichier "Images" et rangées dans des dossier par catégorie.

# Comment l'installer?

Clonez le répertoire/référentiel sur votre ordinateur avec la commande :

git clone https://github.com/CarolinePy/OpenclassroomsProject.git

Assurez-vous d'utiliser python 3.10 Vérifiez votre version de python:
python --version

Créez et activez votre environnement virtuel. 
La méthodologie ci-dessous utilise le module venv mais vous pouvez utiliser votre environnement virtuel préféré à la place.
Création à partir de la racine du projet:
python -m venv <nom-de-votre-environnement-virtuel>

Activation sous Windows:
<votre-nom-env-virtuel>\Scripts\activate.bat

Activation sous Linux et Mac:
source <nom-de-votre-environnement-virtuel>/bin/activate

Installer les dépendances avec pip

pip install -r requirements.txt

# How to use

Lancez le script python main.py

Le système va extraire les catégories du site Book to scrape les inscrire dans des fichiers csv pour chaque catégorie ainsi que l'ensemble des produits de la catégorie concernée.

Patience... votre terminal vous indiquera lorsque votre programme aura terminé son exécution.



Cordialement