#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gets data from webpages.
[Out] ./catalogues/catalogue_shop_merged.csv, ./images/*.{png,jpeg}
[Python] 3.11
[Pkgs] requests beautifulsoup4 pandas selenium
"""
# 2024-10-04 created by Lydia
# 2024-10-06 last modified by Lydia
###############################################################################|
import requests
from bs4 import BeautifulSoup, Tag, NavigableString
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
from selenium.common.exceptions import TimeoutException

from config import columns, config, corrections

pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_rows", 10)
pd.set_option("max_colwidth", 15)

service = Service(os.path.expanduser('~/chromedriver/chromedriver'))
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")

output_dir = config.CATALOG_DIR
output_file = config.CATALOG_FILE_SHOP

image_dir = config.IMAGE_DIR
os.makedirs(image_dir, exist_ok=True)

PREV = 'prev'
NEXT = 'next'


def clean_url(url):
    """Clears parameters from the URL"""
    return url.split('?')[0]


def preserve_tags(element):
    """Extracts the textual content of an HTML element while preserving certain tags"""
    if element.name in ['br', 'p', 'i', 'b', 'a']:
        text = str(element)
    else:
        text = element.get_text()
    text = re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
    return text


def download_image(image_url, file_name):
    """Downloads images from external links"""
    try:
        response = requests.get(image_url, stream=True, headers=config.HEADERS)
        response.raise_for_status()
        with open(file_name, 'wb') as image_file:
            shutil.copyfileobj(response.raw, image_file)
    except Exception as e:
        print(f"Failed to download image {image_url}: {e}")


def remove_node(node):
    """Removes either a NavigableString or a Tag"""
    if isinstance(node, NavigableString):
        node.extract()  # remove text node
    elif isinstance(node, Tag):
        node.decompose()  # remove HTML tag


def extract_attribute(prev_or_next, /, soup, target_text):
    """Extracts an attribute from the text"""
    target_node = soup.find(string=lambda text: target_text in text.lower())
    value = ""
    if target_node:
        value_node = target_node.find_previous() if prev_or_next == PREV else target_node.find_next()
        if value_node:
            value = value_node.get_text(strip=True)
            remove_node(value_node)
        remove_node(target_node)
    return value


def remove_attribute(prev_or_next, /, soup, target_text):
    """Removes an attribute from the text"""
    target_node = soup.find(string=lambda text: target_text in text.lower())
    if target_node:
        value_node = target_node.find_previous() if prev_or_next == PREV else target_node.find_next()
        if value_node:
            remove_node(value_node)
        remove_node(target_node)


def extract_description_content(content):
    content_fix = re.sub(r'<strong>\)\</strong>', ')', content)  # fix a bug in the source
    soup = BeautifulSoup(content_fix, 'html.parser')
    content_lower = content_fix.lower()

    squamish = ""
    halkomelem = ""

    if '(sḵwx̱wú7mesh sníchim)' in content_lower:
        squamish = extract_attribute(PREV, soup, '(sḵwx̱wú7mesh sníchim)')
    if 'sḵwx̱wú7mesh sníchim:' in content_lower:
        squamish = extract_attribute(NEXT, soup, 'sḵwx̱wú7mesh sníchim:')

    if '(hen̓q̓əmin̓əm)' in content_lower:
        halkomelem = extract_attribute(PREV, soup, '(hen̓q̓əmin̓əm)')
    if 'hen̓q̓əmin̓əm:' in content_lower:
        halkomelem = extract_attribute(NEXT, soup, 'hen̓q̓əmin̓əm:')

    if 'Latin:' in content:
        remove_attribute('next', soup, 'latin:')

    cleaned_description = " ".join(map(preserve_tags, soup))
    cleaned_description = re.sub(r"(<p>\s*</p>)+", "", cleaned_description)  # remove any '<p></p>'
    cleaned_description = re.sub(r"\s*<p>\s*|\s*</p>\s*", "<br />", cleaned_description)  # '<p>...</p>' --> '<br />...<br />'
    cleaned_description = re.sub(r"(\s*<br\s*/?>\s*)+", "<br />", cleaned_description)  # multiple <br /> --> <br />
    cleaned_description = cleaned_description.strip("<br />")  # remove leading and trailing <br/>

    return squamish, halkomelem, cleaned_description


def scrape_gallery_page(driver, keyword, page_num):
    page_url = config.GALLERY_URLS[keyword].format(page_num=page_num)

    driver.get(page_url)

    # Wait for the grid to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".category-product-content")
            )
        )
    except TimeoutException:
        print(f"Timeout waiting for page {page_url}. Skipping...")
        return None

    html_gallery = driver.page_source
    # with open("tmp.html", 'w') as f:
    #     f.write(html_gallery)
    soup = BeautifulSoup(html_gallery, 'html.parser')

    # Find all product items
    product_items = soup.find_all('div', class_='product-group')
    if not product_items:
        return None  # No more items to scrape

    items = []

    for item in product_items:
        # Get names
        title_element = item.find('p', class_='w-product-title')
        full_title = title_element['title']
        common_name = full_title.split('(')[0].strip()
        latin_name = re.sub(r"^.*\(([^)]+)\).*$", r"\1", full_title).strip()
        print("-----------------------------------------------------")
        print(f"=== {common_name} ({latin_name}) ===")

        # Detail page
        detail_link = item.find('a', class_='product-image__link')['href']
        detail_url = f"{config.BASE_URL}{clean_url(detail_link)}"
        print("Detail URL:", detail_url)

        driver.get(detail_url)
        # Wait for the content to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".carousel__image")
                )
            )
        except TimeoutException:
            print(f"Timeout waiting for page {detail_url}. Skipping...")
            return None

        html_detail = driver.page_source
        detail_soup = BeautifulSoup(html_detail, 'html.parser')

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
            'IN_STOCK': True,
            'LATIN': latin_name,
            'COMMON': common_name,
            'SQUAMISH': squamish,
            'HALKOMELEM': halkomelem,
            'KEYWORDS': keyword,
            'DESCRIPTION': description,
            'IMAGE': image_url,
            'LINK': detail_url
        })

        time.sleep(random.uniform(2, 5))

    print(f"[Count] {len(items)}", end='\n\n')
    return items


###############################################################################|
if __name__ == '__main__':
    all_items = []

    driver = webdriver.Chrome(service=service, options=options)
    for keyword in config.GALLERY_URLS.keys():
        page_num = 1
        print("========================================================================")
        print(f"[{keyword}]")
        print(f"Go to page: {config.GALLERY_URLS[keyword].replace(config.BASE_URL, '')}")
        while page_num < 10:
            print(f"Retrieving page {page_num}...")
            items = scrape_gallery_page(driver, keyword, page_num)
            if not items:
                print('Empty page. Skipped.', end='\n\n')
                break
            all_items.extend(items)
            page_num += 1
            print()
    driver.quit()

    df = pd.DataFrame(all_items)

    df.replace({r"‘|’": "'", r"“|”": '"', "\n": " "}, regex=True, inplace=True)

    df = df.groupby(df.columns.drop('KEYWORDS').tolist(), as_index=False).agg({'KEYWORDS': ', '.join})

    # Create a new column to store original values, set to '' for non-changed values
    df['LATIN_0'] = df['LATIN'].where(df['LATIN'].isin(corrections.LATIN_REPLACE_SHOP.keys()), '')
    df['COMMON_0'] = df['COMMON'].where(df['COMMON'].isin(corrections.COMMON_REPLACE_SHOP.keys()), '')
    # Correct names
    df['LATIN'] = df['LATIN'].replace(corrections.LATIN_REPLACE_SHOP)
    df['COMMON'] = df['COMMON'].replace(corrections.COMMON_REPLACE_SHOP)

    # Title case
    df['COMMON'] = df['COMMON'].str.replace(r'(^|\s)(\S)', lambda x: x.group(0).upper(), regex=True)

    df.sort_values(by='LATIN', inplace=True)
    df = df[columns.COL_NAMES_SHOP]

    df.to_csv(output_file, index=False)

    print()
    print(df, end='\n\n')
    print(f"File saved: {output_file}")
