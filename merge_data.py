#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Merges CSV tables.
[In] ./catalogues/*.csv
[Out] ./catalogues/catalogue_merged_original.csv, ./catalogues/catalogue_merged.csv
[Python] 3.11
[Pkgs] pandas
"""
# 2024-10-04 created by Lydia
# 2024-10-04 last modified by Lydia
###############################################################################|
import os
import pandas as pd
import constants as const

pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_rows", 10)
pd.set_option("max_colwidth", 15)


output_dir = "./catalogues"
output_file_original = os.path.join(output_dir, "catalogue_merged_original.csv")
output_file = os.path.join(output_dir, "catalogue_merged.csv")


###############################################################################|
if __name__ == '__main__':
    dfs = []
    for category in const.CATEGORIES:
        df = pd.read_csv(os.path.join(output_dir, f'{category}.csv'))

        # Rename 'SPEC SIZES' to 'SIZES'
        if 'SPEC SIZES' in df.columns:
            df.rename(columns={'SPEC SIZES': 'SIZES'}, inplace=True)

        dfs.append(df)

    df_merged = pd.concat(dfs, ignore_index=True)
    col_names_original = df_merged.columns
    df_merged.to_csv(output_file_original, index=False)
    print(df_merged.shape, end='\n\n')
    print(f'File saved: {output_file_original}', end='\n\n')

    for col in const.COL_NAMES_ALL:
        if col not in col_names_original:
            df_merged[col] = ""

    df_merged = df_merged[const.COL_NAMES_ALL]

    df_merged.to_csv(output_file, index=False)
    print(df_merged)
    print(f'File saved: {output_file}')
