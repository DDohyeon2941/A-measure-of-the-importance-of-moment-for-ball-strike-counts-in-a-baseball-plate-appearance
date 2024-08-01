# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 13:44:38 2024

@author: dohyeon
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#%% 1. 기본 애피소드 만들기 [foul의 개수는 무관함]
atbat_df = pd.read_csv('dataset1/atbats.csv')
pitch_df = pd.read_csv('dataset1/pitches.csv')
pitch_df = pitch_df.dropna()


"""Masking codes and pitch types."""


def masking_code(uni_code):
    ball_codes = ['B', '*B', 'I', 'P']
    strike_codes = ['S', 'C', 'F', 'T', 'L', 'W', 'Q', 'R', 'M']
    if uni_code in ball_codes:
        return "B"
    elif uni_code in strike_codes:
        return "S"
    else:
        return uni_code


def mask_Pcode(uni_pcode):
    if uni_pcode in ['FF','FC','SI','FT','FS','FA']:
        return "D"
    elif uni_pcode in ['CU','CH','SL','KC','EP','KN','SC']:
        return "C"
    else:
        return "X"

pitch_df.loc[:, "mcode"] = [masking_code(uni_code) for uni_code in pitch_df.code]
pitch_df.loc[:, "pcode"] = [mask_Pcode(uni_type) for uni_type in pitch_df.pitch_type]

#%%

"""Transform multiple samples as single episode"""

code_li = []
mcode_li = []
ty_li = []
id_li = []
p_li = []
sspd_li = []
espd_li = []
b_count_li = []

for u_i, u_df in pitch_df.groupby('ab_id'):

    id_li.append(u_i)
    code_li.append(u_df['code'].tolist())
    mcode_li.append(u_df['mcode'].tolist())
    p_li.append(u_df['pcode'].tolist())
    sspd_li.append(u_df['start_speed'].tolist())
    espd_li.append(u_df['end_speed'].tolist())
    ty_li.append(u_df['type'].tolist())
    b_count_li.append(u_df['b_count'].tolist()[-1])

"""Make pitch episode dataframe"""

tt_df = pd.DataFrame(columns=[
    'ab_id','mcode','pcode','tcode','start_speed','end_speed','b_count'
    ]).astype(
        {'ab_id':int,'mcode':object, 'pcode':object, 'tcode':object,'start_speed':object, 'end_speed':object, 'b_count':int}
        )

tt_df.ab_id = id_li
tt_df.mcode = mcode_li
tt_df.pcode = p_li
tt_df.start_speed = sspd_li
tt_df.end_speed = espd_li
tt_df.tcode = ty_li
tt_df.b_count = b_count_li
""" Merge pitch episode data with atbat data"""
# 1차적으로 에피소드 데이터 상성

tt_df = pd.merge(left=tt_df, right = atbat_df[['ab_id','event']])


#%% 2. Filter episodes & Add more information

#1) Define Event

"Classify Out event and Reaching base event"

#Filtering Events, Field Error를 아웃에서 base로 바꿈
base_events = np.array(['Double', 'Single', 'Walk', 'Home Run', 'Triple',
                        'Hit By Pitch', 'Intent Walk', 'Field Error'])
out_events = np.array(['Groundout', 'Strikeout', 'Flyout', 'Pop Out', 'Forceout',
                       'Lineout', 'Grounded Into DP', 'Bunt Groundout','Double Play',
                       'Sac Fly', 'Fielders Choice Out', 'Bunt Pop Out', 'Strikeout - DP',
                       'Sac Fly DP', 'Bunt Lineout', 'Triple Play'])

uni_events = np.append(base_events, out_events)

#2) Filter Event
tt_df = tt_df.loc[tt_df.event.isin(uni_events)].reset_index(drop=True)


#%%

#3) Filter type of pitch X

X_type_idx = [xx for xx in range(tt_df.pcode.shape[0]) if 'X' in tt_df.pcode[xx]]


tt_df = tt_df.loc[np.setdiff1d(np.arange(tt_df.shape[0]),X_type_idx)].reset_index(drop=True).reset_index(drop=True)

#4) Filter ball count is 4

tt_df = tt_df.loc[tt_df['b_count'] != 4.0].reset_index(drop=True)


#%%

#5) Add the result of last pitch

e_list=[]
for bb in tt_df['event'].values:
   if bb in base_events: e_mask = 'H'
   elif bb in out_events: e_mask = 'X'
   else: break
   e_list.append(e_mask)

tt_df.loc[:,'E'] = e_list
tt_df.to_pickle(r'episode_list_0119.pkl')

#%% 2. 스트라이크가 2개 이상일때, 파울인 경우, 파울없애기

prep_df = pd.read_pickle(r'episode_list_0119.pkl')

def index_non_foul(whole_list):
    """리스트 형태, 스트라이크가 2개 이상일떄, 파일인 경우를 제외한 인덱스 추출"""
    temp_li = whole_list[:-1]

    s_count= 0
    bin_code = []

    if temp_li.count('S') <= 2:
        bin_code = np.arange(len(temp_li)).tolist()
    else:
        for uni_idx, uni_code in enumerate(temp_li):
            if uni_code == 'S':
                if  s_count < 2:
                    bin_code.append(uni_idx)
                    s_count+=1
            else:
                bin_code.append(uni_idx)
    return bin_code

index_non_foul(list('BBBSSSSS'))

#%% 추출한 인덱스를 활용해, 각 정보(mcode, pcode, start_speed) 인덱싱, 인덱스 값에 -1을 추가하였는데, 맨 마지막 요소[final state로 도달하기 위한 투구] 도 인덱싱 하기위함

prep_df.loc[:, 'f_index'] = [index_non_foul(xx) for xx in prep_df.mcode.values]
prep_df.loc[:, 'f_mode'] = [np.array(ydf.mcode)[ydf.f_index] for xx, ydf in prep_df.iterrows()]
prep_df.loc[:, 'f_pmode'] = [np.array(ydf.pcode)[ydf.f_index+[-1,]] for xx, ydf in prep_df.iterrows()]
prep_df.loc[:, 'f_sspd'] = [np.array(ydf.start_speed)[ydf.f_index+[-1,]] for xx, ydf in prep_df.iterrows()]


prep_df.to_pickle(r'episode_list_0119_f_index.pkl')

#%% 3. transition matrix와 speed dict 만들기

prep_df = pd.read_pickle(r'episode_list_0119_f_index.pkl')

process_list = [(0,0), (0,1), (1,0), (0,2), (1,1), (2,0), (1,2), (2,1), (3,0), (2,2), (3,1), (3,2),'H','X']
process_list = [str(xx) for xx in process_list]

trans_matrix = np.zeros((len(process_list),len(process_list)))
speed_dict = dict(zip(process_list, [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]))


result_df = pd.DataFrame(data=trans_matrix, index=process_list, columns=process_list)

#%%

"""각 state별 transition을 transition matrix에 추가함"""
"""각 state별 직구일때 시작구속 정보 추출"""


for _, (row_fmode, row_fpmode, row_sspd, row_end) in prep_df[['f_mode','f_pmode','f_sspd','E']].iterrows():
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
import user_utils as uu


uu.save_gpickle('state_speed_dist_0119.pickle', speed_dict)


result_df_ratio.to_csv(r'whole_state_ratio_0119.csv')









