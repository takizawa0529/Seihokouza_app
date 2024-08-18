import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
from PIL import Image
import os

# ワイドモードに設定
st.set_page_config(layout="wide")

# タイトルと説明
subject_name = '生命保険総論'
st.title(subject_name)
st.text('このページは、生保講座過去問の解説を記載するページです')

# ディレクトリの作成（必要なら）
if not os.path.exists(f'./answers/{subject_name}'):
    os.makedirs(f'./answers/{subject_name}')

# 年度選択のプルダウンメニュー
subjects_list = ['2023_A', '2023_B', '2023_C']
subject = st.selectbox('年度を選んでください', subjects_list)

# CSVファイルの読み込み
exam_files = {
    '2023_A': '2023_A.csv',
    '2023_B': '2023_B.csv',
    '2023_C': '2023_C.csv',
    # 他の年度のデータもここに追加できます
}

file_path = f'./Problems/{subject_name}/' + exam_files[subject]
df = pd.read_csv(file_path, encoding='shift-jis')

st.markdown('**生保標準生命表2018(死亡保険用)(女)**')
image = Image.open(f'./picture/{subject_name}/{subject}/生命表.png')
st.image(image)#, width=200)

st.markdown('**生保標準生命表2018(死亡保険用)(女)**')
image = Image.open(f'./picture/{subject_name}/{subject}/複利現価表.png')
st.image(image)#, width=200)

# 問題の表示とユーザーの回答入力
num_questions = min(len(df), 50)
today = dt.datetime.now()
user_answers = []

for i in range(num_questions):
    # 問題を表示
    st.markdown(f"**問{i+1}**")
    st.text(df.loc[i, '問題'])

    # CSVファイルの「語群」列から選択肢を取得
    options = df.loc[i, '語群'].split('、')  # 語群をリストに変換（CSVで「、」区切りの場合）
    # ユーザーの回答を選択式で入力

    user_answer = st.radio(label=f'あなたの回答を選んでください - 問{i+1}',
                      options=options,
                      horizontal=True
                      )
    
    user_answers.append(user_answer)

    

# 答え合わせボタンをページの一番下に配置
result_button = st.button('答え合わせ')

# 「答え合わせ」ボタンの処理
if result_button:
    for i in range(num_questions):
        st.markdown(f"**問{i+1}**")
        st.markdown(f"**解答: {df.loc[i, '解答']}**")

        # 解説を横長に表示
        with st.expander(f"解説: 問{i+1}", expanded=False):
            st.markdown(f'<div style="width:100%;">{df.loc[i, "解説"]}</div>', unsafe_allow_html=True)
    
    # ユーザーの回答を保存
    user_answers_df = pd.DataFrame(user_answers, columns=[str(today)[:19]])
    saiten = pd.concat([user_answers_df, df['解答']], axis=1)
    saiten = saiten.rename(columns={str(today)[:19]:'あなたの解答'})
    saiten['正誤ラベル'] = np.where(saiten['解答']==saiten['あなたの解答'], 1, 0)
    saiten['正誤'] = np.where(saiten['解答']==saiten['あなたの解答'], 'o', 'x')

    correct_ratio = saiten[saiten['正誤']=='o']['正誤'].count()/saiten['正誤'].count() * 100
    st.text(f'正答率 {correct_ratio} %')
    st.table(saiten[['解答', 'あなたの解答', '正誤']])

    if not os.path.exists(f'./answers/{subject_name}/{exam_files[subject] + "_your_answer"}.csv'):
        st.write('回答が保存されました！')
        user_answers_df.to_csv(f'./answers/{subject_name}/{exam_files[subject] + "_your_answer"}.csv', encoding='shift-jis', index=False)
    else:
        answers_df = pd.read_csv(f'./answers/{subject_name}/{exam_files[subject] + "_your_answer"}.csv', encoding='shift_jis')
        user_answers_df = pd.concat([answers_df, user_answers_df], axis=1)
        st.write('回答が保存されました！')
        user_answers_df.to_csv(f'./answers/{subject_name}/{exam_files[subject] + "_your_answer"}.csv', encoding='shift-jis', index=False)

    st.table(user_answers_df)