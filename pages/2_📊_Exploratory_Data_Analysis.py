import streamlit as st
from streamlit_pandas_profiling import st_profile_report
import shap
import pandas as pd
import time

# import os
st.set_page_config(layout='wide', page_title="EDA", page_icon="😎")
st.title('📊 Exploratory Data Analysis')

#################################################
#Sidebar
st.sidebar.image('logo.png') 
st.markdown("""
<style>
    div[data-testid="stSidebarUserContent"] img {
        background: #ffffff;
        border-radius: 20px;
        border: thick;
        border-style: inset;
        border-color: black;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.header("About")

st.sidebar.markdown(
    """
This app using Pandas profiling component for [Streamlit](https://streamlit.io/).


""")

st.sidebar.markdown(
    "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
)
st.sidebar.divider()

st.sidebar.header("Resources")
st.sidebar.markdown(
    """
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
- [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
- [Blog](https://blog.streamlit.io/how-to-master-streamlit-for-data-science/) (How to master Streamlit for data science)
"""
)


#################################################
def load_data():
    X, y = shap.datasets.adult()
    df = pd.DataFrame(X)
    return df

def uploader():
    if st.session_state.file_upload == False:
        st.session_state.file_example_upload = True
        
def file_remove():
    if st.session_state.file_upload:
        st.session_state.file_upload = False
    # else:
    #     st.session_state.file_example_upload = True
        
    
if not 'file_example_upload' in st.session_state:
    st.session_state.file_example_upload = False
if not 'file_upload' in st.session_state:
    st.session_state.file_upload = False
if not 'button_dis' in st.session_state:
    st.session_state.button_dis = False

    
# File uploader widget disabled if example data is loade
uploaded_file = st.file_uploader("Choose a CSV file", type='csv',on_change = file_remove)
st.button('Example Data',on_click=uploader,disabled=st.session_state.file_upload)

if uploaded_file is not None:
    st.session_state.file_upload = True
    st.session_state.file_upload = True
    st.session_state.file_example_upload = False
    df = pd.read_csv(uploaded_file)
    st.info('Uploaded File')
    pr = df.profile_report()
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    time.sleep(1)
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    time.sleep(1)
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    time.sleep(1)
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    time.sleep(1)
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    st_profile_report(pr)
    
elif st.session_state.file_example_upload == False:
    st.session_state.file_upload = False
    st.info('☝️ Upload a CSV file or use Example Data')
else:
    st.session_state.file_example_upload = True
    df = load_data()
    st.info('Loaded Example Data')
    pr = df.profile_report()
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    time.sleep(1)
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    time.sleep(1)
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    time.sleep(1)
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    time.sleep(1)
    st.toast('🚨 Analysing Data, Please Wait !! 🚨')
    st_profile_report(pr)

    


    

