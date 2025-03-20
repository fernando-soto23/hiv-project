import folium
from streamlit_folium import folium_static
import json
import os
import streamlit as st
from pathlib import Path


def load_geojson():
    try:
        GEOJSON_PATH = Path(__file__).parent.parent / 'data/nyc_boroughs.geojson'
        with open(GEOJSON_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading GeoJSON: {e}")
        return None


def show_map(df_filtered):
    nyc_geojson = load_geojson()
    st.header("How has HIV/AIDS distributed in NYC?")


    map_metric = st.selectbox(
            "Select Map Metric",
            ["HIV diagnoses", "AIDS diagnoses", "poverty_rate", "% viral suppression", "Deaths"]
    )

    borough_data = df_filtered.groupby('Borough').agg({
        'HIV diagnoses': 'sum',
        'AIDS diagnoses': 'sum',
        'poverty_rate': 'mean',
        '% viral suppression': 'mean',
        'Deaths': 'sum'
    }).reset_index()

    def standardize_borough_name(name):
        name = name.strip()
        if name.lower() == "staten island":
            return "Staten Island"
        elif name.lower() == "manhattan":
            return "Manhattan"
        elif name.lower() == "brooklyn":
            return "Brooklyn"
        elif name.lower() == "queens":
            return "Queens"
        elif name.lower() == "bronx":
            return "Bronx"
        return name

    borough_data['Borough'] = borough_data['Borough'].apply(standardize_borough_name)

    if nyc_geojson is not None:
        try:
            m = folium.Map(
                    location=[40.7128, -74.0060],
                    zoom_start=10,
                    tiles="Cartodb dark_matter"
                )

            choropleth = folium.Choropleth(
                    geo_data=nyc_geojson,
                    name="choropleth",
                    data=borough_data,
                    columns=["Borough", map_metric],
                    key_on="feature.properties.name",
                    fill_opacity=0.7,
                    line_opacity=0.2,
                    legend_name=map_metric
                ).add_to(m)

            choropleth.geojson.add_child(
                    folium.features.GeoJsonTooltip(
                        fields=['name'],
                        aliases=['Borough:'],
                    )
                )

            for feature in choropleth.geojson.data['features']:
                    borough_name = feature['properties']['name']
                    borough_stats = borough_data[borough_data['Borough'] == borough_name]

                    if not borough_stats.empty:
                        html = f"""
                        <div>
                            <h4>{borough_name}</h4>
                            <table style="width: 100%;">
                                <tr><td>HIV diagnoses:</td><td style="text-align: right;">{borough_stats['HIV diagnoses'].values[0]}</td></tr>
                                <tr><td>AIDS diagnoses:</td><td style="text-align: right;">{borough_stats['AIDS diagnoses'].values[0]}</td></tr>
                                <tr><td>Deaths:</td><td style="text-align: right;">{borough_stats['Deaths'].values[0]}</td></tr>
                                <tr><td>Poverty rate:</td><td style="text-align: right;">{borough_stats['poverty_rate'].values[0]:.2f}%</td></tr>
                                <tr><td>Viral suppression:</td><td style="text-align: right;">{borough_stats['% viral suppression'].values[0]:.2f}%</td></tr>
                            </table>
                        </div>
                        """

                        popup = folium.Popup(folium.Html(html, script=True))
                        folium.GeoJson(
                            feature,
                            style_function=lambda x: {'fillOpacity': 0, 'weight': 0},
                            popup=popup
                        ).add_to(m)

            folium_static(m, width=850, height=500)
        except Exception as e:
            st.error(f"Error creating map: {e}")

            if 'features' in nyc_geojson:
                    borough_names_geojson = [feature['properties'].get('name', 'Unknown') for feature in nyc_geojson['features']]
                    st.write("Borough names in GeoJSON:", borough_names_geojson)
                    st.write("Borough names in dataset:", borough_data['Borough'].tolist())
