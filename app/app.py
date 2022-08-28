import datetime

import streamlit as st

import app.scraping_functions as sf


st.title("Job offers:")
df = sf.merge_dataframes()

# Sidebar - Position selection
sorted_position_unique = sorted(df["position"].unique())
selected_position = st.sidebar.multiselect(
    "Position", sorted_position_unique, sorted_position_unique
)
# Sidebar - website selection

sorted_websites_unique = df["website"].unique()

selected_website = st.sidebar.multiselect(
    "Website:", sorted_websites_unique, sorted_websites_unique
)

# Sidebar - date range

last_day = df["publication date"].min()
last_date = datetime.datetime.strptime(last_day, "%Y-%m-%d")
today = datetime.date.today()

end_date = st.sidebar.date_input("To:", today)
start_date = st.sidebar.date_input("From:", last_date)

# Filtering data
if start_date <= end_date:
    df_selected = df[
        (
            (df["position"].isin(selected_position))
            & (df["website"].isin(selected_website))
            & (df["publication date"] >= str(start_date))
            & (df["publication date"] <= str(end_date))
        )
    ]
    if len(df_selected) != 0:
        st.dataframe(df_selected)
    else:
        st.write("Change filters parameters to show results!")
else:
    st.write("End date must fall after start date.")
