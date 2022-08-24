import datetime

import streamlit as st

import scraping_functions as sf


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

last_day = df["publication_date"].min()
last_date = datetime.datetime.strptime(last_day, "%Y-%m-%d")
today = datetime.date.today()

end_date = st.sidebar.date_input("The latest:", today)
start_date = st.sidebar.date_input("The oldest:", last_date)

# Filtering data
if start_date < end_date:
    df_selected = df[
        (
            (df["position"].isin(selected_position))
            & (df["website"].isin(selected_website))
            & (df["publication_date"] >= str(start_date))
            & (df["publication_date"] <= str(end_date))
        )
    ]
    if len(df_selected) != 0:
        st.dataframe(df_selected)
    else:
        st.write("Change filters parameters to show results.")
else:
    st.write("Error: End date must fall after start date.")
