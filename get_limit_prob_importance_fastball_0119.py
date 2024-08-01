# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:50:13 2024

@author: dohyeon
"""


import user_utils as uu
import pandas as pd
import numpy as np

temp_df = pd.read_csv(r'whole_state_ratio_0119.csv', index_col=0)

bin_dict = dict(zip(temp_df.index.values[:-2],[0,0,0,0,0,0,0,0,0,0,0,0]))

bin_dict

bin_dict['(3, 2)'] = temp_df.loc['(3, 2)','X']

bin_dict['(3, 1)'] = temp_df.loc['(3, 1)','X'] + temp_df.loc['(3, 1)','(3, 2)'] * bin_dict['(3, 2)']
bin_dict['(2, 2)'] = temp_df.loc['(2, 2)','X'] + temp_df.loc['(2, 2)','(3, 2)'] * bin_dict['(3, 2)']

bin_dict['(3, 0)'] = temp_df.loc['(3, 0)','X'] + temp_df.loc['(3, 0)','(3, 1)'] * bin_dict['(3, 1)']
bin_dict['(1, 2)'] = temp_df.loc['(1, 2)','X'] + temp_df.loc['(1, 2)','(2, 2)'] * bin_dict['(2, 2)']

bin_dict['(2, 1)'] = temp_df.loc['(2, 1)','X'] + temp_df.loc['(2, 1)','(2, 2)'] * bin_dict['(2, 2)'] + temp_df.loc['(2, 1)','(3, 1)'] * bin_dict['(3, 1)']

bin_dict['(2, 0)'] = temp_df.loc['(2, 0)','X'] + temp_df.loc['(2, 0)','(2, 1)'] * bin_dict['(2, 1)']+ temp_df.loc['(2, 0)','(3, 0)'] * bin_dict['(3, 0)']

##
bin_dict['(1, 1)'] = temp_df.loc['(1, 1)', 'X'] + (temp_df.loc['(1, 1)','(2, 1)'] * bin_dict['(2, 1)'])+ (temp_df.loc['(1, 1)', '(1, 2)'] * bin_dict['(1, 2)'])


bin_dict['(0, 2)'] = temp_df.loc['(0, 2)','X'] + temp_df.loc['(0, 2)','(1, 2)'] * bin_dict['(1, 2)']


bin_dict['(1, 0)'] = temp_df.loc['(1, 0)','X'] + temp_df.loc['(1, 0)','(1, 1)'] * bin_dict['(1, 1)'] + temp_df.loc['(1, 0)','(2, 0)'] * bin_dict['(2, 0)']


bin_dict['(0, 1)'] = temp_df.loc['(0, 1)','X'] + temp_df.loc['(0, 1)','(1, 1)'] * bin_dict['(1, 1)'] + temp_df.loc['(0, 1)','(0, 2)'] * bin_dict['(0, 2)']

bin_dict['(0, 0)'] = temp_df.loc['(0, 0)','X'] + temp_df.loc['(0, 0)','(0, 1)'] * bin_dict['(0, 1)'] + temp_df.loc['(0, 0)','(1, 0)'] * bin_dict['(1, 0)']

limiting_prob_df = pd.DataFrame(index=bin_dict.keys(), data=bin_dict.values(), columns=['val'])
limiting_prob_df.to_csv(r'whole_limiting_prob.csv')

#%%

imp_dict = dict(zip(temp_df.index.values[:-2],[0,0,0,0,0,0,0,0,0,0,0,1]))



imp_dict['(3, 1)'] = 1*(temp_df.loc['(3, 1)', 'X']+temp_df.loc['(3, 1)', 'H']) + bin_dict['(3, 2)']*temp_df.loc['(3, 1)', '(3, 2)']


imp_dict['(2, 2)'] = 1*(temp_df.loc['(2, 2)', 'X'] + temp_df.loc['(2, 2)', 'H']) + bin_dict['(3, 2)']*temp_df.loc['(2, 2)', '(3, 2)']


imp_dict['(3, 0)'] = 1*(temp_df.loc['(3, 0)', 'X'] + temp_df.loc['(3, 0)', 'H']) + bin_dict['(3, 1)']*temp_df.loc['(3, 0)', '(3, 1)']


imp_dict['(1, 2)'] = 1*(temp_df.loc['(1, 2)', 'X'] + temp_df.loc['(1, 2)', 'H']) + bin_dict['(2, 2)']*temp_df.loc['(1, 2)', '(2, 2)']

imp_dict['(2, 1)'] = 1*(temp_df.loc['(2, 1)', 'X'] + temp_df.loc['(2, 1)', 'H']) + np.abs((bin_dict['(2, 2)'] - bin_dict['(3, 1)'])) * (1-(temp_df.loc['(2, 1)', 'X'] + temp_df.loc['(2, 1)', 'H']))

##

imp_dict['(2, 0)'] = 1*(temp_df.loc['(2, 0)', 'X'] + temp_df.loc['(2, 0)', 'H']) + np.abs((bin_dict['(2, 1)'] - bin_dict['(3, 0)'])) * (1-(temp_df.loc['(2, 0)', 'X'] + temp_df.loc['(2, 0)', 'H']))


imp_dict['(1, 1)'] = 1*(temp_df.loc['(1, 1)', 'X'] + temp_df.loc['(1, 1)', 'H']) + np.abs((bin_dict['(2, 1)'] - bin_dict['(1, 2)'])) * (1-(temp_df.loc['(1, 1)', 'X'] + temp_df.loc['(1, 1)', 'H']))

imp_dict['(0, 2)'] = 1*(temp_df.loc['(0, 2)', 'X']+temp_df.loc['(0, 2)', 'H']) + bin_dict['(1, 2)']*temp_df.loc['(0, 2)', '(1, 2)']

imp_dict['(1, 0)'] = 1*(temp_df.loc['(1, 0)', 'X'] + temp_df.loc['(1, 0)', 'H']) + (bin_dict['(1, 1)'] - bin_dict['(2, 0)']) * (1-(temp_df.loc['(1, 0)', 'X'] + temp_df.loc['(1, 0)', 'H']))

imp_dict['(0, 1)'] = 1*(temp_df.loc['(0, 1)', 'X'] + temp_df.loc['(0, 1)', 'H']) + np.abs((bin_dict['(1, 1)'] - bin_dict['(0, 2)'])) * (1-(temp_df.loc['(0, 1)', 'X'] + temp_df.loc['(0, 1)', 'H']))


imp_dict['(0, 0)'] = 1*(temp_df.loc['(0, 0)', 'X'] + temp_df.loc['(0, 0)', 'H']) + np.abs((bin_dict['(1, 0)'] - bin_dict['(0, 1)'])) * (1-(temp_df.loc['(0, 0)', 'X'] + temp_df.loc['(0, 0)', 'H']))

#%%

temp_obj1 = uu.load_gpickle(r'state_speed_dist_0119.pickle')

avg_speed_dic = dict(zip(temp_df.index.values[:-2],[0,0,0,0,0,0,0,0,0,0,0,0]))

num_li = []
for xx in list(temp_obj1.keys())[:-2]:
    avg_speed_dic[xx] = np.mean(temp_obj1[xx])
    num_li.append(len(temp_obj1[xx]))

imp_dict
avg_speed_dic

#%%

total_score_df = pd.DataFrame(data={'imp':list(imp_dict.values()), 'avg_sp':list(avg_speed_dic.values())}, index=imp_dict.keys())



df1 = pd.concat([total_score_df.imp.rank(ascending=False),total_score_df.avg_sp.rank(ascending=False)],axis=1)
df1.columns=['imp_rank','avg_sp_rank']

df2= pd.concat([total_score_df,df1],axis=1)
df2.sort_values(by='imp_rank',ascending=True)


df2.to_csv(r'whole_dataset_empirical_validity_0119.csv')


