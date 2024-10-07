#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merges CSV tables extracted from PDFs.
[In] ./catalogues/*.csv
[Out] ./catalogues/catalogue_nats_merged.csv
[Python] 3.11
[Pkgs] pandas
"""
# 2024-10-06 created by Lydia
# 2024-10-06 last modified by Lydia
###############################################################################|
import pandas as pd
import os
from config import columns, config, corrections


input_file_nats = config.CATALOG_FILE_NATS
input_file_shop = config.CATALOG_FILE_SHOP
output_file = os.path.join(config.CATALOG_DIR, "catalogue_all_merged.csv")
output_file_original = os.path.join(config.CATALOG_DIR, "catalogue_all_merged_original.csv")


PREPEND = 'prepend'
APPEND = 'append'


def add_keyword(df, src_col, src_text, keyword, prepend_or_append):
    mask = df[src_col].str.contains(src_text) & ~df['KEYWORDS'].str.contains(keyword)
    if mask.any():
        if prepend_or_append == PREPEND:
            df.loc[mask, 'KEYWORDS'] = df.loc[mask, 'KEYWORDS'].apply(lambda x: keyword + (', ' + x if x else ''))
        else:
            df.loc[mask, 'KEYWORDS'] = df.loc[mask, 'KEYWORDS'].apply(lambda x: (x + ', ' if x else '') + keyword)
    return df


###############################################################################|
if __name__ == '__main__':
    df_nats = pd.read_csv(input_file_nats)  # ['LATIN', 'LATIN_0', 'COMMON', 'SUN', 'SOIL', 'HABITAT', 'SIZES', 'CATEGORY']
    df_shop = pd.read_csv(input_file_shop)  # ['IN_STOCK', 'LATIN', 'LATIN_0', 'COMMON', 'COMMON_0', 'SQUAMISH', 'HALKOMELEM', 'KEYWORDS', 'IMAGE', 'LINK', 'DESCRIPTION']

    # Correct sun exposure in NATS
    for name, value in corrections.SUN_FIX.items():
        df_nats.loc[df_nats['LATIN'] == name, 'SUN'] = value

    df_merged = pd.merge(df_nats, df_shop, on=['LATIN', 'COMMON'], how='outer', suffixes=('', '_shop')).fillna('')
    df_merged.sort_values(by='LATIN', inplace=True)
    df_merged.reset_index(drop=True, inplace=True)
    col_names_original = df_merged.columns
    # print(list(col_names_original))

    df_merged.to_csv(output_file_original, index=False)
    print(f"File saved: {output_file_original}")

    # Correct 'Perennial/Annual' in 'KEYWORDS'
    if corrections.PERENNIALS:
        mask = df_merged['LATIN'].isin(corrections.PERENNIALS)
        if mask.any():
            df_merged.loc[mask, 'KEYWORDS'] = df_merged.loc[mask, 'KEYWORDS'].str.replace('Perennial/Annual', 'Perennials')
    if corrections.ANNUALS:
        mask = df_merged['LATIN'].isin(corrections.ANNUALS)
        if mask.any():
            df_merged.loc[mask, 'KEYWORDS'] = df_merged.loc[mask, 'KEYWORDS'].str.replace('Perennial/Annual', 'Annuals')

    # Add keywords based on 'CATEGORY'
    keyword_dict = {
        'Perennials': 'Perennials',
        'Native Trees': 'Native Trees',
        'Shrubs': 'Shrubs',
        'Groundcover': 'Groundcover',
        "Wetland Plants": "Wetland"
    }
    for src_text, keyword in keyword_dict.items():
        df_merged = add_keyword(df_merged, 'CATEGORY', src_text, keyword, PREPEND)
    
    # Add keywords based on 'HABITAT'
    keyword_dict = {
        'Wetland': 'Wetland',
        'Salt Marsh': 'Salt Marsh'
    }
    for src_text, keyword in keyword_dict.items():
        df_merged = add_keyword(df_merged, 'HABITAT', src_text, keyword, APPEND)

    # Add keywords from Perennials—Sun and Perennials—Shade lists in NATS
    for name in corrections.PERENNIALS:
        df_merged = add_keyword(df_merged, 'LATIN', name, 'Perennials', PREPEND)

    # Add keywords from Grasses list in NATS
    for name in corrections.GRASSES:
        df_merged = add_keyword(df_merged, 'LATIN', name, 'Grasses', APPEND)

    # Add keywords from Ferns—Shade list in NATS
    for name in corrections.FERNS:
        df_merged = add_keyword(df_merged, 'LATIN', name, 'Ferns', APPEND)

    # Add keywords from Bulbs list in NATS
    for name in corrections.BULBS:
        df_merged = add_keyword(df_merged, 'LATIN', name, 'Bulbs', APPEND)

    # Add keywords from Perennials—Sun list in NATS
    for name in corrections.SUN_LOVING:
        df_merged = add_keyword(df_merged, 'LATIN', name, 'Sun-loving', APPEND)

    # Add keywords from Ferns—Shade and Perennials—Shade lists in NATS
    for name in corrections.SHADE_FRIENDLY:
        df_merged = add_keyword(df_merged, 'LATIN', name, 'Shade-friendly', APPEND)

    # Extra columns
    for col in columns.COL_NAMES_ALL:
        if col not in col_names_original:
            df_merged[col] = ""

    df_merged = df_merged[columns.COL_NAMES_ALL]

    df_merged.to_csv(output_file, index=False)
    print(f"File saved: {output_file}")
