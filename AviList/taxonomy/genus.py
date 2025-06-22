# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 12:41:08 2025

@author: Thomas Lee
Rice University
Department of Earth, Environmental, and Planetary Sciences
Email: tl165@rice.edu

AviList Citation:
AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025. https://doi.org/10.2173/avilist.v2025
"""

from AviList.data.avilistdatabase import AviListDataBase
from AviList.taxonomy.species import Species

class Genus():
    def __init__(self, name: str, exact: bool=False, load_subspecies: bool=False, db: AviListDataBase=None):
        if db is None:
            self.db = AviListDataBase()
        else:
            self.db = db
        self.df = self.lookup_genus(name, exact=exact)
        self._data = self.df.iloc[0].to_dict()
        self.name = self._data['Scientific_name']
        self.family = self._data['Family']
        self.order = self._data['Order']
        self.species = self.find_matching_species(load_subspecies=load_subspecies)

    def __str__(self):
        return_str = f'{self["Scientific_name"]}'
        for key, val in self.items():
            return_str += (f'\n{key}: {val}')
        return return_str

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, key):
        return key in self._data

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def lookup_genus(self, name, exact: bool=False):
        df = self.db.df[self.db.df['Taxon_rank'].str.contains('genus')]
        if exact is True:
            _genus_df = df[df['Scientific_name'] == name]
        else:
            _genus_df = df[df['Scientific_name'].str.contains(name, case=False, na=False)]

        if _genus_df.shape[0] == 0:
            raise ValueError('No matching species found')
        if _genus_df.shape[0] > 1:
            fail_str = f'{name} could refer to: \n'
            for _genus_ in _genus_df['Scientific_name'].to_list():
                fail_str += (f'{_genus_}, ')
            raise ValueError(fail_str)
        _genus_df = _genus_df.dropna(axis=1)
        return _genus_df

    def find_matching_species(self, load_subspecies: bool=False):
        species_df = self.db.df[self.db.df['Taxon_rank'] == 'species']
        matching_species_df = species_df[species_df['Scientific_name'].str.contains(self.name)]
        matching_species_list = []
        for _matching_species_name in matching_species_df['English_name_AviList'].to_list():
            matching_species_list.append(Species(_matching_species_name, db = self.db, exact=True, load_subspecies=load_subspecies))
        return matching_species_list

    def show_species(self):
        for species in self.species:
            print(species)