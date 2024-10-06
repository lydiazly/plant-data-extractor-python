# -*- coding: utf-8 -*-
# config/config.py
"""
[Python] 3.11
[Pkgs] python-dotenv
"""
import os
from dotenv import load_dotenv

load_dotenv()

PDF_PREFIX = "../data/NATS-Nursery-Ltd-Catalogue-2019"  # {PDF_PREFIX}_{category}.pdf

CATALOG_DIR = "./catalogues"
IMAGE_DIR = './images'

CATALOG_FILE_NATS = os.path.join(CATALOG_DIR, "catalogue_nats_merged.csv")
CATALOG_FILE_SHOP = os.path.join(CATALOG_DIR, "catalogue_shop_merged.csv")

BASE_URL = os.getenv('BASE_URL')

GALLERY_URLS = {
    "Perennial/Annual": BASE_URL + "/shop/perennialannual/22?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Shrubs": BASE_URL + "/shop/shrubs/23?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Native Trees": BASE_URL + "/shop/native-trees/21?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Ferns": BASE_URL + "/shop/ferns/18?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Grasses": BASE_URL + "/shop/grasses/24?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Sun-loving": BASE_URL + "/shop/sun-loving-plants/28?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Shade-friendly": BASE_URL + "/shop/shade-plants/29?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Groundcover": BASE_URL + "/shop/groundcover-plants/32?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Edible": BASE_URL + "/shop/edible/26?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Medicinal": BASE_URL + "/shop/medicinal/27?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Hummingbirds": BASE_URL + "/shop/hummingbirds/33?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Bird Food - Berries": BASE_URL + "/shop/bird-food-berries/34?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Bird Food - Seeds": BASE_URL + "/shop/bird-food-dry-seeds/35?page={page_num}&limit=180&sort_by=name&sort_order=asc",
    "Seeds": BASE_URL + "/shop/seeds/14?page={page_num}&limit=180&sort_by=name&sort_order=asc"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}
