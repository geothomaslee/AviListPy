# -*- coding: utf-8 -*-
"""
Created on Sun Jun 22 11:31:20 2025

@author: Thomas Lee
Rice University
Department of Earth, Environmental, and Planetary Sciences
Email: tl165@rice.edu

AviList Citation:
AviList Core Team. 2025. AviList: The Global Avian Checklist, v2025. https://doi.org/10.2173/avilist.v2025
"""
import os
from importlib import resources
from datetime import datetime
import pickle
import pandas as pd

from pandas import DataFrame

class AviListDataBase():
    def __init__(self, path: str=None, overwrite_existing=False, verbose=False) -> None:
        def verbose_print(*args, **kwargs):
            """Helper function that only prints if verbose is True"""
            if verbose:
                print(*args, **kwargs)

        if overwrite_existing is True or path is None:
            if path is not None and os.path.exists(path) is False:
                print(f'Could not find database at {path}. Creating a new database, and saving it there')
            verbose_print('Loading database...')
            start_time = datetime.now()
            self.df = self.load_df()
            verbose_print(f'Database loaded in {datetime.now() - start_time}')
            if path is not None:
                self._save(path)
        else:
            start_time = datetime.now()
            try:
                with open(path, 'rb') as f:
                    saved_version = pickle.load(f)
                self.__dict__.update(saved_version.__dict__)
                verbose_print(f'Database loaded in {datetime.now() - start_time}')
            except FileNotFoundError:
                verbose_print('Could not find pickled database, initializing new...')
                self.df = self.load_df()
                verbose_print(f'Database loaded in {datetime.now() - start_time}')

    def load_df(self) -> pd.DataFrame:
        """Loads the AviList Excel file as a Pandas DataFrame"""
        with resources.files('AviListPy.data').joinpath('AviList-v2025-11Jun-extended.xlsx').open('rb') as f:
            return pd.read_excel(f)

    def _save(self, path=None) -> None:
        """Pickles the AviListDataBase to the disk"""
        if path is None:
            raise ValueError('Must define path to save AviListDataBase.db to')
        try:
            with open(path, 'wb') as file:
                pickle.dump(self, file)
        except FileNotFoundError as e:
            raise ValueError(f'FileNotFoundError raised. Likely that the parent directory for your database save location does not exist: \n: {str(e)}')

    def keys(self):
        """Returns all columns in the data base"""
        return self.df.columns.tolist()

    def query(self, search, category: str=None, exact: bool=False) -> DataFrame:
        if exact is True:
            return_df = self._exact_search(search=search,category=category)
        else:
            return_df = self._substring_search(search=search,category=category)

        print(f'Search resulted in {len(return_df)} entries')

        return return_df

    def _exact_search(self, search: str, category: str) -> DataFrame:
        try:
            if category is None:
                return_df = self.df[self.df.isin([search]).any(axis=1)]
            else:
                return_df = self.df[self.df[category] == search]
        except KeyError:
            raise KeyError(f'Invalid category. Valid categories are {self.keys()}')

        return return_df

    def _substring_search(self, search: str, category: str) -> DataFrame:
        try:
            if category is None:
                df_str = self.df.astype(str)
                mask = df_str.apply(lambda col: col.str.contains(search, na=False, case=False)).any(axis=1)
                return_df = self.df[mask]
            else:
                return_df = self.df[self.df[category].str.contains(search, case=False, na=False)]
        except KeyError:
            raise KeyError(f'Invalid category. Valid categories are {self.keys()}')

        return return_df