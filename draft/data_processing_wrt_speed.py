# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 14:24:39 2021

@author: dohyeon
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#%% 1. 기본 애피소드 만들기[foul의 개수는 무관함]
atbat_df = pd.read_csv('dataset1/atbats.csv')
pitch_df = pd.read_csv('dataset1/pitches.csv')
pitch_df = pitch_df.dropna()


"""Masking codes and pitch types."""


def masking_code(uni_code):
    ball_codes = ['B', '*B', 'I', 'P']
    strike_codes = ['S', 'C', 'F', 'T', 'L', 'W', 'Q', 'R', 'M']
    runs_codes = ['E','H']
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


mask_code = [masking_code(aa) for aa in pitch_df.code]
mask_pcode = [mask_Pcode(aa) for aa in pitch_df.pitch_type]

pitch_df.loc[:, "mcode"] = mask_code
pitch_df.loc[:, "pcode"] = mask_pcode

#t_pitch_df = pitch_df.iloc[:100].copy(deep=True)


#%%
"""Merge multiple samples as single episode"""



code_li = []
mcode_li = []
ty_li = []
id_li = []
p_li = []
sspd_li = []
espd_li = []


for u_i, u_df in pitch_df.groupby('ab_id'):


    if not u_df.shape[0] > 1:
        id_li.append(u_i)
        code_li.append(u_df['code'].tolist())
        mcode_li.append(u_df['mcode'].tolist())
        p_li.append(u_df['pcode'].tolist())
        sspd_li.append(u_df['start_speed'].tolist())
        espd_li.append(u_df['end_speed'].tolist())
        ty_li.append(u_df['type'].tolist())


    else:
        id_li.append(u_i)
        code_li.append(u_df['code'].tolist())
        mcode_li.append(u_df['mcode'].tolist())
        p_li.append(u_df['pcode'].tolist())
        sspd_li.append(u_df['start_speed'].tolist())
        espd_li.append(u_df['end_speed'].tolist())
        ty_li.append(u_df['type'].tolist())


#%%

#t_pitch_df['sspd'] = t_pitch_df['sspd'].astype(object)
#t_pitch_df.loc[:,'sspd'] = p_li[:100]

#%%

tt_df = pd.DataFrame(columns=['ab_id','mcode','pcode','tcode','start_speed','end_speed']).astype({'ab_id':int,'mcode':object, 'pcode':object, 'tcode':object,'start_speed':object, 'end_speed':object})
tt_df.ab_id = id_li
tt_df.mcode = mcode_li
tt_df.pcode = p_li
tt_df.start_speed = sspd_li
tt_df.end_speed = espd_li
tt_df.tcode = ty_li

tt_df = pd.merge(left=tt_df, right = atbat_df[['ab_id','event']])


#%% Filtering Events

base_events = np.array(['Double', 'Single', 'Walk', 'Home Run', 'Triple', 'Hit By Pitch', 'Intent Walk'])
out_events = np.array(['Groundout', 'Strikeout', 'Flyout', 'Pop Out', 'Forceout',
                       'Lineout', 'Grounded Into DP', 'Bunt Groundout', 'Field Error','Double Play', 
                       'Sac Fly', 'Fielders Choice Out', 'Bunt Pop Out', 'Strikeout - DP',
                       'Sac Fly DP', 'Bunt Lineout', 'Triple Play'])

uni_events = np.append(base_events, out_events)

uni_enames = uni_events

#%%

ab_pitch_num = pitch_df[['ab_id','pitch_num']].groupby('ab_id').max().reset_index().astype({'ab_id':int})
bat_pitch_id = atbat_df[['g_id','ab_id','inning','pitcher_id','batter_id','event']].astype({'ab_id':int})
bat_pitch_id = bat_pitch_id.loc[bat_pitch_id.event.isin(uni_enames)]
temp_final = pd.merge(right=ab_pitch_num, left=bat_pitch_id)
#%%

prep_df=pd.merge(left=tt_df, right=temp_final)
aaa= [xx for xx in range(prep_df.pcode.shape[0]) if 'X' in prep_df.pcode[xx]]
prep_df = prep_df.loc[np.setdiff1d(np.arange(prep_df.shape[0]),aaa)].reset_index(drop=True)




tarr = temp_final[['ab_id','pitch_num']].values.astype(int)
varr = pitch_df[['ab_id','pitch_num']].values.astype(int)

tli = [str(tuple([a1,a2])) for a1, a2 in tarr]
vli = [str(tuple([a1,a2])) for a1, a2 in varr]

xy, vidx, tidx = np.intersect1d(vli, tli, return_indices=True)

prep_df = pd.merge(left=prep_df, right=pitch_df.iloc[vidx][['ab_id','b_count','s_count']].reset_index(drop=True))
prep_df = prep_df.loc[prep_df['b_count'] != 4.0].reset_index(drop=True)

#%%


p_list=[]
e_list=[]
for aa,bb in prep_df[['pcode','event']].values:
   if bb in base_events: e_mask = 'H'
   elif bb in out_events: e_mask = 'X'
   else: break
   if len(aa) > 1: p_list.append(aa[-1])
   else: p_list.append(aa)   
   e_list.append(e_mask)

prep_df.loc[:,'E'] = e_list
#prep_df.to_pickle(r'episode_list_1028.pkl')

#%% 2. 스트라이크가 2개 이상일때, 파울인 경우, 파울없애기

#prep_df = pd.read_pickle(r'episode_list_1028.pkl')

def prep_foul(whole_str):
    """string 형태"""
    temp_str = whole_str[:-1]

    s_count= 0
    bin_code = ''

    if temp_str.count('S') <= 2:
        bin_code = temp_str
    else:
        for uni_code in temp_str:
            if uni_code == 'S':
                if  s_count < 2:
                    bin_code += uni_code
                    s_count+=1
            else:
                bin_code += uni_code
    return bin_code

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

a2 = list('BBBSSSSSD')

prep_foul('BBBSSSSSD')

index_non_foul(a2)

#%% 3. 추출한 인덱스를 활용해, 각 정보(mcode, pcode, start_speed) 인덱싱, 인덱스 값에 -1을 추가하였는데, 맨 마지막 요소[final state로 도달하기 위한 투구] 도 인덱싱 하기위함

prep_df.loc[:, 'f_index'] = [index_non_foul(xx) for xx in prep_df.mcode.values]
prep_df.loc[:, 'f_mode'] = [np.array(ydf.mcode)[ydf.f_index] for xx, ydf in prep_df.iterrows()]
prep_df.loc[:, 'f_pmode'] = [np.array(ydf.pcode)[ydf.f_index+[-1,]] for xx, ydf in prep_df.iterrows()]
prep_df.loc[:, 'f_sspd'] = [np.array(ydf.start_speed)[ydf.f_index+[-1,]] for xx, ydf in prep_df.iterrows()]

#prep_df.loc[:, 'D_index'] = [index_D(xx) for xx in prep_df.pcode.values]


#prep_df.to_pickle(r'episode_list_1028_f_index.pkl')

#%%


process_list = [(0,0), (0,1), (1,0), (0,2), (1,1), (2,0), (1,2), (2,1), (3,0), (2,2), (3,1), (3,2),'H','X']
process_list = [str(xx) for xx in process_list]

trans_matrix = np.zeros((len(process_list),len(process_list)))
speed_dict = dict(zip(process_list, [[],[],[],[],[],[],[],[],[],[],[],[],[],[]]))


result_df = pd.DataFrame(data=trans_matrix, index=process_list, columns=process_list)

#%% 4. 각 state별 직구일때 시작구속 정보 추출


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

#%% 5. 추출한 정보를 토대로 state별 observation, 구속 분포내 사분범위 수 추출
bbin_dict = {}

for uni_key, uni_val in speed_dict.items():
    uni_cnt = len(uni_val)
    uni_avg = np.mean(uni_val)
    uni_med = np.median(uni_val)
    uni_qnt = np.quantile(uni_val, [0.25, 0.50, 0.75])

    bbin_dict[uni_key] = [uni_cnt, uni_qnt]
#%%

bbin_dict

result_df

import user_utils as uu
uu.save_gpickle('state_cnt_qnt.pickle',bbin_dict)




#%%
result_df.to_csv(r'count_1028.csv')











