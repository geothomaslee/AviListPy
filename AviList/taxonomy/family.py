# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 13:14:46 2025

@author: Thomas Lee
Rice University
Department of Earth, Environmental, and Planetary Sciences
Email: tl165@rice.edu

AviList Citation:
AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025. https://doi.org/10.2173/avilist.v2025
"""

from AviList.data.avilistdatabase import AviListDataBase
from AviList.taxonomy.genus import Genus

class Family():
    def __init__(self, name: str, exact: bool=False, load_subspecies: bool=False):
        self.db = AviListDataBase()
        self.df = self.lookup_family(name, exact=exact)
        self._data = self.df.iloc[0].to_dict()
        self.name = self._data['Scientific_name']
        self.order = self._data['Order']
        self.genera = self.find_matching_genera(exact=exact, load_subspecies=load_subspecies)
        self.species = self.find_matching_species()

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

    def lookup_family(self, name, exact: bool=False):
        df = self.db.df[self.db.df['Taxon_rank'].str.contains('family')]
        if exact is True:
            _family_df = df[df['Scientific_name'] == name]
        else:
            _family_df = df[df['Scientific_name'].str.contains(name, case=False, na=False)]
        if _family_df.shape[0] == 0:
            raise ValueError('No matching families found')
        if _family_df.shape[0] > 1:
            fail_str = f'{name} could refer to: \n'
            for _family_ in _family_df['Scientific_name'].to_list():
                fail_str += (f'{_family_}, ')
            raise ValueError(fail_str)
        _family_df = _family_df.dropna(axis=1)
        return _family_df

    def find_matching_genera(self, exact: bool=False, load_subspecies: bool=False):
        genus_df = self.db.df[self.db.df['Taxon_rank'] == 'genus']
        matching_genus_df = genus_df[genus_df['Family'] == str(self.name)]
        print(f'Loading {len(matching_genus_df)} genera in family {self.name}')
        if len(matching_genus_df) == 0:
            raise ValueError('No matching genera found')
        matching_genera_list = []
        for _matching_genus_name in matching_genus_df['Scientific_name'].to_list():
            matching_genera_list.append(Genus(_matching_genus_name, exact=True))
        return matching_genera_list

    def find_matching_species(self):
        species_list = []
        for genus in self.genera:
            species_list += genus.species
        return species_list

    def show_genera(self):
        print(f'{len(self.genera)} genera in family {self.name}')
        count = 0
        for genus in self.genera:
            print(f'{genus.name}: {len(genus.species)} species')
            count += len(genus.species)
        print(f'{count} total species in {self.name}')
