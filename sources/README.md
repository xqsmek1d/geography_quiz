# Data Sources

The original source for country information (including ISO3 codes, names, capitals, regions, subregions, nationalities, and other metadata) was:

* https://github.com/amckenna41/iso3166-flags/tree/main

Official country names, ISO3 codes, and optional prefixes, suffixes, and alternative names were verified and supplemented using the ISO Online Browsing Platform:

* https://www.iso.org/obp/ui/#home
* country specific wikipedia pages

The ISO 3166-1 alpha-3 (ISO3) standard was taken as the basis for distinguishing countries. Consequently, territories without an officially assigned ISO3 code (for example, Northern Cyprus) are not included as separate countries.

Country flags are predominantly sourced from Wikipedia.

Country population data was (partly) updated using:

* https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population

Country outline geometries were obtained from the World Bank Official Boundaries dataset:

* https://datacatalog.worldbank.org/search/dataset/0038272/world-bank-official-boundaries

Several manual adjustments were made to align the dataset with the ISO3 standard, including correcting or merging geometries where necessary to match the recognised ISO3 entities.

Capital and city information (including geographic coordinates) was primarily obtained from the Esri World Cities dataset:

* https://hub.arcgis.com/datasets/esri::world-cities/explore?location=11.704001%2C1.535162%2C1

Additional cities were added where necessary, and city information was corrected or updated to align with the ISO3 standard rather than the FIPS-based classification used by the original dataset.

## Disclaimer

Country and territorial recognition varies between organisations and data providers. As a result, different datasets occasionally disagree on whether a territory should be treated as an independent country, a dependency, or part of another sovereign state. To maintain internal consistency throughout this project, the ISO 3166-1 alpha-3 standard was adopted wherever possible. In cases where source datasets differed from this standard, manual decisions and adjustments were made to ensure that all data sources remained consistent with the chosen ISO3-based country definitions.
