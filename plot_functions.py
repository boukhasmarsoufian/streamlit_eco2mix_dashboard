import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder
import random 
import pydeck as pdk


# Total Consommation BARE
def consommation_bare(df_selection):
    consommation_by_year_bare = (
        df_selection.groupby(by=["Year"]).sum()[["Consommation (MW)"]].sort_values(by="Year")
    )
    # fig_consommation_by_year= go.Figure()

    fig_consommation_by_year= px.bar(
        consommation_by_year_bare,
        y= "Consommation (MW)",
        x = consommation_by_year_bare.index,
        # orientation="h",
        title="<b>Estimation de la consommation d'énergie réalisée en France par an.</b>",
        color_discrete_sequence=["#0083B8"]
    )


    fig_consommation_by_year.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    return fig_consommation_by_year

# Echang physique BARE
def ech_phy_bare(df_selection):
    ech_by_year_bare = (
        df_selection.groupby(by=["Year"]).sum()[["Ech. physiques (MW)"]].sort_values(by="Year")
    )
    # fig_consommation_by_year= go.Figure()

    fig_ech_by_year= px.bar(
        ech_by_year_bare,
        y= "Ech. physiques (MW)",
        x = ech_by_year_bare.index,
        # orientation="h",
        title="<b>Total des échanges physiques entre la France et les pays frontières.</b>",
        color_discrete_sequence=["#0083B8"]
    )


    fig_ech_by_year.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    return fig_ech_by_year

# Total Consommation BARE
def consommation_Line(df_selection):
    consommation_by_year_line = (
        df_selection.groupby(by=["Year"]).sum()[["Consommation (MW)"]].sort_values(by="Year")
    )
    fig_consommation_by_year_line = go.Figure()

    fig_consommation_by_year_line.add_trace(go.Scatter(x=consommation_by_year_line.index, y=consommation_by_year_line["Consommation (MW)"],
                    mode='lines+markers',
                    name='lines+markers',
                    text=consommation_by_year_line["Consommation (MW)"]))

    return fig_consommation_by_year_line

# Total of carbon emissions LINE
def carbon_bare(df_selection):
    co2_by_year_line = (
        df_selection.groupby(by=["Year"]).sum()[["Taux de CO2 (g/kWh)"]].sort_values(by="Taux de CO2 (g/kWh)")
    )

    fig_co2_by_year= px.bar(
        co2_by_year_line,
        y= "Taux de CO2 (g/kWh)",
        x = co2_by_year_line.index,
        # orientation="h",
        title="<b>Estimation des émissions de CO2 générées par production électrique en France.</b>",
        # color="Taux de CO2 (g/kWh)"
        color_discrete_sequence=["#0083B8"]
    )


    fig_co2_by_year.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    return fig_co2_by_year

# Total Consommation PIE
def carbon_pie(df_selection):

    fig_co2_pie_by_year= px.pie(
        data_frame=df_selection,
        hole = 0.6,
        values="Taux de CO2 (g/kWh)",
        # labels = co2_by_year_pie,
        names="Year",
        # orientation="h",
        color_discrete_sequence=["#0083B8"]
    )


    fig_co2_pie_by_year.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    return fig_co2_pie_by_year

# Total Echanges commerciaux - bar chart .
def carbon_bar_ech(df_selection):
    co2_by_year_line = (
        df_selection.groupby(by=["Year"]).sum()[["sum_ech"]].sort_values(by="Year")
    )
    ech_fig= px.bar(
        data_frame=co2_by_year_line,
        y= "sum_ech",
        x = co2_by_year_line.index,
        # orientation="h",
        color_discrete_sequence=["#0083B8"],
        title="<b>Total des échanges commerciaux entre la France et les pays frontières<b>"
    )


    ech_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    return ech_fig

# Total Fioul prod Line
def production_line(df_selection):

    line_fig = px.line(df_selection.sort_values(by=['Date']), x="Date", y="Fioul (MW)" ,title='<b>La production du fioul en France en (MW)</b>',color="Season")

    line_fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    return line_fig

def scatter3d(df_selection):


    fig = px.scatter_3d(df_selection, z='Year', y='Taux de CO2 (g/kWh)', x='Consommation (MW)',
                 color="Year",title="<b>Nuage de points 3D, Consomation d'énergie et Taux de CO2</b>")
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )
    return fig

def multiple_lines(df_selection):

    # df_new = df_selection[["Fioul (MW)","Charbon (MW)","date_offset","Day","Date"]].copy()


    df_new = (
            df_selection.groupby(by=["Date"]).sum()[["Fioul (MW)","Charbon (MW)","Gaz (MW)","Nucléaire (MW)","Eolien (MW)","Solaire (MW)","Hydraulique (MW)"]].sort_values(by="Date")
        )

    df_new['Date'] = df_new.index

    fig = px.area(df_new, x="Date", y=df_new.columns[:-1]) #df_new.columns[1:-6]
    fig.update_xaxes(rangeslider_visible=True)
    return fig

@st.cache(allow_output_mutation=True)
def get_data_from_csv(file_path="./DATA/dataset1/eco2mix-national-cons-def.csv"):
    df = pd.read_csv(
    file_path,
    sep=";",
    nrows=100
    )

    # # Add 'Year' column to dataframe
    # df["Year"] = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.year
    # df["Month"] = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.month
    # df["Day"] = pd.to_datetime(df["Date"], format="%Y-%m-%d").dt.day
    # df['date_offset'] = (df["Month"]*100 + df["Day"] - 320)%1300
    # df['Season'] = pd.cut(df['date_offset'], [0, 300, 602, 900, 1300], 
    #                     labels=['spring', 'summer', 'autumn', 'winter'])
    # df["Season"] = df["Season"].astype('object')

    # df.replace('ND', 0,inplace=True)

    # df["Ech. comm. Allemagne-Belgique (MW)"] = df["Ech. comm. Allemagne-Belgique (MW)"].astype('float64')
    # df["Gaz - Cogénération (MW)"] = df["Gaz - Cogénération (MW)"].astype('float64')

    # # df.dropna(inplace=True)
    

    # df['sum_ech'] =  df[['Ech. comm. Angleterre (MW)', 'Ech. comm. Espagne (MW)','Ech. comm. Italie (MW)','Ech. comm. Suisse (MW)','Ech. comm. Allemagne-Belgique (MW)']].sum(axis=1)

    return df


def choropleth_mapbox(geo_df): 
    # create the plot

    # st.text(newtrok_points["features"][0]["geometry"]["coordinates"][0])

    # px.set_mapbox_access_token(open(".mapbox_token").read())
    fig = px.scatter_mapbox(data_frame = geo_df,
                            lat="lat",
                            lon="log",
                            hover_name="Reseau",
                            zoom=1)
    return fig

# df2 = get_data_from_csv()
# df2.to_parquet('.\DATA\dataset1\df.parquet.gzip',compression='gzip')

def split_coordinates(df):
    # Create two lists for the loop results to be placed
    lat = []
    lon = []
    # For each row in a varible,
    for row in df["Coordonnees"]:
        # Try to,
        try:
            # Split the row by comma and append
            # everything before the comma to lat
            lat.append(row.split(',')[0])
            # Split the row by comma and append
            # everything after the comma to lon
            lon.append(row.split(',')[1])
        # But if you get an error
        except:
            # append a missing value to lat
            lat.append(np.NaN)
            # append a missing value to lon
            lon.append(np.NaN)

    # Create two new columns from lat and lon
    df['lat'] = lat
    df['log'] = lon
    df["lat"] = df["lat"].astype('float')
    df["log"] = df["log"].astype('float')

    return df


def scatter_mapbox(df):

    px.set_mapbox_access_token("pk.eyJ1Ijoicml0bzEwIiwiYSI6ImNsMmFoZXlkbTAxcW4zY25jd3liYWdrbmEifQ.Ych9pZYdcmEoonbyDkSsrQ")

    fig = px.scatter_mapbox(df, lat="lat", lon="log",color="Code Region", size="Capacite de production (GWh/an)", labels="Nom du site",
                        color_continuous_scale=px.colors.cyclical.IceFire, center={'lat': 46.37638, 'lon': 2.213749}, size_max=22,zoom=3.8)
    return fig


def ag_grid_table(df, sort_variable):

    keys = random.sample(range(1000, 9999), len(df.columns))
    x = random.randint(1,len(keys))
    available_themes = ["streamlit", "light", "dark", "blue", "fresh", "material"]
    # selected_theme = st.selectbox("Theme", available_themes)
    gb = GridOptionsBuilder.from_dataframe(df)
    list_colors = [x for x in range(1000) if x%2!=0]
    gb.configure_selection('multiple', pre_selected_rows=list_colors)
        
    response = AgGrid(df.head(1000).sort_values(by=[sort_variable]), 
                        editable=True,
                        theme="streamlit", 
                        gridOptions=gb.build(),
                        update_mode="no_update",
                        key=keys[0])
    return response


def density_mapbox(df):
    # px.set_mapbox_access_token("pk.eyJ1Ijoicml0bzEwIiwiYSI6ImNsMmFoZXlkbTAxcW4zY25jd3liYWdrbmEifQ.Ych9pZYdcmEoonbyDkSsrQ")
    fig = px.density_mapbox(df, lat='lat', lon='log', z='Capacite de production (GWh/an)', radius=10,
                        center={'lat': 46.37638, 'lon': 2.213749}, zoom=3.8,
                        mapbox_style="stamen-terrain")
    return fig


def pydeck(df_selected):

    st.pydeck_chart(pdk.Deck(
        # map_style = "mapbox://styles/mapbox/light-v9",
        initial_view_state=pdk.ViewState(
            latitude= 46.37638,
            longitude=2.213749,
            zoom=5.2,
            pitch=50
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=df_selected,
                get_position='[log,lat]',
                auto_highlight=True,
                elevation_scale=40,
                pickable=True,
                elevation_range=[0, 3000],
                extruded=True,
                coverage=30,
                radius=200,
                
            ),
        ],
    ), use_container_width=True) 
