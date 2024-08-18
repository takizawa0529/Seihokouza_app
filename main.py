import streamlit as st

st.title('生保講座')
st.text('このページは、生保講座過去問の解説を記載するページです')

subjects_list = ['生命保険総論', '生命保険計理', '受験結果一覧']
subject = st.selectbox('科目を選んでください', subjects_list)
subject_button = st.button('選択')

subject_pages = {
    '生命保険総論': 'Souron.py',
    '生命保険計理': 'Keiri.py',
}

if subject_button:
    st.text(f'{subject}の勉強頑張りましょう')
    st.switch_page(f'./pages/{subject_pages[subject]}')