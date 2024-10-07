#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exports dicts as CSV tables.
[Out] ./exported_dicts/*.csv
[Python] 3.11
[Pkgs] pandas
"""
# 2024-10-06 created by Lydia
# 2024-10-06 last modified by Lydia
###############################################################################|
import pandas as pd
import os
from config import corrections, mappings


output_dir = './exported_dicts'

correction_dicts = [
    (corrections.LATIN_REPLACE_SHOP, 'latin_replace_shop.csv'),
    (corrections.COMMON_REPLACE_SHOP, 'common_replace_shop.csv'),
    (corrections.LATIN_REPLACE_NATS, 'latin_replace_nats.csv'),
    (corrections.COMMON_REPLACE_NATS, 'common_replace_nats.csv')
]

mapping_dicts = [
    (mappings.SUN_MAPPING, 'sun_mapping.csv'),
    (mappings.SOIL_MAPPING, 'soil_mapping.csv'),
    (mappings.HABITAT_MAPPING, 'habitat_mapping.csv'),
    (mappings.SIZE_MAPPING, 'size_mapping.csv')
]


###############################################################################|
if __name__ == '__main__':
    os.makedirs(output_dir, exist_ok=True)

    for d, filename in correction_dicts:
        output_file = os.path.join(output_dir, filename)
        df = pd.DataFrame(list(d.items()), columns=['OLD', 'NEW'])
        df.to_csv(output_file, index=False)
        print(f'File saved: {output_file}')
    
    for d, filename in mapping_dicts:
        output_file = os.path.join(output_dir, filename)
        df = pd.DataFrame(list(d.items()), columns=['ACRONYM', 'FULL'])
        df.to_csv(output_file, index=False)
        print(f'File saved: {output_file}')
