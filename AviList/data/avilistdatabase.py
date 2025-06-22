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

from importlib import resources
from datetime import datetime
import pickle
import pandas as pd

class AviListDataBase():
    def __init__(self, overwrite_existing=False, verbose=False):
        def verbose_print(*args, **kwargs):
            """Helper function that only prints if verbose is True"""
            if verbose:
                print(*args, **kwargs)

        if overwrite_existing is True:
            verbose_print('Loading database...')
            start_time = datetime.now()
            self.df = self.load_df()
            verbose_print(f'Database loaded in {datetime.now() - start_time}')
        else:
            start_time = datetime.now()
            try:
                with resources.files('AviList.data').joinpath('AviListDataBase.pickle').open('rb') as f:
                    saved_version = pickle.load(f)
                    self.__dict__.update(saved_version.__dict__)
                verbose_print(f'Database loaded in {datetime.now() - start_time}')
            except FileNotFoundError:
                verbose_print('Could not find pickled database, initializing new...')
                self.df = self.load_df()
                verbose_print(f'Database loaded in {datetime.now() - start_time}')

    def load_df(self):
        with resources.files('AviList.data').joinpath('AviList-v2025-11Jun-extended.xlsx').open('rb') as f:
            return pd.read_excel(f)

    def _save(self, path=None, i_know_what_im_doing=False):
        if i_know_what_im_doing is False:
            raise ValueError('_save is a developer method for pickling the database as an AviListDataBase object. ' \
                             'This is better than just reading the excel file from the AviList team directly ' \
                             'because it brings the loading time for that file from 10 seconds to a few milliseconds, ' \
                             'allowing for the general structure of this package to work'
                             'This package ships with a pickled version of this database, and will be updated as AviList is. ' \
                             'This function generally should never need to be called by end users. ' \
                             'However, if you have need to for some reason, set i_know_what_im_doing=True in AviListDataBase._save()')
        if path is None:
            raise ValueError('Must define path to save AviListDataBase.pickle to')
        with open(path, 'wb') as file:
            pickle.dump(self, file)
