import datetime
from turtle import color

import streamlit as st

import scraping_functions as sf
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


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
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Count of offers by website.", "Count of offers by position."))
        df_selected_count_by_website = df_selected.groupby('website').count()
        df_selected_count_by_position = df_selected.groupby('position').count()
        fig.add_trace(go.Bar(x=df_selected_count_by_website.index, 
                            y=df_selected_count_by_website['company'],name='website', showlegend=False),
                            row=1, col=1)
        fig.add_trace(go.Bar(x=df_selected_count_by_position.index, 
                            y=df_selected_count_by_position['company'],name='position', showlegend=False), 
                            row=1, col=2)
        # Update yaxis properties
        fig.update_yaxes(title_text="Count", row=1, col=1)
        fig.update_yaxes(title_text="Count", row=1, col=2)
        fig.update_layout( 
            legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1))
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("Change filters parameters to show results!")
else:
    st.write("End date must fall after start date.")
