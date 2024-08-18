import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

st.title('受験結果一覧')
st.text('こちらのページでは、今まで受験した試験を結果を見ることができます。')

code = st.text_input('社員番号を入力してください')
code_button = st.checkbox('社員番号確定')

if code_button:
    subjects_list = ['生命保険総論', '生命保険計理']
    subject_name = st.radio(
            label=f'科目を選んでください',
            options=subjects_list,
            horizontal=True
        )
    # 年度選択のプルダウンメニュー
    subjects_list = ['2023_A', '2023_B', '2023_C', 
                    '2022_A', '2022_B', '2022_C', 
                    '2021_A', '2021_B', '2021_C']
    subject = st.selectbox('年度を選んでください', subjects_list)
    
    if not os.path.exists(f'./answers/{code}/{subject_name}/{subject + "_correct_ratio"}.csv'):
        st.text('受験結果が存在しません')
    else:
        correct_ratio_df = pd.read_csv(f'./answers/{code}/{subject_name}/{subject + "_correct_ratio"}.csv', encoding='shift_jis')
        
    if os.path.exists(f'./answers/{code}/{subject_name}/{subject + "_your_answer"}.csv'):
        user_answers_df = pd.read_csv(f'./answers/{code}/{subject_name}/{subject + "_your_answer"}.csv', encoding='shift_jis')

    st.text('過去の解答')
    st.table(user_answers_df)
    st.text('正答率の推移')
    st.table(correct_ratio_df)

    plt.figure()
    plt.xticks(rotation=90)
    plt.scatter(correct_ratio_df['受験日'], correct_ratio_df['正答率'])
    plt.plot(correct_ratio_df['受験日'], correct_ratio_df['正答率'])
    st.pyplot(plt, use_container_width=True)