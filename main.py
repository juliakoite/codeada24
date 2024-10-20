import streamlit as st
import pandas as pd
from io import StringIO
from parse import parse_file

from bill_summary import create_bill_summary, create_detailed_table
from ai_explain import get_medical_explanation




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

        # adding AI explanation for code
        if 'explain_index' not in st.session_state:
            st.session_state.explain_index = None
        
        # create interactive table with explanation buttons
        interactive_df = create_detailed_table(items_dict)
        
        # ai explanations
        for idx, row in interactive_df.iterrows():
            if row['Actions']:
                st.session_state.explain_index = idx
        
        if st.session_state.explain_index is not None:
            procedure = interactive_df.iloc[st.session_state.explain_index]['Service']
            with st.expander(f"Explanation for {procedure}"):
                explanation = get_medical_explanation(procedure)
                st.write(explanation)





    


