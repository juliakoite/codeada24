import streamlit as st
import pandas as pd
import plotly.express as px

def create_bill_summary(items_dict):
    # mapping possible categories
    # im just using common keywords which prob wont work 
    # if we wanted to actually do general, it would take a lot more code which I can do 
    categories = {
        'ROOM AND CARE': ['Room and Care'],
        'GENERAL LABORATORY': ['ARTERIAL PUNCTURE', 'VENIPUNCTURE'],
        'LAB-CHEMISTRY': ['COMP METABOLIC PANEL', 'BASIC METABOLIC PANEL'],
        'LAB-HEMATOLOGY': ['CBC AUTO DIFF'],
        'RAD DIAGNOSTIC': ['XR CHEST SGL VIEW'],
        'RESPIRATORY': ['INHALATION TX', 'HAND HELD NEB SUBSQ', 'CHEST PHYSIO SUBSQ']
    }

    #init summary data
    category_totals = {cat: 0 for cat in categories.keys()}

    # calculate totals for each category
    for item, (amount, count) in items_dict.items():
        amount = float(str(amount).replace('$', '').replace(',', ''))
        for category, items in categories.items():
            if any(service.upper() in item.upper() for service in items):
                category_totals[category] += amount
                break

    # summary section :3
    st.header("Bill Summary")
    total_bill = sum(category_totals.values())
    st.metric("Total Bill Amount", f"${total_bill:,.2f}")

    # pie chart then plot
    fig = px.pie (
        values=list(category_totals.values()),
        names=list(category_totals.keys()),
        title='Charges by Category'
    )
    st.plotly_chart(fig)

    # then gonna try category breakdown 
    st.subheader("Category Breakdown")
    for category, total in category_totals.items():
        st.write(f"{category}: ${total:,.2f}")
    
    return category_totals


# now want to create like a table to show data?
def create_table(items_dict): 
    st.header("Itemized Chargest")

    #im gonna use a pandas dataframe for this.
    # it'll give a basic breakdown

    df = pd.DataFrame([
        {
            "Service": key,
            "Amount": value[0],
            "Count": value[1],
            "Status": "⚠️ Duplicate" if value[1] > 1 else "✓",
            "Actions": "Explain"
        }
        for key, value in items_dict.items()
    ])

    # now to show intereactive table (starts of it? had to kinda search)
    return st.data_editor(
        df,
        column_config={
            "Actions": st.column_config.ButtonColumn(
                "Actions",
                help="Click to get AI explanation"
            )
        },
        hide_index=True
    )



