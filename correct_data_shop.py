#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Corrects names in the CSV from the shop (testing only).
[In] ./catalogues/catalogue_shop_merged.csv
[Out] ./catalogues/catalogue_shop_merged.csv
[Python] 3.11
[Pkgs] pandas
"""
# 2024-10-05 created by Lydia
# 2024-10-05 last modified by Lydia
###############################################################################|
import pandas as pd
import os
from config import config, corrections

input_file = config.CATALOG_FILE_SHOP
output_file = os.path.join(config.CATALOG_DIR, "catalogue_shop_merged_corrected.csv")


###############################################################################|
if __name__ == '__main__':
    df = pd.read_csv(input_file)

    # Use/Create another column to store original values
    df['LATIN_0'] = df['LATIN_0'].where(~df['LATIN'].isin(corrections.LATIN_REPLACE_SHOP.keys()), df['LATIN'])
    df['COMMON_0'] = df['COMMON_0'].where(~df['COMMON'].isin(corrections.COMMON_REPLACE_SHOP.keys()), df['COMMON'])
    # Correct names
    df['LATIN'] = df['LATIN'].replace(corrections.LATIN_REPLACE_SHOP)
    df['COMMON'] = df['COMMON'].replace(corrections.COMMON_REPLACE_SHOP)

    # Title case
    df['COMMON'] = df['COMMON'].str.replace(r'(^|\s)(\S)', lambda x: x.group(0).upper(), regex=True)

    df.to_csv(output_file, index=False)
    print(f'File saved: {output_file}')
