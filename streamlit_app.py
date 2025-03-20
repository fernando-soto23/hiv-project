import streamlit as st
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

import altair as alt
import os
from sections.map_section import show_map

st.set_page_config(
    page_title='HIV Project Dashboard',
    page_icon=':⚕️:',
    layout="wide",
)

@st.cache_data
def get_df_data():
    DATA_FILENAME = Path(__file__).parent / 'data/df_hiv_poverty.csv'
    df_hiv_poverty = pd.read_csv(DATA_FILENAME)
    
    df_hiv_poverty['Year'] = pd.to_numeric(df_hiv_poverty['Year'])
    
    return df_hiv_poverty

df_hiv_poverty = get_df_data()

'''
# :drop_of_blood: HIV PROJECT



This project analyzes the relationship between socioeconomic status and HIV prevalence in New York City.
By examining HIV diagnosis rates alongside poverty indicators, we aim to identify potential correlations and disparities across boroughs, age groups, genders, and racial demographics.
'''
st.text("This project analyzes the relationship between HIV prevalence and socioeconomic status in New York City.")

col1, col2 = st.columns(2,  border=True)
with col1:
    st.subheader("HIV y socioeconomics")
    st.image(image="images/data_sources.png", width=660)
    st.text("Data sources from New York. Poverty data includes Unemployment, Poverty, and Deaths, while HIV data covers HIV cases, Viral Suppression, and AIDS.")
with col2:
    st.subheader("Communities")
    st.image(image="images/comunities.png", width=345)
    st.text("The study cases are Demographic Groups, we called them communities. Communities are defined by Year, Boroughs, Age, Sex, Race")



''
''
st.header("Do the socioeconomic factors of NYC communities influence the prevalence of HIV and its associated consequences?")
year_option = st.selectbox(
    'Select Year', 
    options=[2017, 2018], 
    index=0
)
''
''

df_filtered = df_hiv_poverty[df_hiv_poverty['Year'] == year_option]
st.subheader("Is there a correlation between poverty and vulneravility?")
''

col1, col2 = st.columns(2,  border=True)

def plot_correlation_scatter2(df, x_col, y_col, title, x_label, y_label):
    sns.set_style("darkgrid", {"axes.facecolor": "black", "grid.color": "#0E1117"})
    
    plt.figure(figsize=(8,6))
    
    sns.regplot(x=df[y_col], y=df[x_col], scatter_kws={"alpha":0.5}, line_kws={"color":"red"})
    
    plt.xlabel(x_label, color='white')
    plt.ylabel(y_label, color='white')
    plt.title(title, color='white')
    
    plt.tick_params(axis='both', colors='white')
    
    plt.gcf().set_facecolor('#0E1117')
    
    st.pyplot(plt)
def plot_correlation_scatter3(df, x_col, y_col, title, x_label, y_label):
    sns.set_style("darkgrid", {"axes.facecolor": "black", "grid.color": "#0E1117"})
    
    plt.figure(figsize=(8,6))
    
    sns.regplot(x=df[x_col], y=df[y_col], scatter_kws={"alpha":0.5}, line_kws={"color":"red"})
    
    plt.xlabel(x_label, color='white')
    plt.ylabel(y_label, color='white')
    plt.title(title, color='white')
    
    plt.tick_params(axis='both', colors='white')
    
    plt.gcf().set_facecolor('#0E1117')
    
    st.pyplot(plt)
''
''
with col1:
    col1.subheader(f"Deaths and unemployment")
    plot_correlation_scatter2(
        df_filtered, 
        x_col="weighted_No_Work", 
        y_col="Deaths", 
        title=f"Correlation between deaths and unemployment ({year_option})", 
        x_label="People without rork (weighted_No_Work)", 
        y_label="Number of deaths (Deaths)"
    )
    col1.info("Higher unemployment may be linked to higher mortality rates, possibly due to factors like poor access to healthcare, increased stress, or lack of social support in unemployed communities", icon="ℹ️")


with col2:
    col2.subheader(f"Viral suppression and poverty rate")
    plot_correlation_scatter3(
        df_filtered, 
        x_col="poverty_rate", 
        y_col="% viral suppression", 
        title=f"Correlation between viral suppression and poverty rate ({year_option})", 
        x_label="Poverty rate (%)", 
        y_label="Viral suppression (%)"
    )
    col2.info('Communities facing higher poverty levels may struggle more with achieving viral suppression, which could be due to limited access to healthcare, medication, or support.', icon="ℹ️")

st.subheader("Which communities are most vulnerable?")

def plot_top_aids_communities(df):
    top_5 = df.sort_values(by="AIDS diagnoses", ascending=False).head(10).copy()
    top_5["Community"] = top_5[['Borough', 'Gender', 'Age', 'Race']].astype(str).agg(' | '.join, axis=1)
    chart_data = top_5[["Community", "AIDS diagnoses"]]

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Community', sort=alt.EncodingSortField(field='AIDS diagnoses', order='descending')),
        y=alt.Y('AIDS diagnoses', title="AIDS diagnoses"),
        color=alt.Color('AIDS diagnoses', scale=alt.Scale(scheme='blues'), legend=None)
    ).properties(
        height=600,
        title = "Top 10 Communities by AIDS diagnoses"
    )
    st.altair_chart(chart, use_container_width=True)

def plot_top_poverty_communities(df):
    top_5 = df.sort_values(by="poverty_rate", ascending=False).head(10).copy()
    top_5["Community"] = top_5[['Borough', 'Gender', 'Age', 'Race']].astype(str).agg(' | '.join, axis=1)
    chart_data = top_5[["Community", "poverty_rate"]]

    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('Community', sort=alt.EncodingSortField(field='poverty_rate', order='descending')),
        y=alt.Y('poverty_rate', title="Poverty rate"),
        color=alt.Color('poverty_rate', scale=alt.Scale(scheme='blues'), legend=None)
    ).properties(
        height=600,
        title = "Top 10 Communities by poverty rate"
    )
    st.altair_chart(chart, use_container_width=True)


col1 = st.columns(1,  border=True)[0]
with col1:
    plot_top_aids_communities(df_filtered)
    st.info("Out of the 10 most vulnerable communities, none are of White race.", icon="🚨")
    st.divider()
    plot_top_poverty_communities(df_filtered)
    st.info("Out of the 10 most poverty communities, none are of White race.", icon="🚨")

show_map(df_filtered)

''
''
st.text("© 2025 Thoughtworks")