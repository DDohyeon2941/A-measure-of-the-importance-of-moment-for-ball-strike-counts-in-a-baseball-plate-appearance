# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:14:23 2023

@author: dohyeon
"""


import numpy as np
import pandas as pd
import user_utils as uu


atbat_df = pd.read_csv('dataset1/atbats.csv')
pitch_df = pd.read_csv('dataset1/pitches.csv')
temp_obj = pd.read_pickle(r'episode_list_1028_f_index.pkl')