import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt
import re
from sympy import sympify, preview

# ワイドモードに設定
#st.set_page_config(layout="wide")

# タイトルと説明
subject_name = '生命保険計理'
st.title(subject_name)
st.text('このページは、生保講座過去問の解説を記載するページです')

code = st.text_input('社員番号を入力してください')
code_button = st.button('社員番号確定')

if code_button:
    # ディレクトリの作成（必要なら）
    if not os.path.exists(f'./answers/{code}'):
        os.makedirs(f'./answers/{code}')
    if not os.path.exists(f'./answers/{code}/{subject_name}'):
        os.makedirs(f'./answers/{code}/{subject_name}')

# 年度選択のプルダウンメニュー
subjects_list = ['2023_A', '2023_B', '2023_C', 
                 '2022_A', '2022_B', '2022_C', 
                 '2021_A', '2021_B', '2021_C']
subject = st.selectbox('年度を選んでください', subjects_list)

# CSVファイルの読み込み
exam_files = {
    '2023_A': '2023_A.csv',
    '2023_B': '2023_B.csv',
    '2023_C': '2023_C.csv',
    '2022_A': '2022_A.csv',
    '2022_B': '2022_B.csv',
    '2022_C': '2022_C.csv',
    '2021_A': '2021_A.csv',
    '2021_B': '2021_B.csv',
    '2021_C': '2021_C.csv',
    # 他の年度のデータもここに追加できます
}

file_path = f'./Problems/{subject_name}/' + exam_files[subject]
df = pd.read_csv(file_path, encoding='shift-jis')

image_path = f"./Problems/{subject_name}/{subject}/page_{2}.png"
if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image)

# 問題範囲を各ページに割り当てる
page_to_questions = {
    3: range(1, 6),
    4: range(6, 11),
    5: range(11, 16),
    6: range(16, 21),
    7: range(21, 23),
    8: range(23, 25),
    9: range(25, 27),
    10: range(27, 29),
    11: range(29, 31),
    12: range(31, 35),
    13: range(35, 39),
    14: range(39, 42),
    15: range(42, 44),
    16: range(44, 46),
    17: range(46, 48),
    18: range(48, 50),
    19: range(50, 51),
}

today = now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
user_answers = []

for page, questions in page_to_questions.items():
    # 画像を表示
    image_path = f"./Problems/{subject_name}/{subject}/page_{page}.png"

    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image)
    else:
        st.text(f"画像が見つかりませんでした: page_{page}.png")

    # 各ページに対応する問題を表示
    for i in questions:
        # 問題を表示
        st.text('-'*100)
        st.markdown(f"**問{i}**")
        
        # 選択肢を表示
        options = df.loc[i-1, '語群'].split('、')  # 語群をリストに変換
        user_answer = st.radio(
            label=f'あなたの回答を選んでください - 問{i}',
            options=options,
            horizontal=True
        )
        user_answers.append(user_answer)

# 答え合わせボタンをページの一番下に配置
result_button = st.button('答え合わせ')

def preprocess_tex(tex):
    # '^' を '**' に変換
    tex = tex.replace('^', '**')
    
    # 数字と変数の間に掛け算を挿入
    tex = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', tex)
    
    return tex

def render_markdown_with_tex(text):
    """
    テキスト内のTeX形式の数式を処理し、SymPyで表示可能な形にする。
    """
    segments = re.split(r'(\$[^\$]+\$)', text)  # '$'で囲まれた部分を分割
    for segment in segments:
        if segment.startswith('$') and segment.endswith('$'):
            # TeX部分を処理する
            tex = segment.strip('$')
            try:
                # 前処理を行う
                tex = preprocess_tex(tex)
                expr = sympify(tex)
                st.latex(sp.latex(expr))  # 数式をTeX形式で表示
            except Exception as e:
                st.write(segment)  # 解析に失敗した場合はそのまま表示
        else:
            # 通常のテキスト部分を表示する
            st.write(segment)


# 「答え合わせ」ボタンの処理
if result_button:
    for i in range(len(user_answers)):
        st.markdown(f"**問{i+1}**")
        st.markdown(f"**解答: {df.loc[i, '解答']}**")

        # 解説を横長に表示
        with st.expander(f"解説: 問{i+1}", expanded=False):
            render_markdown_with_tex(df.loc[i, "解説"])  # 解説をレンダリングする
    
    # ユーザーの回答を保存（この部分は元のコードのまま）
    user_answers_df = pd.DataFrame(user_answers, columns=[str(today)[:19]])
    saiten = pd.concat([user_answers_df, df[['解答', '点数']]], axis=1)
    saiten = saiten.rename(columns={str(today)[:19]:'あなたの解答'})
    saiten['正誤ラベル'] = np.where(saiten['解答']==saiten['あなたの解答'], 1, 0)
    saiten['正誤'] = np.where(saiten['解答']==saiten['あなたの解答'], 'o', 'x')

    score = saiten[saiten['正誤']=='o']['点数'].sum()
    st.text(f'得点 {score} 点')
    st.table(saiten[['解答', 'あなたの解答', '正誤']])

    score_df = pd.DataFrame([[str(today)[:19], int(score)]], columns=['受験日', '正答率'])

    if not os.path.exists(f'./answers/{code}/{subject_name}/{subject + "_score"}.csv'):
        score_df.to_csv(f'./answers/{code}/{subject_name}/{subject + "_score"}.csv', encoding='shift-jis', index=False)
    else:
        ratio_df = pd.read_csv(f'./answers/{code}/{subject_name}/{subject + "_score"}.csv', encoding='shift_jis')
        score_df = pd.concat([ratio_df, score_df], axis=0, ignore_index=True)
        score_df.to_csv(f'./answers/{code}/{subject_name}/{subject + "_score"}.csv', encoding='shift-jis', index=False)

    if not os.path.exists(f'./answers/{code}/{subject_name}/{subject + "_your_answer"}.csv'):
        st.write('回答が保存されました！')
        user_answers_df.to_csv(f'./answers/{code}/{subject_name}/{subject + "_your_answer"}.csv', encoding='shift-jis', index=False)
    else:
        answers_df = pd.read_csv(f'./answers/{code}/{subject_name}/{subject + "_your_answer"}.csv', encoding='shift_jis')
        user_answers_df = pd.concat([answers_df, user_answers_df], axis=1)
        st.write('回答が保存されました！')
        user_answers_df.to_csv(f'./answers/{code}/{subject_name}/{subject + "_your_answer"}.csv', encoding='shift-jis', index=False)

    st.text('過去の解答')
    st.table(user_answers_df)
    st.text('正答率の推移')
    st.table(score_df)

    plt.figure()
    plt.xticks(rotation=90)
    plt.scatter(score_df['受験日'], score_df['正答率'])
    plt.plot(score_df['受験日'], score_df['正答率'])
    st.pyplot(plt, use_container_width=True)