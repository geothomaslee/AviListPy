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
    """Container for a Genus in the AviList DataBase

    The third lowest/highest taxonomic rank in the AviList.taxonomy class
    system. Container for all Species objects corresponding with species
    in this genus. See Genus.keys() for a list of all available data. Can
    access data in a dictionary-like manner where keys are columns in the
    AviList, but iterating will iterate through Genus.species()

    Attributes:
    -----------
    db: AviList.data.avilistdatabase.AviListDataBase
        AviListDataBase class. It is recommended to pass an existing
        AviListDataBase object to the Genus class during initialization,
        but if none is given it will initialize one from the Excel sheet. See
        the Setup section on the main GitHub page for more detail.
    df: Pandas.DataFrame
        The single row for this genus in AviList as a Pandas DataFrame.
    name: str
        Scientific name for this genus, from self['Scientific_name']
    order: str
        Taxonomic order
    family: str
        Taxonomic family
    species: list of AviList.taxonomy.species.Species, or None

    Example:
        >>> db = AviListDataBase()
        >>> genus = Genus('Ardea',db=db)
        >>> genus.name
        'Ardea'
    """
    def __init__(self, name: str, exact: bool=False, load_subspecies: bool=False, db: AviListDataBase=None):
        """
        Parameters
        ----------
        name : str
            English name of the species to search for.
        exact : bool, optional
            If True, will only search for an exact match for the name string.
            If False, searches for name as a substring of any English name
            in the database, and is not case sensitive. The default is False.
        load_subspecies: bool, optional
            If True, will load Subspecies objects while loading Species. See
            AviList.taxonomy.species.Species for more information.
        db : AviListDataBase, optional
            AviListDataBase. The default is None.
        """
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

    def __iter__(self):
        return iter(self.species)

    def __len__(self):
        return len(self.species)

    def keys(self):
        """Returns keys in a dictionary.keys() like manner"""
        return self._data.keys()

    def values(self):
        """Returns values in a dictionary.values() like manner"""
        return self._data.values()

    def items(self):
        """Returns keys, values in a dictionary.items() like manner"""
        return self._data.items()

    def lookup_genus(self, name, exact: bool=False):
        """
        Parameters
        ----------
        name : str
            Genus to search for.
        exact : bool, optional
            If True, will only search for an exact match for the name string.
            If False, searches for name as a substring of any scientific name
            in the database, and is not case sensitive. The default is False.

        Returns
        -------
        _genus_df : pandas.DataFrame
           Pandas DataFrame with only one row containing the entry for the genus.

        """
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
        """
        Parameters
        ----------
        exact : bool, optional
            If True, will only search for an exact match for the name string.
            If False, searches for name as a substring of any scientific name
            in the database, and is not case sensitive. The default is False.
        load_subspecies : bool, optional
            If True, loads subspecies. The default is False.

        Returns
        -------
        matching_species_list : list of AviList.taxonomy.species.Species
            List of species contained within the order.
        """
        species_df = self.db.df[self.db.df['Taxon_rank'] == 'species']
        matching_species_df = species_df[species_df['Scientific_name'].str.contains(self.name)]
        matching_species_list = []
        for _matching_species_name in matching_species_df['English_name_AviList'].to_list():
            matching_species_list.append(Species(_matching_species_name, db = self.db, exact=True, load_subspecies=load_subspecies))
        return matching_species_list

    def show_species(self):
        """Prints each species in this genus"""
        for species in self.species:
            print(species)
