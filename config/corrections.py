# -*- coding: utf-8 -*-
# config/corrections.py

# Keeping consistent with NATS
LATIN_REPLACE_SHOP = {
    "Aruncus sylvester": "Aruncus sylvestris (dioicus)",
    "Cornus sericea": "Cornus sericea (stolonifera)",
    "Pseudotsuga menziesii": "Pseudotsuga menziesii var. menziesii",  # needs review
    "Salix lasiandra": "Salix lucida ssp. lasiandra",
    "Spirea douglasii": "Spiraea douglasii",  # more common
    "Symphoricarpus albus": "Symphoricarpos albus",  # typo fixed
    "Symplocarpus foetidus": "Lysichiton americanus",  # needs review (Western Skunk Cabbage)
    "Tsuga Hetrophylla": "Tsuga heterophylla",  # typo fixed
    "Vaccininium ovatum": "Vaccinium ovatum",  # typo fixed
    "Vaccinium parviflorum": "Vaccinium parvifolium"  # typo fixed
}

# Keeping consistent with NATS
COMMON_REPLACE_SHOP = {
    "Maple - Vine": "Vine Maple",
    "Goastsbeard": "Goat's Beard",
    "Red-osier Dogwood": "Red-twig Dogwood",
    "Crabapple - Pacific": "Pacific Crabapple",
    "Osoberry/Wild Plum": "Osoberry/Indian Plum/Wild Plum",
    "Pine - Lodgepole": "Lodgepole Pine",
    "Douglas fir": "Coastal Douglas-fir",  # needs review
    "Willow - Pacific": "Pacific Willow",
    "Elderberry - Blue": "Blue Elderberry",
    "Elderberry - Red": "Red Elderberry",
    "Stonecrop - Spreading": "Spreading Stonecrop",
    "Snowberry": "Common Snowberry",
    "Skunk Cabbage": "Western Skunk Cabbage",  # needs review
    "Western Hemlock -": "Western Hemlock",  # typo fixed
    "Huckleberry - Evergreen": "Evergreen Huckleberry",
    "Huckleberry - Black": "Black Huckleberry",
    "Huckleberry - Red": "Red Huckleberry"
}

# Corrections in NATS
LATIN_REPLACE_NATS = {
    "Malus diversifolia": "Malus fusca",  # better
    "Osmaronia (Oemleria) cerasiformis": "Oemleria cerasiformis",  # newer
    "Salix lasiandra": "Salix lucida ssp. lasiandra"  # newer
}

# Keeping consistent with the shop
COMMON_REPLACE_NATS = {
    "Indian Plum": "Osoberry/Indian Plum/Wild Plum",
    "Skunk Cabbage": "Western Skunk Cabbage"  # needs review
}

# Perennial plants (Latin)
PERENNIALS = ["Lysichiton americanus", "Sedum divergens"]

# Annual plants (Latin)
ANNUALS = []
