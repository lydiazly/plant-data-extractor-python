# -*- coding: utf-8 -*-
"""
[Python] 3.11
[Pkgs] python-dotenv
"""
import os
from dotenv import load_dotenv

load_dotenv()

CATEGORIES = {
    "NativePerennials": "Native Perennials",
    "NativeGroundcovers": "Native Groundcovers",
    "NativeShrubs": "Native Shrubs",
    "NativeTrees": "Native Trees",
    "NativeWetlandPlants": "Native Wetland Plants",
    "Grasses-Associates": "Grasses & Associates",
    "ChristmasTreeSeedlings": "Christmas Tree Seedlings",
    "Ferns": "Ferns",
    "MiscellaneousGroundcovers": "Miscellaneous Groundcovers",
    "MiscellaneousPlants": "Miscellaneous Plants"
}

SUN_MAPPING = {
    "S": "Sun",
    "PSH": "Partial Shade",
    "SH": "Shade"
}

SOIL_MAPPING = {
    "AC": "Acidic",
    "D": "Dry",
    "AL": "Alkaline (Basic)",
    "H": "Humus",
    "M": "Moist",
    "R": "Rocky",
    "S": "Sandy",
    "W": "Wet",
    "WD": "Well Drained",
    "DT": "Drought Tolerant"
}

HABITAT_MAPPING = {
    "BF": "Bio-filtration",
    "BG": "Bog",
    "DS": "Disturbed Sites",
    "FE": "Forest Edge",
    "GL": "Grassland",
    "GR": "Green Roof",
    "INT": "Interior",
    "MT": "Montane/Alpine",
    "RP": "Riparian",
    "OF": "Open Forest",
    "SF": "Shade Forest",
    "SL": "Shoreline",
    "SM": "Salt Marsh",
    "WL": "Wetland"
}

SIZE_MAPPING = {
    "C": "Container",
    "P": "Plug",
    "LS": "Live Stake",
    "URC": "Un-Rooted Cuttings"
}

COL_NAMES_ORIGINAL = [
    "LATIN",
    "COMMON",
    "SUN",
    "SOIL",
    "HABITAT",
    "SIZES",
    "CATEGORY"
]

COL_NAMES_ALL = [
    "IN_STOCK",
    "LATIN",
    "COMMON",
    "SQUAMISH",
    "HALKOMELEM",
    "FAMILY",
    "CATEGORY",
    "KEYWORDS",
    "MAX_HEIGHT",
    "SUN",
    "SOIL",
    "HABITAT",
    "SIZES",
    "GROWING_EASE",
    "USE_VALUE",
    "ATTRACTS",
    "URL",
    "IMAGE",
    "DESCRIPTION"
]

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
