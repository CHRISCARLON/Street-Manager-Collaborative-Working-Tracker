import folium
import streamlit
from folium.plugins import MarkerCluster
import geopandas as gpd
import branca


@streamlit.cache_data
def create_collab_map(df):
    if df is None or df.empty:
        return None

    # Convert WKT to geometry and set original CRS
    df['geometry'] = gpd.GeoSeries.from_wkt(df['works_location_coordinates'])
    geodf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:27700")

    geodf = geodf.to_crs(epsg=4326)

    # Calculate centroids
    geodf['centroid'] = geodf.geometry.centroid
    geodf["latitude"] = geodf.centroid.y
    geodf["longitude"] = geodf.centroid.x

    # Create a Folium map
    m = folium.Map(location=[54.5, -3.5], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in geodf.iterrows():
        # Create HTML content for each marker dynamically
        html_content = f"""
            <div style="font-size: 12px; font-family: monospace">
                <h4>Promoter: {row['promoter_organisation']}</h4>
                <p>Highway Authority: {row['highway_authority']}<br>
                   Month: {row['month']}<br>
                   Year: {row['year']}<br>
                   Street Name: {row['street_name']}<br>
                   Activity: {row['activity_type']}<br>
                   Collaboration Type: {row['collaboration_type']}<br>
                   Work Category: {row['work_category']}</p>
            </div>
        """
        iframe = branca.element.IFrame(html=html_content, width=200, height=185)
        popup = folium.Popup(iframe, parse_html=True)

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup
        ).add_to(marker_cluster)

    return m
