# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 19:51:31 2024

@author: dohyeon
"""


import pandas as pd
import numpy as np

temp_df = pd.read_csv(r'table_8.csv', index_col=0)



temp_df.loc[['(0, 0)','(1, 0)','(2, 0)','(3, 0)']][['avg_sp', 'elite_avg_sp']].mean()


temp_df.loc[['(0, 1)','(1, 1)','(2, 1)','(3, 1)']][['avg_sp', 'elite_avg_sp']].mean()


temp_df.loc[['(0, 2)','(1, 2)','(2, 2)','(3, 2)']][['avg_sp', 'elite_avg_sp']].mean()
