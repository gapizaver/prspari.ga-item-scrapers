from numpy.core.fromnumeric import prod
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from random import randint, uniform
import json
import time

# prvi in zadnja stran ki jo želimo popraskati
FIRST_PAGE = 1
LAST_PAGE = 1000

# seznam izdelkov
products = []
counter = 0

# praskaj strani znotraj obsega
for page in range(FIRST_PAGE, LAST_PAGE+1):
    print("Praskam stran", page)
    url = "https://www.ceneje.si/Akcije?page=" + str(page)

    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    # najdi vse produkte na strani
    product_div = soup.find_all("div", class_="innerProductBox")

    # spraskaj izdelke s strani
    for div in product_div:
        counter += 1
        product = {
            "id" : randint(100000000, 999999999),
            "title" : "",
            "description" : "",
            "shop_id" : 4847505,
            "shop_item_id" : "",
            "image_url" : "",
        }
        product_attrs = div.div.div.a.img.attrs

        # pridobi id izdelka, sicer preskoči izdelek
        if "id" not in product_attrs:
            continue
        product["shop_item_id"] = product_attrs["id"][3:]

        # pridobi ime izdelka
        if "alt" in product_attrs:
            product["title"] = product_attrs["alt"]

        # pridobi source slike (2 argumenta možna)
        src = ""
        if "src" in product_attrs:
            src = product_attrs["src"]
        elif "data-src" in product_attrs:
            src = product_attrs["data-src"]
        
        # smo pridobili source -> sestavi dejansko pot do slike
        if src != "":
            src_splitted = src.split("/")
            product["image_url"] =  \
                    "https://s3.eu-central-1.amazonaws.com/cnj-img/images/" \
                    + src_splitted[-2] + "/" + src_splitted[-1]
        
        # dodaj izdelek
        products.append(product)
    
    # počakaj trenutek (za razbremenitev strežnika)
    time.sleep(uniform(0.5, 1.0))
    

# na koncu zapiši spraskane izdelke v json datoteko
json_object = json.dumps(products, indent=5, ensure_ascii=False)
with open("cenejesi_izdelki1.json", "w") as outfile:
    outfile.write(json_object)
