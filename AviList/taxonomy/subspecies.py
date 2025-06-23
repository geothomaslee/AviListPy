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
    """Container for a Subspecies in the AviList DataBase

    The lowest taxonomic rank in the AviList.taxonomy class system. Generally,
    this class is better accessed by initializing the Species class and
    using the load_subspecies=True option, and then accessing this class inside
    the Species.subspecies attribute

    Attributes:
    -----------
    db: AviList.data.avilistdatabase.AviListDataBase
        AviListDataBase class. It is recommended to pass an existing
        AviListDataBase object to the Subspecies class during initialization,
        but if none is given it will initialize one from the Excel sheet. See
        the Setup section on the main GitHub page for more detail.
    df: Pandas.DataFrame
        The single row for this subspecies in AviList as a Pandas DataFrame.
    name: str
        Scientific name for this subspecies, from self['Scientific_name']
    order: str
        Taxonomic order
    family: str
        Taxonomic family
    genus: str
        Taxonomic genus

    Example:
        >>> db = AviListDataBase()
        >>> subspecies = Subspecies(name = "Ardea alba egretta",db=db)
        >>> subspecies.name
        'Adra alba egretta'
    """
    def __init__(self, name, exact: bool=False, db: AviListDataBase=None):
        """
        Parameters
        ----------
        name : str
            Scientific name of the subspecies to search for.
        exact : bool, optional
            If True, will only search for an exact match for the name string.
            If False, searches for name as a substring of any scientific name
            in the database, and is not case sensitive. The default is False.
        db : AviListDataBase, optional
            AviListDataBase. The default is None.
        """
        if db is None:
            self.db = AviListDataBase()
        else:
            self.db = db
        self.df = self.lookup_subspecies(name, exact=exact)
        self._data = self.df.iloc[0].to_dict()
        self.name = self._data['Scientific_name']
        self.order = self._data['Order']
        self.family = self._data['Family']
        self.genus = self.get_genus()

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
        """Returns keys in a dictionary.keys() like manner"""
        return self._data.keys()

    def values(self):
        """Returns values in a dictionary.values() like manner"""
        return self._data.values()

    def items(self):
        """Returns keys, values in a dictionary.items() like manner"""
        return self._data.items()

    def lookup_subspecies(self, name: str, exact: bool=False):
        """
        Parameters
        ----------
        name : str
            Subspecies to search for.
        exact : bool, optional
            If True, will only search for an exact match for the name string.
            If False, searches for name as a substring of any scientific name
            in the database, and is not case sensitive. The default is False.

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

    def get_genus(self):
        """Returns the genus as a string"""
        return self.name.split(' ')[0]
