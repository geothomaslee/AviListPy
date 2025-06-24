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

from AviListPy.data.avilistdatabase import AviListDataBase
from AviListPy.taxonomy.subspecies import Subspecies
from typing import Any, KeysView, ValuesView, ItemsView, List
from pandas import DataFrame

class Species():
    """Container for a Species in the AviList DataBase

    The second lowest taxonomic rank in the AviList.taxonomy class system. This
    class is initialized with the English name for the species. This will be
    updated to support initializing with the scientific name in the future.

    Attributes:
    -----------
    db: AviList.data.avilistdatabase.AviListDataBase
        AviListDataBase class. It is recommended to pass an existing
        AviListDataBase object to the Species class during initialization,
        but if none is given it will initialize one from the Excel sheet. See
        the Setup section on the main GitHub page for more detail.
    df: Pandas.DataFrame
        The single row for this subspecies in AviList as a Pandas DataFrame.
    name: str
        English name for this species, from self['English_name_AviList']
    scientific_name: str
        Scientific name for this subspecies, from self['Scientific_name']
    order: str
        Taxonomic order
    family: str
        Taxonomic family
    genus: str
        Taxonomic genus
    subspecies: list of AviList.taxonomy.subspecies.Subspecies, or None
        If load_subspecies is False, then None. If True, then list of
        Subspecies objects.

    Example:
        >>> db = AviListDataBase()
        >>> species = Species(name = "Great Egret",db=db)
        >>> subspecies.name
        'Great Egret'
        >>> subspecies['Bibliographic_details']
        'Systema Naturæ per Regna Tria Naturæ, Secundum Classes, Ordines,
        Genera, Species, cum Characteribus, Differentiis, Synonymis, Locis.
        Tomus I. Editio decima, reformata 1 p.144'
    """
    def __init__(self, name: str, exact: bool=False, load_subspecies=False, db: AviListDataBase=None):
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
            If True, will load Subspecies objects for each subspecies and write
            them in a list to Species.subspecies
        db : AviListDataBase, optional
            AviListDataBase. The default is None.
        """
        if db is None:
            self.db = AviListDataBase()
        else:
            self.db = db
        self.df = self.lookup_species(name, exact=exact)
        self._data = self.df.iloc[0].to_dict()
        self.name = self._data['English_name_AviList']
        self.scientific_name = self._data['Scientific_name']
        self.order = self._data['Order']
        self.family = self._data['Family']
        self.genus = self.get_genus()
        self.subspecies = None

        if load_subspecies is True:
            self.subspecies = self.get_subspecies()

    def __str__(self) -> str:
        return_str = f'{self["English_name_AviList"]}'
        num_equals = (80 - len(return_str)) // 2
        return_str = '='*num_equals + return_str + '='*num_equals
        if self.subspecies is not None:
            return_str += f'\nContains {len(self.subspecies)} subspecies'
        for key, val in self.items():
            return_str += (f'\n{key}: {val}')
        return return_str + '\n'

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

    def lookup_species(self, name: str, exact: bool=False) -> DataFrame:
        """
        Parameters
        ----------
        name : str
            Species to search for.
        exact : bool, optional
            If True, will only search for an exact match for the name string.
            If False, searches for name as a substring of any scientific name
            in the database, and is not case sensitive. The default is False.

        Returns
        -------
        _species_df : pandas.DataFrame
           Pandas DataFrame with only one row containing the entry for the species.
        """
        df = self.db.df

        # First we search for a matching English name
        try:
            if exact is True:
                _species_df = df[df['English_name_AviList'] == name]
            else:
                _species_df = df[df['English_name_AviList'].str.contains(name, case=False, na=False)]

            if _species_df.shape[0] == 0:
                raise ValueError('No matching species found')
        except ValueError as e:
            # We only want to search for scientific name if the English name
            # search doesn't return any results
            if str(e) == 'No matching species found':
                # Scientific name will always be a substring of the subspecies
                # We need to limit our results to only species
                if exact is True:
                    _species_df = df[df['Scientific_name'] == name]
                    _species_df = _species_df[_species_df['Taxon_rank'] == 'species']
                else:
                    _species_df = df[df['Scientific_name'].str.contains(name, case=False, na=False)]
                    _species_df = _species_df[_species_df['Taxon_rank'] == 'species']

        if _species_df.shape[0] == 0:
            raise ValueError('No matching species found')

        if _species_df.shape[0] > 1:
            fail_str = f'{name} could refer to: \n'
            for _species_ in _species_df['English_name_AviList'].to_list():
                fail_str += (f'{_species_}, ')
            raise ValueError(fail_str)

        # Drop nan columns
        _species_df = _species_df.dropna(axis=1)

        return _species_df

    def get_subspecies(self) -> List[Subspecies]:
        """Pulls all subspecies for this species and writes them as a list of
        AviList.taxonomy.subspecies.Subspecies objects to Species.subspecies"""
        subspecies_df = self.db.df[self.db.df['Taxon_rank'] == 'subspecies']
        matching_subspecies_df = subspecies_df[subspecies_df['Scientific_name'].str.contains(self.scientific_name, case=False,na=False)]
        matching_subspecies_list = []
        for _matching_subspecies_name in matching_subspecies_df['Scientific_name'].to_list():
            matching_subspecies_list.append(Subspecies(_matching_subspecies_name, db=self.db, exact=True))
        return matching_subspecies_list

    def get_genus(self) -> str:
        """Returns the genus of this species as a string"""
        return self.scientific_name.split(' ')[0]

    def brief_summary(self) -> str:
        """Returns a short, easily readable version of info about this species"""
        return_str = f'{self["English_name_AviList"]}'
        num_equals = (80 - len(return_str)) // 2
        return_str = '='*num_equals + return_str + '='*num_equals
        return_str += f"\nScientific Name: {self['Scientific_name']}"
        if self.subspecies is not None:
            return_str += f"\n{len(self.subspecies)} Subspecies: "
            for subspecies in self.subspecies:
                return_str += f"{subspecies.name}, "
        return_str += f"\nOrder: {self.order}"
        return_str += f"\nFamily: {self.family}: {self['Family_English_name']}"
        try:
            return_str += f"\nRange: {self['Range']}"
        except KeyError:
            return_str += "\nRange Not Specified"
        return return_str + '\n'
