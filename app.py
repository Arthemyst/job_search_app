import pandas as pd
import streamlit as st

import scraping_functions as sf

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
# Filtering data
df_selected = df[
    (df["position"].isin(selected_position)) & (df["title"].isin(selected_title))
]

st.title("Job offers:")
st.dataframe(df_selected)
