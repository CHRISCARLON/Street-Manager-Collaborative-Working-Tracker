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

    # Calculate mean location for initial map center
    mean_latitude = geodf["latitude"].mean()
    mean_longitude = geodf["longitude"].mean()

    # Create a Folium map centered on the mean location
    m = folium.Map(location=[mean_latitude, mean_longitude], zoom_start=8)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in geodf.iterrows():
        # Create HTML content for each marker dynamically
        html_content = f"""
            <div style="font-size: 12px; font-family: monospace">
                <h4><b>Promoter:</b> {row['promoter_organisation']}</h4>
                <p><b>Highway Authority:</b> {row['highway_authority']}<br>
                   <b>Month:</b> {row['month']}<br>
                   <b>Year:</b> {row['year']}<br>
                   <b>Street Name:</b> {row['street_name']}<br>
                   <b>Activity:</b> {row['activity_type']}<br>
                   <b>Collaboration Type:</b> {row['collaboration_type']}<br>
                   <b>Work Category:</b> {row['work_category']}</p>
            </div>
        """
        iframe = branca.element.IFrame(html=html_content, width=265, height=195)
        popup = folium.Popup(iframe, parse_html=True)

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup
        ).add_to(marker_cluster)

    return m
