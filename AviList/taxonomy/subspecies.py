# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 13:58:39 2025

@author: Thomas Lee
Rice University
Department of Earth, Environmental, and Planetary Sciences
Email: tl165@rice.edu

AviList Citation:
AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025. https://doi.org/10.2173/avilist.v2025
"""

from AviList.data.avilistdatabase import AviListDataBase

class Subspecies():
    def __init__(self, name, exact: bool=False, db: AviListDataBase=None):
        if db is None:
            self.db = AviListDataBase()
        else:
            self.db = db
        self.df = self.lookup_subspecies(name, exact=exact)
        self._data = self.df.iloc[0].to_dict()
        self.name = self._data['Scientific_name']
        self.order = self._data['Order']
        self.family = self._data['Family']

    def __str__(self):
        return_str = f'{self["Scientific_name"]}'
        num_equals = (80 - len(return_str)) // 2
        return_str = '='*num_equals + return_str + '='*num_equals
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

    def lookup_subspecies(self, name: str, exact: bool=False):
        """
        Parameters
        ----------
        name : str
            Subspecies to search for.
        exact : bool, optional
            If True, will only search for the exact string in the data base. If False, will search
            for any string containing name as a substring, and is not case sensitive. The default is False.

        Returns
        -------
        _subspecies_df : pandas.DataFrame
           Pandas DataFrame with only one row containing the entry for the subspecies.

        """
        df = self.db.df
        if exact is True:
            _subspecies_df = df[df['Scientific_name'] == name]
        else:
            _subspecies_df = df[df['Scientific_name'].str.contains(name, case=False, na=False)]

        if _subspecies_df.shape[0] == 0:
            raise ValueError('No matching species found')
        if _subspecies_df.shape[0] > 1:
            fail_str = f'{name} could refer to: \n'
            for _subspecies_ in _subspecies_df['English_name_AviList'].to_list():
                fail_str += (f'{_subspecies_}, ')
            raise ValueError(fail_str)
        _subspecies_df = _subspecies_df.dropna(axis=1)
        return _subspecies_df