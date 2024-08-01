# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 17:49:33 2024

@author: dohyeon
"""


import pandas as pd
import numpy as np

actual_df = pd.read_csv('actual_out_prob.csv', index_col=0)
model_df = pd.read_csv('whole_limiting_prob.csv', index_col=0)


actual_df
model_df


actual_df['model'] = model_df.val


#%%


def get_z_stats(p1, n1, p2, n2):
    return  (p1 - p2) / ((p1*(1-p1)/n1 + p2*(1-p2)/n2)**0.5)



#%%


actual_df['z_stats'] = [get_z_stats(uni_model, uni_num, uni_act, uni_num) for _, (uni_num, uni_act, uni_model) in actual_df[['total', 'actual', 'model']].iterrows()]

actual_df['diff'] = actual_df.model - actual_df.actual


actual_df[['model','actual','total','diff','z_stats']].round(4)

actual_df.to_csv(r'table_6.csv')
