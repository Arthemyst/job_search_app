import datetime
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

import scraping_functions as sf
from datetime import datetime, timezone, date
import pytz

st.title("Job offers:")
df = sf.merge_dataframes()
if st.button("Update offers data"):
    st.legacy_caching.clear_cache()
    df = sf.merge_dataframes()
    PL = pytz.timezone("Europe/Warsaw")
    load_datetime = datetime.now().astimezone(PL).strftime("%m/%d/%Y, %H:%M:%S")
    st.write(f"Update time: {load_datetime} CEST")
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
last_date = datetime.strptime(last_day, "%Y-%m-%d")
today = date.today()

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

        st.download_button(
            label="Download data as CSV",
            data=df_selected.to_csv().encode("utf-8"),
            file_name="offers.csv",
            mime="text/csv",
        )
        fig1 = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=(
                "Count of offers by website.",
                "Count of offers by position.",
            ),
        )
        df_selected_count_by_website = df_selected.groupby("website").count()
        df_selected_count_by_position = df_selected.groupby("position").count()
        fig1.add_trace(
            go.Bar(
                x=df_selected_count_by_website.index,
                y=df_selected_count_by_website.company,
                name="website",
                showlegend=False,
                text=df_selected_count_by_website.company,
            ),
            row=1,
            col=1,
        )
        fig1.add_trace(
            go.Bar(
                x=df_selected_count_by_position.index,
                y=df_selected_count_by_position.company,
                name="position",
                showlegend=False,
                text=df_selected_count_by_position.company,
            ),
            row=2,
            col=1,
        )
        # Update yaxis properties
        fig1.update_yaxes(title_text="Count", row=1, col=1)
        fig1.update_yaxes(title_text="Count", row=2, col=1)
        fig1.update_layout(
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
            ),
            height=1000,
            width=800,
        )
        st.plotly_chart(fig1, use_container_width=True)

        df_selected_count_by_date = df_selected.groupby(["publication date"]).agg(
            "count"
        )

        fig2 = px.line(
            y=df_selected_count_by_date.company,
            x=df_selected_count_by_date.index,
            markers=True,
            text=df_selected_count_by_date.company,
            title="Count of offers by publication date.",
        )
        fig2.update_yaxes(title_text="Count of offers")
        fig2.update_xaxes(title_text="Publication date")
        fig2.update_traces(textposition="top left")
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.write("Change filters parameters to show results!")
else:
    st.write("End date must fall after start date.")
