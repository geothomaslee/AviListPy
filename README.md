# AviListPy
`AviListPy` is a Python package for quickly accessing data from the [AviList Global Check List](https://www.avilist.org/checklist/v2025/). AviList is meant to be a single unified data base for bird taxonomy that will be adopted by many different ornithology authorities. Of particular interest to most people is that the Cornell Lab of Ornithology, the team behind eBird and Merlin, have stated their plans to conform to this checklist completely by 2026.

## AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025. https://doi.org/10.2173/avilist.v2025

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
```
from AviList.database.avilistdatabase import AviListDataBase

db = AviListDataBase(path='/path/to/database/AviListDataBase.db')
```
`db` can then be passed to all taxonomic objects in your script.

## Usage 
Entries in the data base can be accessed by initializing the `AviList.taxonomy` object matching their given rank. For example, `AviList.taxonomy.species.Species`:
```
from AviList.taxonomy.species import Species

species = Species('American Redstart', db=db)
```
The `Species` class contains its corresponding row in the AviList data base in a dictionary-like manner. For example, the AviList column `English_name_AviList` can be accessed by:
```
species['English_name_AviList']
```
These classes have a few of these values written directly as attributes as well for ease of use, such as `species.Family`. These values can still be accessed in the same dictionary like manner. 
`species.name` contains a species plain English name, `species.scientific_name` contains its scientific name. Currently, all other taxonomic ranks have the scientific name saved to the `.name` attribute.

By default, subspecies are not loaded. This can be changed by setting `load_subspecies=True` while intitializing the `Species` class. These are saved to the `Species.subspecies` attribute as a list of `AviList.taxonomy.subspecies.Subspecies` objects. 
When `print()` is called on any taxonomic object in `AviListPy`, it gives a line or two of basic information, then just writes `column: value` for the given row in the AviListDataBase.

For higher taxonomic ranks, lower taxonomic ranks are also loaded in and saved to a list within the higher ranked object. For example:
```
from AviList.taxomomy.genus import Genus

genus = Genus('Calidris', db=db)
```
`genus.species` contains a list of `Species` objects

Higher ranks also contain methods that given information about the lower ranked taxons that they contain. For example,
```
from AviList.taxonomy.family import Family

family = Family('Podargidae', db=db)
family.show_genera()
```
This will give basic information about how many genera this family contains. `family.genera` is an attribute that contains a list of `Genera` objects.

Higher taxonomic ranks can also be passed `load_subspecies=True`, which is just passed to `Species` objects when they are initialized.
