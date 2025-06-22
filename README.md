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
`conda create -n AviListPy python=3.12 pandas openpyxl` or
`mamba create -n AviListPy python=3.12 pandas openpyxl`

Or if you want to install into an existing environment:
`conda install pandas openpyxl` or 
`mamba install pandas openpyxl`

#### First Time Use
AviListPy uses the `AviListDataBase` class as a very light weight wrapper for a Pandas DataFrame containing the actual Excel file from the AviList team. This `AviListDataBase` is used by every taxonomic class, and an instance of the database can be passed directly to each taxonomic object when initializing, or these classes can create their own irectly from the AviList excel file. It is recommended to initialize a single instanec of `AviListDatabase` at the beginning of your script and pass it to taxonomic classes, because it takes about 10 seconds to load the entire excel sheet. `AviListDataBase` can also be fed a file path, where it will pickle itself or look for an already pickled version of itself to load in. This is the fastest option. 

#### Example Setup
<python>
from AviList.database.avilistdatabase import AviListDataBase

db = AviListDataBase(path='/path/to/database/AviListDataBase.db')
</python>
`db` can then be fed to all taxonomic objects in your script.

