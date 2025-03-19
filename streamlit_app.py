import streamlit as st
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='HIV Project Dashboard',
    page_icon=':⚕️:',
)

@st.cache_data
def get_df_data():
    DATA_FILENAME = Path(__file__).parent / 'data/df_hiv_poverty.csv'
    df_hiv_poverty = pd.read_csv(DATA_FILENAME)
    
    df_hiv_poverty['Year'] = pd.to_numeric(df_hiv_poverty['Year'])
    
    return df_hiv_poverty

# Cargar los datos
df_hiv_poverty = get_df_data()

'''
# ⚕️ HIV PROJECT

This is a description of what our project are pretending to solve
This is a description of what our project are pretending to solve
This is a description of what our project are pretending to solve
This is a description of what our project are pretending to solve
'''
''
''
# Seleccionar año
year_option = st.selectbox(
    'Select Year', 
    options=[2017, 2018], 
    index=0  # Puedes poner el año por defecto
)

# Filtrar DataFrame según el año seleccionado
df_filtered = df_hiv_poverty[df_hiv_poverty['Year'] == year_option]

def plot_correlation_scatter2(df, x_col, y_col, title, x_label, y_label):
    # Cambiar el estilo del gráfico de seaborn para tener fondo oscuro
    sns.set_style("darkgrid", {"axes.facecolor": "black", "grid.color": "#0E1117"})
    
    plt.figure(figsize=(8,6))
    
    # Graficar el gráfico de dispersión y la línea de regresión
    sns.regplot(x=df[y_col], y=df[x_col], scatter_kws={"alpha":0.5}, line_kws={"color":"red"})
    
    # Cambiar color de los ejes, etiquetas y título
    plt.xlabel(x_label, color='white')
    plt.ylabel(y_label, color='white')
    plt.title(title, color='white')
    
    # Cambiar el color de los ticks de los ejes
    plt.tick_params(axis='both', colors='white')
    
    # Cambiar el fondo de la figura a negro
    plt.gcf().set_facecolor('#0E1117')
    
    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

# Llamada a la función con los datos filtrados
plot_correlation_scatter2(
    df_filtered, 
    x_col="weighted_No_Work", 
    y_col="Deaths", 
    title=f"Correlation between Deaths and Unemployment ({year_option})", 
    x_label="People without Work (weighted_No_Work)", 
    y_label="Number of Deaths (Deaths)"
)


