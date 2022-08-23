import pandas as pd
import streamlit as st

import scraping_functions as sf

nofluffjobs_list = sf.nofluffjobs_page_job_offers()
df_raw_1 = pd.DataFrame.from_records(nofluffjobs_list)
df_1 = df_raw_1.copy()
df_1["publication_date"] = pd.to_datetime(
    df_1["publication_date"], infer_datetime_format=True
)
df_1.drop_duplicates(
    subset=["publication_date", "company", "title"], inplace=True, ignore_index=True
)


bulldogjob_list = sf.bulldog_page_job_offers()
df_raw_2 = pd.DataFrame.from_records(bulldogjob_list)
df_2 = df_raw_2.copy()
df_2["publication_date"] = pd.to_datetime(
    df_2["publication_date"], infer_datetime_format=True
)
df_2.drop_duplicates(
    subset=["publication_date", "company", "title"], inplace=True, ignore_index=True
)


df_3 = pd.concat([df_1, df_2], axis=0, ignore_index=True)
df_3.sort_values(["publication_date"], inplace=True, ascending=False)
df_3["publication_date"] = df_3["publication_date"].dt.strftime("%Y-%m-%d")

sector = df_3.groupby("position")

# Sidebar - Position selection
sorted_position_unique = sorted(df_3["position"].unique())
selected_position = st.sidebar.multiselect(
    "Position", sorted_position_unique, sorted_position_unique
)
# Sidebar - Title selection
sorted_title_unique = sorted(df_3["title"].unique())
selected_title = st.sidebar.multiselect(
    "Title", sorted_title_unique, sorted_title_unique
)
# Filtering data
df_selected = df_3[
    (df_3["position"].isin(selected_position)) & (df_3["title"].isin(selected_title))
]
st.title("Job offers:")

st.dataframe(df_selected)
