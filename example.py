# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 11:34:35 2025

@author: Thomas Lee
Rice University
Department of Earth, Environmental, and Planetary Sciences
Email: tl165@rice.edu

AviList Citation:
AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025. https://doi.org/10.2173/avilist.v2025
"""

from AviList.taxonomy.species import Species
from AviList.taxonomy.genus import Genus
from AviList.taxonomy.family import Family
from AviList.taxonomy.order import Order

from AviList.data.avilistdatabase import AviListDataBase

db = AviListDataBase(path='C:\\thomas\\example_path\\AviListDataBase.db',overwrite_existing=False,verbose=True)

species = Species("Western Cattle Egret", db=db, load_subspecies=True)
print(species)
print(species.brief_summary())

genus = Genus('Calidris', db=db)
print(genus)

family = Family('Podargidae',db=db)
print(family)

order = Order('Anseriformes',db=db)
print(order)
