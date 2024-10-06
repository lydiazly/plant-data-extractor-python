#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gets data from webpages.
[Out] ./catalogues/catalogue_shop_merged.csv, ./images/*.{png,jpeg}
[Python] 3.11
[Pkgs] requests beautifulsoup4 pandas
"""
# 2024-10-04 created by Lydia
# 2024-10-04 last modified by Lydia
###############################################################################|
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import pandas as pd
import shutil
import os
import time
import random
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import constants as const

pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_rows", 10)
pd.set_option("max_colwidth", 15)

service = Service()
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

output_dir = "./catalogues"
output_file = os.path.join(output_dir, "catalogue_shop_merged.csv")

image_dir = './images'
os.makedirs(image_dir, exist_ok=True)


def clean_url(url):
    return url.split('?')[0]


def preserve_tags(element):
    if element.name in ['br', 'p', 'i', 'b', 'a']:
        text = str(element)
    else:
        text = element.get_text()
    text = re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
    return text


def download_image(image_url, file_name):
    response = requests.get(image_url, stream=True, headers=const.HEADERS)
    if response.status_code == 200:
        with open(file_name, 'wb') as image_file:
            shutil.copyfileobj(response.raw, image_file)


def extract_indigenous_name_prev(soup, target_text):
    target_node = soup.find(string=lambda text: target_text in text.lower())
    name = ""
    if target_node:
        previous_node = target_node.find_previous()
        if previous_node:
            name = previous_node.get_text(strip=True)
            if isinstance(previous_node, NavigableString):
                previous_node.extract()  # Remove text node
            elif isinstance(previous_node, Tag):
                previous_node.decompose()  # Remove Tag
        if isinstance(target_node, NavigableString):
            target_node.extract()  # Remove text node
        elif isinstance(target_node, Tag):
            target_node.decompose()  # Remove Tag
    return name


def extract_indigenous_name_next(soup, target_text):
    target_node = soup.find(string=lambda text: target_text in text.lower())
    name = ""
    if target_node:
        next_node = target_node.find_next()
        if next_node:
            name = next_node.get_text(strip=True)
            if isinstance(next_node, NavigableString):
                next_node.extract()  # Remove text node
            elif isinstance(next_node, Tag):
                next_node.decompose()  # Remove Tag
        if isinstance(target_node, NavigableString):
            target_node.extract()  # Remove text node
        elif isinstance(target_node, Tag):
            target_node.decompose()  # Remove Tag
    return name


def remove_node_prev(soup, target_text):
    target_node = soup.find(string=lambda text: target_text in text.lower())
    name = ""
    if target_node:
        previous_node = target_node.find_previous()
        if previous_node:
            if isinstance(previous_node, NavigableString):
                previous_node.extract()  # Remove text node
            elif isinstance(previous_node, Tag):
                previous_node.decompose()  # Remove Tag
        if isinstance(target_node, NavigableString):
            target_node.extract()  # Remove text node
        elif isinstance(target_node, Tag):
            target_node.decompose()  # Remove Tag
    return name


def remove_node_next(soup, target_text):
    target_node = soup.find(string=lambda text: target_text in text.lower())
    name = ""
    if target_node:
        next_node = target_node.find_next()
        if next_node:
            if isinstance(next_node, NavigableString):
                next_node.extract()  # Remove text node
            elif isinstance(next_node, Tag):
                next_node.decompose()  # Remove Tag
        if isinstance(target_node, NavigableString):
            target_node.extract()  # Remove text node
        elif isinstance(target_node, Tag):
            target_node.decompose()  # Remove Tag
    return name


def extract_description_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    content_lower = content.lower()
    content_lower = content_lower.replace('<strong>)</strong>', ')')  # fix a bug in the source

    squamish = ""
    halkomelem = ""

    if 'sḵwx̱wú7mesh sníchim' in content_lower:
        squamish = extract_indigenous_name_prev(soup, '(sḵwx̱wú7mesh sníchim)')
        if not squamish:
            squamish = extract_indigenous_name_next(soup, 'sḵwx̱wú7mesh sníchim:')

    if 'hen̓q̓əmin̓əm' in content_lower:
        halkomelem = extract_indigenous_name_prev(soup, '(hen̓q̓əmin̓əm)')
        if not halkomelem:
            halkomelem = extract_indigenous_name_next(soup, 'hen̓q̓əmin̓əm:')

    if 'Latin:' in content:
        remove_node_next(soup, 'latin:')

    # cleaned_description = soup.get_text().strip()
    cleaned_description = " ".join(map(preserve_tags, soup))
    cleaned_description = re.sub(r"(<p>\s*</p>)+", "", cleaned_description)
    cleaned_description = re.sub(r"\s*<p>\s*", "", cleaned_description)
    cleaned_description = re.sub(r"\s*</p>\s*", "<br />", cleaned_description)
    cleaned_description = re.sub(r"(\s*<br\s*/?>\s*)+", "<br />", cleaned_description)
    cleaned_description = re.sub(r"^(<br />)", "", cleaned_description)  # remove leading <br/>
    cleaned_description = re.sub(r"(<br />)$", "", cleaned_description)  # remove trailing <br/>

    return squamish, halkomelem, cleaned_description


def scrape_gallery_page(driver, keyword, page_num):
    page_url = const.GALLERY_URLS[keyword].format(page_num=page_num)

    driver.get(page_url)

    # Wait for the grid to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".category-product-content")
        )
    )
    html = driver.page_source

    # with open("tmp.html", 'w') as f:
    #     f.write(html)

    soup = BeautifulSoup(html, 'html.parser')

    # Find all product items
    product_items = soup.find_all(class_='product-group')
    if not product_items:
        return None  # No more items to scrape

    items = []

    for item in product_items:
        # Get names
        title_element = item.find('p', class_='w-product-title')
        full_title = title_element['title']
        common_name = full_title.split('(')[0].strip()
        latin_name = full_title.split('(')[1].replace(')', '').strip()
        print("-----------------------------------------------------")
        print(f"=== {common_name} ({latin_name}) ===")

        # Detail page
        detail_link = item.find('a', class_='product-image__link')['href']
        detail_url = f"{const.BASE_URL}{clean_url(detail_link)}"
        print("Detail URL:", detail_url)

        driver.get(detail_url)
        # Wait for the grid to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".carousel__image")
            )
        )
        html = driver.page_source

        detail_soup = BeautifulSoup(html, 'html.parser')

        # Extract image URL
        image_element = detail_soup.find('div', class_='carousel__image').find('img')
        image_url = clean_url(image_element['src'])
        print("Image URL:", image_url)

        # Download image
        image_file_name = os.path.join(image_dir, f"{common_name.replace(' ', '').split('/')[0]}.{image_url.split('.')[-1]}")
        download_image(image_url, image_file_name)
        print(f"Image saved: {image_file_name}", end='\n\n')

        # Extract description
        description_element = detail_soup.find('div', class_='w-product-description')
        if description_element:
            content = description_element['content']
            squamish, halkomelem, description = extract_description_content(content)
            if squamish:
                print("[Squamish]", squamish)
            if halkomelem:
                print("[Halkomelem]", halkomelem)
            print(description, end='\n\n')
        else:
            squamish, halkomelem, description = "", "", ""

        # Append data to list
        items.append({
            'IN_STOCK': 'true',
            'LATIN': latin_name,
            'COMMON': common_name,
            'SQUAMISH': squamish,
            'HALKOMELEM': halkomelem,
            'KEYWORDS': keyword,
            'DESCRIPTION': description,
            'IMAGE': image_url,
            'LINK': detail_url
        })


        time.sleep(random.uniform(1, 3))

    print(f"[Count] {len(items)}", end='\n\n')
    return items


###############################################################################|
if __name__ == '__main__':
    all_items = []

    driver = webdriver.Chrome(service=service, options=options)
    for keyword in const.GALLERY_URLS.keys():
        page_num = 1
        print("========================================================================")
        print(f"[{keyword}]")
        print(f"Go to page: {const.GALLERY_URLS[keyword]}")
        while page_num < 10:
            print(f"Retrieving page {page_num}...")
            items = scrape_gallery_page(driver, keyword, page_num)
            if not items:
                print('Empty page. Skip.', end='\n\n')
                break
            all_items.extend(items)
            page_num += 1
            print()
    driver.quit()

    df = pd.DataFrame(all_items)

    df.replace("’", "'", regex=True, inplace=True)
    df.replace("‘", "'", regex=True, inplace=True)
    df.replace("\n", "<br />", regex=True, inplace=True)

    df = df.groupby(df.columns.drop('KEYWORDS').tolist(), as_index=False).agg({'KEYWORDS': ', '.join})

    df.to_csv(output_file, index=False)

    print()
    print(df)
    print(f"File saved: {output_file}")