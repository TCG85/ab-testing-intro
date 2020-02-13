import pandas as pd
import numpy as np

def transform_raw_data(df:pd.DataFrame) -> pd.DataFrame:
    """convenience function to transform data from long form and calculate conversions"""
    merged = df[df.action == 'installed']\
            .merge(df[df.action == 'registered'], 
                   on = 'user_id', 
                   how = 'left')\
            .sort_values(['user_id','created_at_x'], 
                         ascending = True)\
            .groupby('user_id')\
            .head(1)\
            .reset_index(drop = True)
    assert merged.user_id.nunique() == merged.shape[0], \
    "Dataframe must have one row per user_id"
    merged.drop(['action_x', 'action_y'], axis = 1, inplace = True)
    merged.columns = ['user_id', 'installed', 'registered']
    merged['time_to_convert'] = (
        merged['registered'] - merged['installed']
            ).astype('timedelta64[m]')

    merged['converted'] = (
        merged['time_to_convert'] <= 60
            ).astype(int)
    
    return merged