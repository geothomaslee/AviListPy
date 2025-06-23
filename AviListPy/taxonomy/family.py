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

from AviListPy.data.avilistdatabase import AviListDataBase
from AviListPy.taxonomy.genus import Genus

class Family():
    """Container for a Family in the AviList DataBase

    The second highest taxonomic rank in the AviList.taxonomy class
    system. Container for all Genus objects corresponding with genera
    in this family. See Family.keys() for a list of all available data. Can
    access data in a dictionary-like manner where keys are columns in the
    AviList, but iterating will iterate through Family.genera

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
        >>> family = Family('Anatidae',db=db)
        >>> family.name
        'Anatidae'
        >>> family['Family_English_name']
        'Ducks, Swans, and Geese'

    """
    def __init__(self, name: str, exact: bool=False, load_subspecies: bool=False, db: AviListDataBase=None):
        """
        Parameters
        ----------
        name : str
            Scientific name of the family to search for.
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
        self.df = self.lookup_family(name, exact=exact)
        self._data = self.df.iloc[0].to_dict()
        self.name = self._data['Scientific_name']
        self.order = self._data['Order']
        self.genera = self.find_matching_genera(load_subspecies=load_subspecies)
        self.species = self.find_matching_species()

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
        return iter(self.genera)

    def __len__(self):
        return len(self.genera)

    def keys(self):
        """Returns keys in a dictionary.keys() like manner"""
        return self._data.keys()

    def values(self):
        """Returns values in a dictionary.values() like manner"""
        return self._data.values()

    def items(self):
        """Returns keys, values in a dictionary.items() like manner"""
        return self._data.items()

    def lookup_family(self, name, exact: bool=False):
        """
        Parameters
        ----------
        name : str
            Family to search for.
        exact : bool, optional
            If True, will only search for an exact match for the name string.
            If False, searches for name as a substring of any scientific name
            in the database, and is not case sensitive. The default is False.

        Returns
        -------
        _family_df : pandas.DataFrame
           Pandas DataFrame with only one row containing the entry for the family.

        """
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

    def find_matching_genera(self, load_subspecies: bool=False):
        """
        Parameters
        ----------
            If True, loads subspecies. The default is False.

        Returns
        -------
        matching_genera_list : list of AviList.taxonomy.genus.Genus
            List of genera contained within the order.
        """
        genus_df = self.db.df[self.db.df['Taxon_rank'] == 'genus']
        matching_genus_df = genus_df[genus_df['Family'] == str(self.name)]
        print(f'Loading {len(matching_genus_df)} genera in family {self.name}')
        if len(matching_genus_df) == 0:
            raise ValueError('No matching genera found')
        matching_genera_list = []
        for _matching_genus_name in matching_genus_df['Scientific_name'].to_list():
            matching_genera_list.append(Genus(_matching_genus_name, db=self.db, exact=True, load_subspecies=load_subspecies))
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
