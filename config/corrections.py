# -*- coding: utf-8 -*-
# config/corrections.py

# To keep consistency with NATS
LATIN_REPLACE_SHOP = {
    "Aruncus sylvester": "Aruncus sylvestris (dioicus)",
    "Cornus sericea": "Cornus sericea (stolonifera)",
    "Pseudotsuga menziesii": "Pseudotsuga menziesii var. menziesii",  # ? (Coastal Douglas-fir)
    "Salix lasiandra": "Salix lucida ssp. lasiandra",
    "Spirea douglasii": "Spiraea douglasii",  # more common
    "Symphoricarpus albus": "Symphoricarpos albus",  # typo fixed
    "Symplocarpus foetidus": "Lysichiton americanus",  # ? (Western Skunk Cabbage)
    "Tsuga Hetrophylla": "Tsuga heterophylla",  # typo fixed
    "Vaccininium ovatum": "Vaccinium ovatum",  # typo fixed
    "Vaccinium parviflorum": "Vaccinium parvifolium"  # typo fixed
}

# To keep consistency with NATS
COMMON_REPLACE_SHOP = {
    "Maple - Vine": "Vine Maple",
    "Goastsbeard": "Goat's Beard",
    "Red-osier Dogwood": "Red-twig Dogwood",
    "Crabapple - Pacific": "Pacific Crabapple",
    "Osoberry/Wild Plum": "Osoberry/Indian Plum/Wild Plum",
    "Pine - Lodgepole": "Lodgepole Pine",
    "Douglas fir": "Coastal Douglas-fir",  # ?
    "Willow - Pacific": "Pacific Willow",
    "Elderberry - Blue": "Blue Elderberry",
    "Elderberry - Red": "Red Elderberry",
    "Stonecrop - Spreading": "Spreading Stonecrop",
    "Snowberry": "Common Snowberry",
    "Skunk Cabbage": "Western Skunk Cabbage",  # ?
    "Western Hemlock -": "Western Hemlock",  # typo fixed
    "Huckleberry - Evergreen": "Evergreen Huckleberry",
    "Huckleberry - Black": "Black Huckleberry",
    "Huckleberry - Red": "Red Huckleberry"
}

# Corrections in NATS (also for keeping consistency with the shop)
LATIN_REPLACE_NATS = {
    "Malus diversifolia": "Malus fusca",  # better
    "Osmaronia (Oemleria) cerasiformis": "Oemleria cerasiformis",  # newer
    "Salix lasiandra": "Salix lucida ssp. lasiandra"  # newer
}

# To keep consistency with the shop
COMMON_REPLACE_NATS = {
    "Indian Plum": "Osoberry/Indian Plum/Wild Plum",
    "Skunk Cabbage": "Western Skunk Cabbage",  # ?
    "False Lily-of-the- Valley": "False Lily-of-the-Valley"  # typo fixed
}

# From Perennials—Sun, Perennials—Shade and other data in NATS
PERENNIALS = [
    # correct 'Perennial/Annual' in the shop
    "Lysichiton americanus",
    "Sedum divergens"
] + [
    # Perennials—Sun
    "Achillea millefolium",
    "Anaphalis margaritaceae",
    "Anemone multifida",
    "Arctostaphylos uva-ursi",
    "Armeria maritima",
    "Artemesia frigida",
    "Aster",  # Aster spp.
    "Campanula rotundifolia",
    "Castilleja",  # Castilleja spp.
    "Eriophyllum lanatum",
    "Fragaria",  # Fragaria spp.
    "Gaillaria aristata",
    "Gallium boreale",
    "Geum triflorum",
    "Heuchera cylindrica",  # Heuchera spp.
    "Oslynium douglasii",
    "Penstemon",  # Penstemon spp.
    "Sisyrinchium",  # Sisyrinchium spp.
    "Solidago canadensis"
] + [
    # Perennials—Shade
    "Achlys triphylla",
    "Aquilegia formosa",
    "Cornus canadensis",
    "Dicentra formosa",
    "Fragaria chiloensis",  # SUN value fixed
    "Geum macrophyllum",
    "Maianthemum dilatatum",
    "Tellima grandiflora",
    "Tolmiea menziesii",
    "Viola sempervirens"
]

ANNUALS = []

# From Ferns—Shade in NATS
FERNS = [
    "Adiantum aleuticum",
    "Blechnum spicant",
    "Polypodium glycyrrhiza",
    "Polypodium scouleri",
    "Polystichum munitum",
    "Polystichum neolobatum"
]

# From Perennials—Sun in NATS
SUN_LOVING = [
    "Achillea millefolium",
    "Anaphalis margaritaceae",
    "Anemone multifida",
    "Arctostaphylos uva-ursi",
    "Armeria maritima",
    "Artemesia frigida",
    "Aster",  # Aster spp.
    "Campanula rotundifolia",
    "Castilleja",  # Castilleja spp.
    "Eriophyllum lanatum",
    "Fragaria",  # Fragaria spp.
    "Gaillaria aristata",
    "Gallium boreale",
    "Geum triflorum",
    "Heuchera cylindrica",  # Heuchera spp.
    "Oslynium douglasii",
    "Penstemon",  # Penstemon spp.
    "Sisyrinchium",  # Sisyrinchium spp.
    "Solidago canadensis"
]

# From Ferns—Shade and Perennials—Shade in NATS
SHADE_FRIENDLY = [
    # Ferns—Shade
    "Adiantum aleuticum",
    "Blechnum spicant",
    "Polypodium glycyrrhiza",
    "Polypodium scouleri",
    "Polystichum munitum",
    "Polystichum neolobatum",
] + [
    # Perennials—Shade
    "Achlys triphylla",
    "Aquilegia formosa",
    "Cornus canadensis",
    "Dicentra formosa",
    "Fragaria chiloensis",  # SUN value fixed
    "Geum macrophyllum",
    "Maianthemum dilatatum",
    "Tellima grandiflora",
    "Tolmiea menziesii",
    "Viola sempervirens"
]

# From Grasses in NATS
GRASSES = [
    "Carex pachystachya",  # Carex spp. (dryland)
    "Carex pansa",  # Carex spp. (dryland)
    "Carex tumulicola",  # Carex spp. (dryland)
    "Festuca",  # Festuca spp.
    "Koeleria macrantha",
    "Calamagrostis stricta",
    "Schizachyrium scoparium"
]

BULBS = [
    "Allium acuminatum",
    "Allium cernuum",
    "Allium schoenoprasm",
    "Brodiaea",
    "Camassia quamash",
    "Narcissus",
    "Oslynium douglasii"
]

# Corrections
SUN_FIX = {
    "Fragaria chiloensis": "Sun/Partial Shade"
}
