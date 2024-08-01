# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 18:08:04 2024

@author: dohyeon
"""


import pandas as pd
import numpy as np
import user_utils as uu


temp_df = pd.read_csv(r'whole_dataset_empirical_validity_0119.csv', index_col=0)
temp_obj = uu.load_gpickle(r'state_speed_dist_0119.pickle')

#%%
for xx in temp_obj.keys():
    if not xx in ['H','X']:
        temp_df.loc[xx, 'cnt'] = len(temp_obj[xx])

#%%
new_temp_df = temp_df.sort_values(by='imp_rank',ascending=True)


new_temp_df[['imp','imp_rank','avg_sp','avg_sp_rank','cnt']].to_csv(r'table_7.csv')
