import streamlit as st
import pandas as pd
from io import StringIO
from parse import parse_file

st.write("Our program")
uploaded_file = st.file_uploader("Upload your medical bill", ['png', 'jpg'])
if uploaded_file is not None:
     print("Filename:" + uploaded_file.name)
     print("Type" + uploaded_file.type)

     with open(f"uploads/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())

        parse_file(uploaded_file.name)


    


