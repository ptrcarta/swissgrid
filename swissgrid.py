import pandas as pd
import os
DATA_DIR = 'data/'

def _col_names(fname):
    columns = pd.read_excel(
        fname,
        sheet_name=2).columns[1:]
    columns = columns.str.split('\n').map(lambda l: l[-1]) #use english names
    return columns

def _load():
    years = []
    for fname in os.listdir(DATA_DIR):
        if '.xls' in fname:
            year_data = pd.read_excel(
                        DATA_DIR + fname,
                        sheet_name = 2,
                        skiprows = 2,
                        index_col = 0
            )
            year_data.columns = _col_names(DATA_DIR + fname)
            years.append(year_data)
    d = pd.concat(years, sort=False)
    d.index.name = 'time'
    d = d.sort_index()
    #resample to get equally spaced (get rid of few holes and errors)
    return d.resample('15 min').first()

_serialized = DATA_DIR + 'griddata.pkl'
try:
    grid_data = pd.read_pickle(_serialized)
except:
    grid_data = _load()
    grid_data.to_pickle(_serialized)
