import streamlit as st
import pandas as pd
from io import StringIO
from parse import parse_file




st.title("INSERT WEBSITE TITLE HERE")
uploaded_file = st.file_uploader("Upload your medical bill", ['png', 'jpg'])
if uploaded_file is not None:
     print("Filename:" + uploaded_file.name)
     print("Type" + uploaded_file.type)

     with open(f"uploads/{uploaded_file.name}", "wb") as f:
        f.write(uploaded_file.getbuffer())

        items_dict = parse_file(uploaded_file.name)
        amounts = []
        duplicates_set = []
        for key, value in items_dict.items():
            amounts.append(value[0])
            if value[1] > 1:
                duplicates_set.append(key)
        duplicates_set = set(duplicates_set)
        print(duplicates_set)
        df = pd.DataFrame({
            "Charges": items_dict.keys(),
            "Amount($)" :amounts
        })

        def highlight_duplicates(row):
            if row['Charges'] in duplicates_set:
                return['background-color: red'] * len(row)
            else:
                return[''] * len(row)
            
        styled_df = df.style.apply(highlight_duplicates, axis=1)

        if "styled_df" not in st.session_state:
            st.session_state["styled_df"] = styled_df
        
        def callback():
            st.write(st.session_state["styled_df"])
            print(st.session_state["styled_df"])

        styled_df = st.session_state["styled_df"]
        st.dataframe(styled_df, selection_mode='multi-row', on_select=callback, key="styled_df")





    


