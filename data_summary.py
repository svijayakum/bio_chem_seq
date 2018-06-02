from os import path, walk
from pprint import pprint
from logger import Logger
from fnmatch import filter
import pandas as pd

logger = Logger().get_logger()  # initiating logger

class DataSummary(object):
    def __init__(self, root_path, pattern):
        logger.info('Initiating FileManager object')
        self.root_path = root_path
        self.pattern = pattern
        self.rf_list = []  # create empty list to store file locations
        self.tab = []


    def generate_summary(self):
        logger.info('generating summary')

        for root, dir, files in walk(self.root_path):
            for filename in filter(files, self.pattern):
                self.rf_list.append(path.join(root, filename))

        for readerfiles in self.rf_list:
            df = pd.read_csv(readerfiles)

            error_rate = self.calculate_error_rate(df)
            self.tab.append(error_rate)
        pprint(self.tab)




    def histogram(self, df):
        pd.Series(df['calls']).value_counts().plot('bar')

    def calculate_error_rate(self, df):
        accuracy_score = (float(sum(df['accuracy'])) / float(len(df['accuracy']))) * 100
        error_rate = round(100 - accuracy_score,2)
        return error_rate

        return pd.DataFrame({'accurace': accuracy_score, 'error_rate': error_rate})

    # def freq_graph(self,df):


