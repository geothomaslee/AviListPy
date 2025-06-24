# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 14:25:46 2025

@author: Thomas Lee
Rice University
Department of Earth, Environmental, and Planetary Sciences
Email: tl165@rice.edu
"""

from AviListPy.taxonomy.family import Family, Genus, Species
from AviListPy.data.avilistdatabase import AviListDataBase
from typing import Any, KeysView, ValuesView, ItemsView, Iterator, List
from pandas import DataFrame

class Order():
    """Container for a Family in the AviList DataBase

    The highest taxonomic rank in the AviList.taxonomy class system. Container
    for all family objects corresponding with family
    in this order. See Order.keys() for a list of all available data. Can
    access data in a dictionary-like manner where keys are columns in the
    AviList, but iterating will iterate through Order.families

    Attributes:
    -----------
    db: AviList.data.avilistdatabase.AviListDataBase
        AviListDataBase class. It is recommended to pass an existing
        AviListDataBase object to the Family class during initialization,
        but if none is given it will initialize one from the Excel sheet. See
        the Setup section on the main GitHub page for more detail.
    df: Pandas.DataFrame
        The single row for this family in AviList as a Pandas DataFrame.
    name: str
        Scientific name for this family, from self['Scientific_name']
    order: str
        Taxonomic order
    family: str
        Taxonomic family
    genera: list of AviList.taxonomy.genus.Genus
        All genera within this family.
    species: list of AviList.taxonomy.species.Species
        All species within this family.

    Example:
        >>> db = AviListDataBase()
        >>> order = Order('Anseriformes',db=db)
        >>> order.name
        'Anseriformes'
        >>> order['Sequence']
        230

    """
    def __init__(self, name: str, exact: bool=False, load_subspecies: bool=False, db: AviListDataBase=None):
        """
        Parameters
        ----------
        name : str
            Scientific name of the species to search for.
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
        self.df = self.lookup_order(name)
        self._data = self.df.iloc[0].to_dict()
        self.name = self._data['Scientific_name']
        self.families = self.find_matching_families(load_subspecies=load_subspecies)
        self.genera = self.find_matching_genera()
        self.species = self.find_matching_species()

    def __str__(self) -> str:
        return_str = f'{self.name}'
        num_equals = (80 - len(return_str)) // 2
        return_str = '='*num_equals + return_str + '='*num_equals
        return_str += f'\n{len(self.species)} species in {len(self.genera)} genera across {len(self.families)} families'
        for key, val in self.items():
            return_str += (f'\n{key}: {val}')
        return return_str + '\n'

    def __iter__(self) -> Iterator[Any]:
        return iter(self.families)

    def __len__(self) -> int:
        return len(self.families)

    def __getitem__(self, key) -> Any:
        return self._data[key]

    def __setitem__(self, key, value) -> None:
        self._data[key] = value

    def __contains__(self, key) -> bool:
        return key in self._data

    def keys(self) -> KeysView:
        """Returns keys in a dictionary.keys() like manner"""
        return self._data.keys()

    def values(self) -> ValuesView:
        """Returns values in a dictionary.values() like manner"""
        return self._data.values()

    def items(self) -> ItemsView:
        """Returns keys, values in a dictionary.items() like manner"""
        return self._data.items()

    def lookup_order(self, name) -> DataFrame:
        """
        Parameters
        ----------
        name : str
            Order to search for.
        exact : bool, optional
            If True, will only search for an exact match for the name string.
            If False, searches for name as a substring of any scientific name
            in the database, and is not case sensitive. The default is False.

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

    def find_matching_families(self, load_subspecies: bool=False) -> List[Family]:
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
            matching_family_list.append(Family(_matching_family_name, db=self.db, exact=True, load_subspecies=load_subspecies))
        return matching_family_list

    def find_matching_genera(self) -> List[Genus]:
        """Returns a list of all genera in this order as Genus objects"""
        genera_list = []
        for family in self.families:
            genera_list += family.genera
        return genera_list

    def find_matching_species(self) -> List[Species]:
        """Returns a list of all species in this order as Species objects"""
        species_list = []
        for genus in self.genera:
            species_list += genus.species
        return species_list

    def show_families(self) -> None:
        print(f'{len(self.families)} family in order {self.name}')
        count = 0
        for family in self.families:
            print(f'{family.name}: {len(family.genera)} genera, {len(family.species)} species')
            count += len(family.species)
        print(f'{count} total species in {self.name}')

    def show_genera(self) -> None:
        print(f'{len(self.genera)} genera in family {self.name}')
        count = 0
        for genus in self.genera:
            print(f'{genus.name}: {len(genus.species)} species')
            count += len(genus.species)
        print(f'{count} total species in {self.name}')