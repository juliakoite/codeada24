import math
import streamlit as st
import pandas as pd
from io import StringIO
from parse import parse_file
from open_ai import ask_ai
from matplotlib import pyplot as plt

import numpy as np

from streamlit_extras.stylable_container import stylable_container


def get_summary(items_dict, amounts, duplicates_set):
    charges = items_dict.keys()
    st.write("## Summary of bill")
    with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: 10px;
                    background-color: #e591a3;
                    width: 950;
                }
                """,
        ):
        st.write("Here are your charges:")
        charge_list = []
        for charge in charges:
            charge_list.append(charge)
        st.write(str(charge_list))
        st.write("Here are your duplicate charges (recommend double checking these charges to make sure you haven't been overcharged)")
        st.write(str(duplicates_set))


def pie_chart(items_dict): 
   labels = list(items_dict.keys())
   total, dict = calculator(items_dict)
   amounts = list(dict.values())

   #ex = amounts.sort()

   fig1, ax1 = plt.subplots()
   percents = np.array(amounts)
   plt.show()

   

   ax1.pie(percents, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
   ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

   st.pyplot(fig1)
   return total


#dict/map charges -> amounts
def calculator(items_dict):
    values = list(items_dict.values())
    charges = list(items_dict.keys())
    amounts = []

    for value in values:
      amounts.append(value[0])


    #items = dict(zip(charges, amounts))
    total = sum(amounts)
    to_return = dict()

    if total > 0:
        for key, value in zip(charges, amounts):
            decimal = value / total
            percent = math.ceil(decimal * 100) / 100
            to_return[key] = percent
    else:
        # If total is zero, return zeros or handle as needed
        to_return = {key: 0 for key in charges}

    return total, to_return   

   
   

st.title("INSERT WEBSITE TITLE HERE")
st.write("### Upload your itemized medical bill")
uploaded_file = st.file_uploader("",['png', 'jpg'])
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
                return['background-color: #b6465f'] * len(row)
            else:
                return[''] * len(row)
            
        styled_df = df.style.apply(highlight_duplicates, axis=1)
        st.dataframe(styled_df, key="styled_df")

        total = pie_chart(items_dict)
        def create_checkbox_columns(df):
            checkboxes = []
            total_items = len(df)
            items_per_column = math.ceil(total_items / 2)

            col1, col2 = st.columns(2)

            for index, row in df.iterrows():
                if index < items_per_column:
                    with col1:
                        is_checked = st.checkbox(f"{row['Charges']}", key=f"checkbox_{index}")
                else:
                    with col2:
                        is_checked = st.checkbox(f"{row['Charges']}", key=f"checkbox_{index}")
                
                if is_checked:
                    checkboxes.append(df.loc[index]['Charges'])

            return checkboxes

        st.write("## Which charges would you like to be explained to you?")
        checkboxes = create_checkbox_columns(df)

        ai_response = ask_ai(checkboxes)
        with stylable_container(
            key="container_with_border",
            css_styles="""
                {
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 0.5rem;
                    padding: 10px;
                    background-color: #e591a3;
                    width: 950;
                }
                """,
            ):
            for charge in ai_response['charges']:
                st.write("Charge: " + charge['Procedure'])
                st.write("Description: " + charge['Description'])
                st.write("Validity: " + charge['Validity'])
        if st.button("Get summary of bill"):
            get_summary(items_dict, amounts, duplicates_set)








    




