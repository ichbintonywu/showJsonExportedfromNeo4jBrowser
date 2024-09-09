
import json
import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Display JSON File",
    page_icon="🚀",
    layout="wide",
)


st.title('DataFrame Display for the JSON file exported from Neo4j Browser')

st.markdown("**Please fill the below form :**")
with st.form(key="Choose a json file exported from Neo4j Browser", clear_on_submit = False):
    File = st.file_uploader(label = "Upload file", type=["json"])
    # Load JSON data

    if st.form_submit_button("Upload the JSON File"):
            save_folder = './'
            save_path = Path(save_folder, File.name)
            with open(save_path, mode='wb') as w:
                w.write(File.getvalue())
            with open(File.name, 'r',encoding='utf-8-sig') as file:
                data = json.load(file)
                df = pd.DataFrame(data)
                pd.set_option('display.max_colwidth', None) 
                print(df)
                st.dataframe(df,use_container_width=True) 

