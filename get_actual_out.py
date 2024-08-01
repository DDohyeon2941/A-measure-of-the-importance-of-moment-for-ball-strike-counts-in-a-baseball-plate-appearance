# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 16:40:02 2024

@author: dohyeon
"""


import numpy as np
import pandas as pd

episode = pd.read_pickle('episode_list_0119_f_index.pkl')
episode

count_list = [(0,0), (0,1), (1,0), (0,2), (1,1), (2,0), (1,2), (2,1), (3,0), (2,2), (3,1), (3,2)]
count_list = [str(xx) for xx in count_list]
#%%

trans_matrix = np.zeros((len(count_list),len(count_list)))
out_dict = dict(zip(count_list, [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]))
result_df = pd.DataFrame(data=np.zeros((len(count_list),2)), index=count_list, columns=['X','H'])
for _, (row_fmode, row_end) in (episode[['f_mode','E']][:]).iterrows():
    #print(row_fmode, row_end)
    if len(row_fmode)<1:
        result_df.loc['(0, 0)',row_end] +=1
    else:
        bs = np.array([0,0])
        result_df.loc['(0, 0)',row_end] +=1
        for u_c in row_fmode:
            if u_c ==  'B':
                bs[0] += 1
            elif u_c == 'S':
                bs[1] += 1
            bs_idx = str(tuple(bs))
            #print(bs_idx, row_end)
            result_df.loc[bs_idx, row_end] +=1
#%%

result_df['total']= result_df.X + result_df.H
result_df['actual'] = result_df.X / result_df.total

#%%

result_df.to_csv(r'actual_out_prob.csv')
