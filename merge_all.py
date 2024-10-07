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


def add_keyword(df, keyword):
    mask = df['CATEGORY'].str.contains(keyword) & ~df['KEYWORDS'].str.contains(keyword)
    df.loc[mask, 'KEYWORDS'] = df.loc[mask, 'KEYWORDS'].apply(lambda x: keyword + (', ' + x if x else ''))
    return df


###############################################################################|
if __name__ == '__main__':
    df_nats = pd.read_csv(input_file_nats)  # ['LATIN', 'LATIN_0', 'COMMON', 'SUN', 'SOIL', 'HABITAT', 'SIZES', 'CATEGORY']
    df_shop = pd.read_csv(input_file_shop)  # ['IN_STOCK', 'LATIN', 'LATIN_0', 'COMMON', 'COMMON_0', 'SQUAMISH', 'HALKOMELEM', 'KEYWORDS', 'IMAGE', 'LINK', 'DESCRIPTION']

    df_merged = pd.merge(df_nats, df_shop, on='LATIN', how='outer', suffixes=('', '_shop')).fillna('')
    df_merged.sort_values(by='LATIN', inplace=True)
    df_merged.reset_index(drop=True, inplace=True)
    col_names_original = df_merged.columns
    # print(list(col_names_original))

    # Correct 'Perennial/Annual' in 'KEYWORDS'
    if corrections.PERENNIALS:
        mask = df_merged['LATIN'].isin(corrections.PERENNIALS)
        df_merged.loc[mask, 'KEYWORDS'] = df_merged.loc[mask, 'KEYWORDS'].str.replace('Perennial/Annual', 'Perennial')
    if corrections.ANNUALS:
        mask = df_merged['LATIN'].isin(corrections.ANNUALS)
        df_merged.loc[mask, 'KEYWORDS'] = df_merged.loc[mask, 'KEYWORDS'].str.replace('Perennial/Annual', 'Annual')

    # Prepend keywords
    for keyword in ['Perennial', 'Native Trees', 'Shrubs', 'Groundcover']:
        df_merged = add_keyword(df_merged, keyword)

    for col in columns.COL_NAMES_ALL:
        if col not in col_names_original:
            df_merged[col] = ""

    df_merged = df_merged[columns.COL_NAMES_ALL]

    df_merged.to_csv(output_file, index=False)
    print(f"File saved: {output_file}")
