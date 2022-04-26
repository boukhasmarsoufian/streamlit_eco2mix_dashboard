from datetime import datetime
from matplotlib.pyplot import text, title
from wandb import Plotly
from nbformat import write
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from st_aggrid import AgGrid, GridOptionsBuilder
import random
import plot_functions as plt
import pydeck as pdk
import os 
showWarningOnDirectExecution = False
hide_menu = """
<style>
#MainMenu {
    visibility:hidden;
}
footer{
    visibility:hidden;
}
</style>
"""
footer="""<style>
a:link , a:visited{
color: black;
background-color: #ffe9b5;
text-decoration: underline;
}

a:hover,  a:active {
color: #ba831e;
background-color: transparent;
text-decoration: underline;
}

.footer2 {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #ffe9b5;
color: black;
text-align: center;
}
</style>

<div class="footer2">
<a style='display: block; text-align: center;' href="#co2mix-dashboard" target="_self"> 🔝Back to Top</a>
</div>

"""


st.set_page_config( page_title="CVA dashboards", page_icon=":bar_chart", layout="wide")

st.markdown(hide_menu, unsafe_allow_html=True)
# ---- Data Functions ---- #

@st.cache(allow_output_mutation=True)
def get_data_from_csv(file_path="./DATA/dataset1/eco2mix-national-cons-def.csv"):
    df = pd.read_csv(
    file_path,
    sep=";",
    nrows=10000
    )

    # Add 'Year' column to dataframe
    df["Year"] = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.year
    df["Month"] = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.month
    df["Day"] = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.day
    df['date_offset'] = (df["Month"]*100 + df["Day"] - 320)%1300
    df['Season'] = pd.cut(df['date_offset'], [0, 300, 602, 900, 1300], 
                        labels=['spring', 'summer', 'autumn', 'winter'])
    df["Season"] = df["Season"].astype('object')

    df.replace('ND', 0,inplace=True)

    df["Ech. comm. Allemagne-Belgique (MW)"] = df["Ech. comm. Allemagne-Belgique (MW)"].astype('float64')
    df["Gaz - Cogénération (MW)"] = df["Gaz - Cogénération (MW)"].astype('float64')

    # df.dropna(inplace=True)
    

    df['sum_ech'] =  df[['Ech. comm. Angleterre (MW)', 'Ech. comm. Espagne (MW)','Ech. comm. Italie (MW)','Ech. comm. Suisse (MW)','Ech. comm. Allemagne-Belgique (MW)']].sum(axis=1)

    return df.sort_values(by="Date")

# df_x = get_data_from_csv()
# df_x.to_parquet("./DATA/dataset1/df.parquet.gzip",compression='gzip')
df = pd.read_parquet("./DATA/dataset1/df.parquet.gzip")

# df_y = plt.get_data_from_csv("./DATA/dataset2/points-dinjection-de-biomethane-en-france.csv")
# df_y.to_parquet('./DATA/dataset2/df.parquet.gzip',compression='gzip')
df2 = pd.read_parquet('./DATA/dataset2/df.parquet.gzip')
df2.rename(columns={"Annee mise en service":"Year","Type de site":"Type_de_site"}, inplace=True)

def app():
# Load parquet gzip
    ################################## ---- SIDEBAR ---- ##################################
    keys = random.sample(range(1000, 9999), len(df.columns))

    season = st.sidebar.multiselect(
        "Select Season:",
        options=["winter","spring","summer","autumn"],
        default=["winter","spring","summer","autumn"],
        key=keys[5]
    )

    values, values2 = st.slider(
        'Please select the wanted date range ',
        int(df.Year.min()), int(df.Year.max()), (int(df.Year.min()), int(df.Year.max()))
        )
        
    
    type_de_site = st.sidebar.multiselect(
        "Type de site:",
        options=df2["Type_de_site"].unique(),
        default=df2["Type_de_site"].unique()
    )

    departement = st.sidebar.multiselect(
        "Déprtements:",
        options=df2["Departement"].unique(),
        default=df2["Departement"].unique()
    )

    # Query
    df_selection = df.query(
        "Season == @season & Year >= @values & Year <= @values2"
    )

    
    # Query 2
    df_selection2 = df2.query(
        " Year >= @values & Year <= @values2 & Type_de_site == @type_de_site  & Departement==@departement"
    )

    df_selection2.dropna(inplace=True)
    # plt.ag_grid_table(df_selection2,"Date de mise en service")
    ################################## ---- MAINPAGE ---- ##################################
    st.title(":bar_chart: éCO2mix Dashboard")

    #  ---- Metrics ----  #

    ## Consommation (MW)
    total_consommation = int(df_selection["Consommation (MW)"].sum() )

    ## Prévision J-1 (MW)
    j_1_total_consommation = int(df_selection["Prévision J-1 (MW)"].sum() )

    ## Prévision J (MW)
    j_total_consommation = int(df_selection["Prévision J (MW)"].sum() )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Consommation (MW)",f"{total_consommation:,}")
    col2.metric("Prévision J-1 (MW)",f"{j_1_total_consommation:,}")
    col3.metric("Prévision J (MW)", f"{j_total_consommation:,}")

    st.markdown("""---""")


    #  ---- Call Pyplot functions  ---- #

    fig_consommation_by_year = plt.consommation_bare(df_selection)
    fig_consommation_by_year_line = plt.consommation_Line(df_selection)
    fig_co2_by_year = plt.carbon_bare(df_selection)
    fig_co2_pie_by_year = plt.carbon_pie(df_selection)
    ech_fig = plt.carbon_bar_ech(df_selection)
    fig_ech_by_year = plt.ech_phy_bare(df_selection)
    line_fig = plt.production_line(df_selection)
    fig_3d = plt.scatter3d(df_selection)
    multi_line_fig = plt.multiple_lines(df_selection)


    ### Display figures as columns
    left_column, right_column  = st.columns(2)
    left_column.plotly_chart(fig_consommation_by_year, use_container_width=False)
    right_column.plotly_chart(fig_consommation_by_year_line, use_container_width=False)


    left_column_2, right_column_2  = st.columns(2)
    left_column_2.plotly_chart(fig_co2_by_year, use_container_width=False)
    right_column_2.plotly_chart(fig_co2_pie_by_year, use_container_width=False)

    left_column_3, right_column_3  = st.columns(2)
    left_column_3.plotly_chart(fig_ech_by_year, use_container_width=False)
    right_column_3.plotly_chart(ech_fig, use_container_width=False)


    ### Display figures in a container
    container = st.container()
    with container:
        
        container.markdown("### **La production selon les différentes filières composant le mix énergétique.**")

        container.plotly_chart(multi_line_fig, use_container_width=True)
        
        container.plotly_chart(line_fig, use_container_width=True)
        
    plt.split_coordinates(df_selection2)
    plt.ag_grid_table(df_selection2,"Date de mise en service")
    # git figures
    fig2 = plt.density_mapbox(df_selection2)
    fig = plt.scatter_mapbox(df_selection2)
    
    container2 = st.container()
    with container2:

        container2.plotly_chart(fig_3d, use_container_width=True)
        container2.markdown("### **Points d'injection de Biométhane en France en service**")
        plt.pydeck(df_selection2)
        container2.plotly_chart(fig2, use_container_width=True)
        container2.plotly_chart(fig, use_container_width=True)
        
    

    

    st.markdown(footer,unsafe_allow_html=True)



app()
