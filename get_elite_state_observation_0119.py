# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 19:42:32 2023

@author: dohyeon
"""

import user_utils as uu
import pandas as pd
import numpy as np

temp_obj = pd.read_pickle(r'episode_list_0119_f_index.pkl')




#%%



temp_df = pd.read_csv(r'elite_id_unique.csv')


elite_df = temp_obj.loc[temp_obj.pitcher_id.isin(temp_df.id.values)].reset_index(drop=True)



#%%


process_list = [(0,0), (0,1), (1,0), (0,2), (1,1), (2,0), (1,2), (2,1), (3,0), (2,2), (3,1), (3,2),'H','X']
process_list = [str(xx) for xx in process_list]

trans_matrix = np.zeros((len(process_list),len(process_list)))
speed_dict = dict(zip(process_list, [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]))


result_df = pd.DataFrame(data=trans_matrix, index=process_list, columns=process_list)

#%% 4. 각 state별 직구일때 시작구속 정보 추출


for _, (row_fmode, row_fpmode, row_sspd, row_end) in elite_df[['f_mode','f_pmode','f_sspd','E']].iterrows():
    if len(row_fmode)<1:
        result_df.loc['(0, 0)',row_end] +=1
        if row_fpmode == 'D':
            speed_dict['(0, 0)'].append(row_sspd[0])
    else:
        from_bs = np.array([0,0])
        for u_c, u_d, u_ss in zip(row_fmode, row_fpmode[:-1], row_sspd[:-1]):
            from_idx = str(tuple(from_bs))
            if u_d == 'D':
                speed_dict[from_idx].append(u_ss)
            if u_c ==  'B':
                from_bs[0] += 1
            elif u_c == 'S':
                from_bs[1] += 1
            to_bs = from_bs
            to_idx = str(tuple(to_bs))

            result_df.loc[from_idx, to_idx] +=1
        result_df.loc[to_idx, row_end] +=1
        if row_fpmode[-1] == 'D':
            speed_dict[to_idx].append(row_sspd[-1])

#%%


result_df_ratio = (result_df / result_df.sum(axis=1).values.reshape(-1,1))

#%%

uu.save_gpickle(r'elite_state_start_speed_0119.pickle',speed_dict)

result_df_ratio.to_csv(r'elite_state_ratio_0119.csv')


