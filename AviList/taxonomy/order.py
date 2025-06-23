# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 14:25:46 2025

@author: Thomas Lee
Rice University
Department of Earth, Environmental, and Planetary Sciences
Email: tl165@rice.edu
"""

from AviList.taxonomy.family import Family
from AviList.data.avilistdatabase import AviListDataBase

class Order():
    def __init__(self, name: str, exact: bool=False, load_subspecies: bool=False, db: AviListDataBase=None):
        if db is None:
            self.db = AviListDataBase()
        else:
            self.db = db
        self.df = self.lookup_order(name)
        self._data = self.df.iloc[0].to_dict()
        self.name = self._data['Scientific_name']
        self.families = self.find_matching_families(exact=exact,load_subspecies=load_subspecies)
        self.genera = self.find_matching_genera()
        self.species = self.find_matching_species()

    def __str__(self):
        return_str = f'{self.name}'
        num_equals = (80 - len(return_str)) // 2
        return_str = '='*num_equals + return_str + '='*num_equals
        return_str += f'\n{len(self.species)} species in {len(self.genera)} genera across {len(self.families)} families'
        for key, val in self.items():
            return_str += (f'\n{key}: {val}')
        return return_str + '\n'

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

    def lookup_order(self, name):
        """
        Parameters
        ----------
        name : str
            Order to search for.
        exact : bool, optional
            If True, will only search for the exact string in the data base. If False, will search
            for any string containing name as a substring, and is not case sensitive. The default is False.

        Returns
        -------
        _order_df : pandas.DataFrame
           Pandas DataFrame with only one row containing the entry for the order.

        """
        df = self.db.df[self.db.df['Taxon_rank'].str.contains('order')]
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

    def find_matching_families(self, exact: bool=False, load_subspecies: bool=False):
        """
        Parameters
        ----------
        exact : bool, optional
            If True, will only search for the exact string in the data base. If False, will search
            for any string containing name as a substring, and is not case sensitive. The default is False.
        load_subspecies : bool, optional
            If True, loads subspecies. The default is False.

        Returns
        -------
        matching_family_list : list of AviList.taxonomy.family.Family
            List of families contained within the order.
        """
        family_df = self.db.df[self.db.df['Taxon_rank'] == 'family']
        matching_family_df = family_df[family_df['Order'] == str(self.name)]
        print(f'Loading {len(matching_family_df)} families in order {self.name}')
        if len(matching_family_df) == 0:
            raise ValueError('No matching families found')
        matching_family_list = []
        for _matching_family_name in matching_family_df['Scientific_name'].to_list():
            matching_family_list.append(Family(_matching_family_name, db=self.db, exact=True))
        return matching_family_list

    def find_matching_genera(self):
        genera_list = []
        for family in self.families:
            genera_list += family.genera
        return genera_list

    def find_matching_species(self):
        species_list = []
        for genus in self.genera:
            species_list += genus.species
        return species_list

    def show_families(self):
        print(f'{len(self.families)} family in order {self.name}')
        count = 0
        for family in self.families:
            print(f'{family.name}: {len(family.genera)} genera, {len(family.species)} species')
            count += len(family.species)
        print(f'{count} total species in {self.name}')

    def show_genera(self):
        print(f'{len(self.genera)} genera in family {self.name}')
        count = 0
        for genus in self.genera:
            print(f'{genus.name}: {len(genus.species)} species')
            count += len(genus.species)
        print(f'{count} total species in {self.name}')