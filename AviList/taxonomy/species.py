# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 11:38:06 2025

@author: Thomas Lee
Rice University
Department of Earth, Environmental, and Planetary Sciences
Email: tl165@rice.edu

AviList Citation:
AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025. https://doi.org/10.2173/avilist.v2025
"""

from AviList.data.avilistdatabase import AviListDataBase
from AviList.taxonomy.subspecies import Subspecies

class Species():
    def __init__(self, name: str, exact: bool=False, load_subspecies=False, db: AviListDataBase=None):
        if db is None:
            self.db = AviListDataBase()
        else:
            self.db = db
        self.df = self.lookup_species_common_name(name, exact=exact)
        self._data = self.df.iloc[0].to_dict()
        self.name = self._data['English_name_AviList']
        self.scientific_name = self._data['Scientific_name']
        self.order = self._data['Order']
        self.family = self._data['Family']
        self.subspecies = None

        if load_subspecies is True:
            self.subspecies = self.get_subspecies()

    def __str__(self):
        return_str = f'{self["English_name_AviList"]}'
        if self.subspecies is not None:
            return_str += f'\nContains {len(self.subspecies)} subspecies'
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

    def lookup_species_common_name(self, name: str, exact: bool=False):
        """
        Parameters
        ----------
        name : str
            Species to search for.
        exact : bool, optional
            If True, will only search for the exact string in the data base. If False, will search
            for any string containing name as a substring, and is not case sensitive. The default is False.

        Returns
        -------
        _species_df : pandas.DataFrame
           Pandas DataFrame with only one row containing the entry for the species.
        """
        df = self.db.df
        if exact is True:
            _species_df = df[df['English_name_AviList'] == name]
        else:
            _species_df = df[df['English_name_AviList'].str.contains(name, case=False, na=False)]

        if _species_df.shape[0] == 0:
            raise ValueError('No matching species found')
        if _species_df.shape[0] > 1:
            fail_str = f'{name} could refer to: \n'
            for _species_ in _species_df['English_name_AviList'].to_list():
                fail_str += (f'{_species_}, ')
            raise ValueError(fail_str)
        _species_df = _species_df.dropna(axis=1)
        return _species_df

    def get_subspecies(self):
        subspecies_df = self.db.df[self.db.df['Taxon_rank'] == 'subspecies']
        matching_subspecies_df = subspecies_df[subspecies_df['Scientific_name'].str.contains(self.scientific_name, case=False,na=False)]
        matching_subspecies_list = []
        for _matching_subspecies_name in matching_subspecies_df['Scientific_name'].to_list():
            matching_subspecies_list.append(Subspecies(_matching_subspecies_name, db=self.db, exact=True))
        return matching_subspecies_list