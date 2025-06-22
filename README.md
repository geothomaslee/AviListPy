# AviListPy
### A Python implementation of AviList 2025
AviList:
AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025. https://doi.org/10.2173/avilist.v2025

### Installation
This requires pandas, openpyxl

#### With Pip
`pip install pandas, openpyxl`

#### With Conda/Mamba
It is recommended you create a new environment for this package:
`conda create -n AviListPy python=3.12 pandas openpyxl` or `mamba create -n AviListPy python=3.12 pandas openpyxl`

Or if you want to install into an existing environment:
`conda install pandas openpyxl` or `mamba install pandas openpyxl`

#### First Time Use
AviListPy uses the `AviListDataBase` class as a very light weight wrapper for a Pandas DataFrame containing the actual Excel file from the AviList team [^1]. This `AviListDataBase` is used by every taxonomic class, and instance of the database can be passed directly to each taxonomic object when initializing, or it can create its own every time directly from the AviList excel file.





[^1] AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025. https://doi.org/10.2173/avilist.v2025
