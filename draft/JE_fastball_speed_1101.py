import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

atbat_df = pd.read_csv('dataset/atbats.csv')
pitch_df = pd.read_csv('dataset/pitches.csv')
pitch_df = pitch_df.dropna()

pitch_df['pitch_type'].value_counts()

# masking
def mask_Pcode(uni_pcode):
    if uni_pcode in ['FF','FC','SI','FT','FS','FA']: # 직구
        return "fastball"
    elif uni_pcode in ['CU','CH','SL','KC','EP','KN','SC']: # 변화구
        return "breakingball"
    else:
        return "X" # 고의사구 등

mask_pcode = [mask_Pcode(aa) for aa in pitch_df.pitch_type]
pitch_df.loc[:, "pcode"] = mask_pcode

# speed
## 야구 구속은 초속으로 측정함
## 데이터 제외없이 모든 event를 고려함
count = pitch_df.groupby(['b_count', 's_count','pcode',])['start_speed'].mean()
count = count.reset_index(inplace=False)
count.columns=['b_count','s_count','pcode','start_speed']

# 각 state에서의 구속 평균
mean_fastball_speed = (count.iloc[np.where(count['pcode']=='fastball')[0]]).iloc[:-2]
mean_fastball_speed = mean_fastball_speed.reset_index(drop=True)
mean_fastball_speed

# 각 state의 구속 평균 - 모든 state의 구속 평균 후 정렬
rank = mean_fastball_speed.sort_values(by=['start_speed']) 
rank['start_speed']= rank['start_speed'] - mean_fastball_speed['start_speed'].mean()
rank