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

from AviList.data.avilistdatabase import AviListDataBase
from AviList.taxonomy.species import Species
from AviList.taxonomy.genus import Genus
from AviList.taxonomy.family import Family
from AviList.taxonomy.order import Order

db = AviListDataBase()
db._save()

#species = Species('Brown Thornbill', load_subspecies=True)
#print(species)

#family = Family('Acanthizidae', load_subspecies=False)
#family.show_genera()

order = Order('Anseriformes')
print(order)