#!/usr/bin/env python

from os import path, walk
import os
from logger import Logger
from fnmatch import filter
import pandas as pd
import numpy as np



logger = Logger().get_logger()  # initiating logger


class BioChemData(object):
    def __init__(self, root_path, pattern):
        logger.info('Initiating FileManager object')
        self.root_path = root_path
        self.pattern = pattern
        self.rf_list = []  # create empty list to store file locations
        self.all_readerfiles = []

    #def populate_data(self):
     #   logger.info('Create a list of files to read in')
      #  for root, dirs, files in walk(self.root_path):
       #     for filename in filter(files, self.pattern):
        #        return self.rf_list.append(path.join(root, filename))
    def analyze_biochem(self):
        logger.info('extracting data')

        for root, dir, files in walk(self.root_path):
            for filename in filter(files, self.pattern):
                self.rf_list.append(path.join(root, filename))

        for readerfiles in self.rf_list:
            df = pd.read_csv(readerfiles)

            cycle_1 = df.filter(regex=("_1$"))
            cycle_2 = df.filter(regex=("_2$"))

            if 'biochem2' in readerfiles:
                print("biochem2")
                self.modify_biochem2(cycle_1)
                self.modify_biochem2(cycle_2)
            else:
                print("biochem1")
                self.modify_biochem1(cycle_1)
                self.modify_biochem1(cycle_2)

            self.calculate_accuracy(cycle_1)
            self.calculate_accuracy(cycle_2)

            cycle_1.to_csv(os.path.basename(readerfiles + '_cycle1.csv'))
            cycle_2.to_csv(os.path.basename(readerfiles + '_cycle2.csv'))


    def modify_biochem2(self, df):
        logger.info('Modifying column names for biochem2')

        df.rename(columns={'ref_1':'ref', 'A_1': 'C', 'C_1': 'G', 'G_1': 'T', 'T_1': 'A',
                           'ref_2':'ref','A_2': 'C', 'C_2': 'G', 'G_2': 'T', 'T_2': 'A'},
                      inplace=True)

        self.generate_calls(df)
        #df['calls'][df[['A', 'C', 'G', 'T']].sum(axis=1) == 0] = 'N'

    def modify_biochem1(self, df):
        logger.info('Modifying column names for biochem1')
        df.rename(columns={'ref_1':'ref','A_1': 'A', 'C_1': 'C', 'G_1': 'G', 'T_1': 'T',
                           'ref_2':'ref','A_2': 'A', 'C_2': 'C', 'G_2': 'G', 'T_2': 'T'},
                  inplace=True)

        self.generate_calls(df)
        df['calls'][df[['A', 'C', 'G', 'T']].sum(axis=1) == 0] = 'N'

    def generate_calls(self,df):
        logger.info('generating call')

        df['calls'] = df[['A', 'C', 'G', 'T']].idxmax(axis=1)

    def calculate_accuracy(self, df):
        df['accuracy'] = np.where(df['calls'] == df['ref'], 1, 0)





