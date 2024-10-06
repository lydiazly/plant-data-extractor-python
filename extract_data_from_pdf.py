#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Uses PyMuPDF to extract tables in PDFs.
Reference: https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/table-analysis/join_tables.ipynb
[In] ../data/*.pdf
[Out] ./catalogues/*.csv
[Python] 3.11
[Pkgs] pandas, pymupdf
"""
# 2024-10-04 created by Lydia
# 2024-10-05 last modified by Lydia
###############################################################################|
import pandas as pd
import os
import fitz
if not hasattr(fitz.Page, "find_tables"):
    raise RuntimeError("This PyMuPDF version does not support the table feature")

from config import config, mappings

pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_rows", 10)
pd.set_option("max_colwidth", 15)


input_file_prefix = config.PDF_PREFIX
output_dir = config.CATALOG_DIR


def replace_acronyms(column, mapping):
    for acronym, full_text in mapping.items():
        column = column.str.replace(r'\b' + acronym + r'\b', full_text, regex=True)
    return column


def extract_category_data(category, category_name):
    input_file = f'{input_file_prefix}_{category}.pdf'
    doc = fitz.open(input_file)

    print(f'=== {category} ===')
    df_fragments = []  # list of DataFrames per table fragment
    for page in doc:  # iterate over the pages
        tabs = page.find_tables()
        if len(tabs.tables) == []:
            break
        tab = tabs[0]  # the 1st table
        df_tmp = tab.to_pandas()
        df_fragments.append(df_tmp)  # append this DataFrame
        print(df_tmp.shape)

    df = pd.concat(df_fragments)
    df['CATEGORY'] = category_name

    df.replace({r"‘|’": "'", r"“|”": '"', "\n": " "}, regex=True, inplace=True)

    df['SUN'] = replace_acronyms(df['SUN'], mappings.SUN_MAPPING)
    df['SOIL'] = replace_acronyms(df['SOIL'], mappings.SOIL_MAPPING)
    df['HABITAT'] = replace_acronyms(df['HABITAT'], mappings.HABITAT_MAPPING)
    try:
        df['SPEC SIZES'] = replace_acronyms(df['SPEC SIZES'], mappings.SIZE_MAPPING)
    except KeyError:
        pass

    return df


###############################################################################|
if __name__ == '__main__':
    os.makedirs(output_dir, exist_ok=True)

    dfs = []
    for category, category_name in mappings.CATEGORIES.items():
        df = extract_category_data(category, category_name)

        output_file_category = os.path.join(output_dir, f'{category}.csv')
        df.to_csv(output_file_category, index=False)
        print(df, end='\n\n')
        print(f'File saved: {output_file_category}')
