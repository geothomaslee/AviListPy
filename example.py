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

from AviListPy import Species, Genus, Order, Family, AviListDataBase

db = AviListDataBase(path='C:\\thomas\\example_path\\AviListDataBase.db',overwrite_existing=False,verbose=True)

species = Species("Western Cattle Egret", db=db, load_subspecies=True)
print(species)
print(species.brief_summary())

genus = Genus('Calidris', db=db)
print(genus)

family = Family('Anatidae',db=db,exact=True)
print(family)

order = Order('Anseriformes',db=db)
print(order)

