#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merges CSV tables extracted from PDFs.
[In] ./catalogues/*.csv
[Out] ./catalogues/catalogue_nats_merged.csv
[Python] 3.11
[Pkgs] pandas
"""
# 2024-10-04 created by Lydia
# 2024-10-05 last modified by Lydia
###############################################################################|
import os
import pandas as pd
from config import columns, config, corrections, mappings

pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_rows", 10)
pd.set_option("max_colwidth", 15)


output_dir = config.CATALOG_DIR
output_file = config.CATALOG_FILE_NATS
# output_file_modified = os.path.join(output_dir, "catalogue_nats_merged_modified.csv")


###############################################################################|
if __name__ == '__main__':
    dfs = []
    for category in mappings.CATEGORIES:
        df = pd.read_csv(os.path.join(output_dir, f'{category}.csv'))

        # Rename 'SPEC SIZES' to 'SIZES'
        if 'SPEC SIZES' in df.columns:
            df.rename(columns={'SPEC SIZES': 'SIZES'}, inplace=True)

        dfs.append(df)

    df_merged = pd.concat(dfs, ignore_index=True)
    col_names_original = df_merged.columns

    # Create a new column to store original values, set to '' for non-changed values
    df_merged['LATIN_0'] = df_merged['LATIN'].where(df_merged['LATIN'].isin(corrections.LATIN_REPLACE_NATS.keys()), '')
    df_merged['COMMON_0'] = df_merged['COMMON'].where(df_merged['COMMON'].isin(corrections.COMMON_REPLACE_NATS.keys()), '')
    # Correct names
    df_merged['LATIN'] = df_merged['LATIN'].replace(corrections.LATIN_REPLACE_NATS)
    df_merged['COMMON'] = df_merged['COMMON'].replace(corrections.COMMON_REPLACE_NATS)

    df_merged.sort_values(by='LATIN', inplace=True)
    df_merged = df_merged[columns.COL_NAMES_NATS]

    df_merged.to_csv(output_file, index=False)
    print(df_merged.shape, end='\n\n')
    print(f'File saved: {output_file}')

    # for col in columns.COL_NAMES_ALL:
    #     if col not in col_names_original:
    #         df_merged[col] = ""

    # df_merged = df_merged[columns.COL_NAMES_ALL]

    # df_merged.to_csv(output_file_modified, index=False)
    # print(df_merged)
    # print(f'File saved: {output_file_modified}')
