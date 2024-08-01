# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:25:12 2024

@author: dohyeon
"""


import numpy as np
import pandas as pd

temp_obj = pd.read_pickle(r'episode_list_0119_f_index.pkl')
#temp_obj1 = pd.read_pickle(r'episode_list_0119.pkl')


temp_obj.head(3).T
#temp_obj1.head(3).T

temp_obj['str_f_mode'] = [''.join(xx) for xx in temp_obj.f_mode]

temp_obj.loc[temp_obj.str_f_mode == ''].head(3).T

#%%

independence_table = pd.DataFrame(index=['1,1|0,1','1,1|1,0',
                                          '1,2|0,2','1,2|1,1',
                                          '2,1|1,1','2,1|2,0',
                                          '2,2|1,2','2,2|2,1',
                                          '3,1|2,1','3,1|3,0',
                                          '3,2|2,2','3,2|3,1',],
                                  columns=['out_prob.', 'out_observation',
                                           'base_prob.', 'base_observation', 'total_observation'
                                           ])
independence_table

#%%

#temp_obj[temp_obj['str_f_mode'].str.contains(r"^SBS")]

def get_cond_num(episode_data, col1, col2, str1, str2):
    output = episode_data[(episode_data[col1].str.contains(str1)) & (episode_data[col2]==str2)].shape[0]
    return output

def get_cond_result(episode_data, col1, col2, str1):
    out_num = get_cond_num(episode_data, col1, col2, str1, 'X')
    base_num = get_cond_num(episode_data, col1, col2, str1, 'H')
    total_num = out_num + base_num
    return [out_num/total_num, out_num, base_num/total_num, base_num, total_num]

#%%
#1) 1,1
### 11 from 01(SB)
independence_table.loc['1,1|0,1'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^SB")
### 11 from 10(BS)
independence_table.loc['1,1|1,0'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^BS")

#2) 1,2
### 12 from 02(SSB)
independence_table.loc['1,2|0,2'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^SSB")
### 12 from 11(SB or BS)
independence_table.loc['1,2|1,1'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^(?:SB|BS)S")

#3) 2,1
### 21 from 11(SBS or BSS)
independence_table.loc['2,1|1,1'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^(?:SB|BS)B")
### 21 from 20(BBS)
independence_table.loc['2,1|2,0'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^BBS")


#4) 2,2
### 22 from 12(SSB or SBS or BSS)
independence_table.loc['2,2|1,2'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^(?:SSB|SBS|BSS)B")

### 22 from 21(SBB or BSB or BBS)
independence_table.loc['2,2|2,1'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^(?:SBB|BSB|BBS)S")


#5) 3,1
### 31 from 21(SBB or BSB or BBS)
independence_table.loc['3,1|2,1'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^(?:SBB|BSB|BBS)B")

### 31 from 30(BBBS)
independence_table.loc['3,1|3,0'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^BBBS")

#6) 3,2
### 32 from 22(SSBB or SBSB or SBBS or BSBS or BSSB or BBSS)
independence_table.loc['3,2|2,2'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^(?:SSBB|SBSB|SBBS|BSBS|BSSB|BBSS)B")

### 32 from 31(SBBB or BSBB or BBSB or BBBS)
independence_table.loc['3,2|3,1'] = get_cond_result(temp_obj, 'str_f_mode', 'E', r"^(?:SBBB|BSBB|BBSB|BBBS)S")

#%%

def get_z_stats(p1, n1, p2, n2):
    return  (p1 - p2) / ((p1*(1-p1)/n1 + p2*(1-p2)/n2)**0.5)

#%%

z_df = pd.DataFrame(index=['1,1','1,2','2,1','2,2','3,1','3,2'], columns=['zstat','pvalue'])
#1,1
z_df.loc['1,1','zstat'] = get_z_stats(independence_table.loc['1,1|0,1','out_prob.'],
            independence_table.loc['1,1|0,1','total_observation'],
            independence_table.loc['1,1|1,0','out_prob.'],
            independence_table.loc['1,1|1,0','total_observation'])

#1,2
z_df.loc['1,2','zstat'] = get_z_stats(independence_table.loc['1,2|0,2','out_prob.'],
            independence_table.loc['1,2|0,2','total_observation'],
            independence_table.loc['1,2|1,1','out_prob.'],
            independence_table.loc['1,2|1,1','total_observation'])

#2,1
z_df.loc['2,1','zstat'] = get_z_stats(independence_table.loc['2,1|1,1','out_prob.'],
            independence_table.loc['2,1|1,1','total_observation'],
            independence_table.loc['2,1|2,0','out_prob.'],
            independence_table.loc['2,1|2,0','total_observation'])

#2,2
z_df.loc['2,2','zstat'] = get_z_stats(independence_table.loc['2,2|1,2','out_prob.'],
            independence_table.loc['2,2|1,2','total_observation'],
            independence_table.loc['2,2|2,1','out_prob.'],
            independence_table.loc['2,2|2,1','total_observation'])

#3,1
z_df.loc['3,1','zstat'] = get_z_stats(independence_table.loc['3,1|2,1','out_prob.'],
            independence_table.loc['3,1|2,1','total_observation'],
            independence_table.loc['3,1|3,0','out_prob.'],
            independence_table.loc['3,1|3,0','total_observation'])

#3,2
z_df.loc['3,2','zstat'] = get_z_stats(independence_table.loc['3,2|2,2','out_prob.'],
            independence_table.loc['3,2|2,2','total_observation'],
            independence_table.loc['3,2|3,1','out_prob.'],
            independence_table.loc['3,2|3,1','total_observation'])



#%%

from scipy.stats import norm


z_df.loc[:,'pvalue'] = [norm.sf(abs(xx))*2 for xx in z_df.zstat]


#%%

independence_table.to_csv(r'table_5_1.csv')
z_df.to_csv(r'table_5_2.csv')



