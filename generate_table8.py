# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 18:38:58 2024

@author: dohyeon
"""


import pandas as pd
import numpy as np
import user_utils as uu


temp_df = pd.read_csv(r'whole_dataset_empirical_validity_0119.csv', index_col=0)
temp_df1 = pd.read_csv(r'elite_dataset_empirical_validity_0119.csv', index_col=0)


temp_obj = uu.load_gpickle(r'state_speed_dist_0119.pickle')
temp_obj1 = uu.load_gpickle(r'elite_state_start_speed_0119.pickle')


#%%
for xx in temp_obj.keys():
    if not xx in ['H','X']:
        temp_df.loc[xx, 'cnt'] = len(temp_obj[xx])

#%%


#%%
for xx in temp_obj1.keys():
    if not xx in ['H','X']:
        temp_df1.loc[xx, 'cnt'] = len(temp_obj1[xx])
#%%

temp_df1.columns = ['elite_imp', 'elite_avg_sp', 'elite_imp_rank', 'elite_avg_sp_rank', 'elite_cnt']

#%%

new_temp_df = pd.concat([temp_df, temp_df1[temp_df1.columns[1:]]], axis=1)
new_temp_df['diff_avg_sp'] = new_temp_df.elite_avg_sp - new_temp_df.avg_sp

#%%

new_temp_df.columns

new_temp_df[['imp','imp_rank','avg_sp','avg_sp_rank','cnt','elite_avg_sp','elite_avg_sp_rank','elite_cnt','diff_avg_sp']].sort_values(by='imp_rank',ascending=True).to_csv(r'table_8.csv')
