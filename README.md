# plant-data-extractor-python

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE) [![python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org)

The scripts in this repository are used to extract plant catalogues for data review, management, and display on other platforms.

## Data Extraction

### Extract the catalogues in a PDF file

Extract the catalogues from the PDF (not included in this repository) using [PyMuPDF](https://github.com/pymupdf/PyMuPDF) ([reference](https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/table-analysis/join_tables.ipynb)). The PDF should be divided into separate files, and the content should be cleared to make the extraction more accurate.

Other functions in the scripts:

1. Replace some names in the column `LATIN` with more commonly used or newer names, also to keep consistency with the data from the online shop.

2. Record the titles of the tables in the PDF as `CATEGORY`.

3. Extract acronyms list in the PDF and convert them to full words.

4. Merge the `SPEC SIZES` and `SIZES` fields in the PDF for convenience.

### Retrieve data from the online shop

Retrieve the data from the online shopping site using [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) and [Selenium](https://github.com/SeleniumHQ/Selenium) to compare with the catalogue.

To keep consistency, the following fields are revised and replaced/filled out by the scripts:

1. `LATIN` and `COMMON` names.

2. `KEYWORDS`: initial `KEYWORDS` from the tabs on the site are merged with the data in the PDF.

3. `DESCRIPTION`: the text is directly retrieved from the Description section on the detail page of each item.

4. `LINK`: the URL to the detail page.

5. `IMAGE`: the image URLs that are retrieved from the shop. Images are also downloaded by the scripts.

All previous names before correction are copied to the columns `LATIN_0` and `COMMON_0`.
