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
