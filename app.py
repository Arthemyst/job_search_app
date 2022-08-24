import datetime

import streamlit as st

import scraping_functions as sf

st.title("Job offers:")
df = sf.merge_dataframes()


sector = df.groupby("position")

# Sidebar - Position selection
sorted_position_unique = sorted(df["position"].unique())
selected_position = st.sidebar.multiselect(
    "Position", sorted_position_unique, sorted_position_unique
)
# Sidebar - Title selection
sorted_title_unique = sorted(df["title"].unique())
selected_title = st.sidebar.multiselect(
    "Title", sorted_title_unique, sorted_title_unique
)
# Sidebar - date range

last_day = df["publication_date"].min()
last_date = datetime.datetime.strptime(last_day, "%Y-%m-%d")
today = datetime.date.today()

end_date = st.sidebar.date_input("End date", today)
start_date = st.sidebar.date_input("Start date", last_date)


# Filtering data
if start_date < end_date:
    df_selected = df[
        (df["position"].isin(selected_position))
        & (
            df["title"].isin(selected_title)
            & (df["publication_date"] >= str(start_date))
            & (df["publication_date"] <= str(end_date))
        )
    ]
    st.dataframe(df_selected)
else:
    st.write("Error: End date must fall after start date.")
