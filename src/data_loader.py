import pandas as pd
from .config import FILE_I

def load_data():
    """
    Loads the aggregate + appliance consumption data.
    Returns a DataFrame.
    """
    df = pd.read_csv(FILE_I)
    df['UNIX_TS'] = pd.to_datetime(df['UNIX_TS'], unit='s')
    df.set_index('UNIX_TS', inplace=True)
    return df
