import streamlit as st
from streamlit_folium import folium_static
from data_loader import ExploreStreetManagerData, connect_to_motherduck
from streamlit_pages import home_page, search_collaborative_street_works, explore_collab_works_sankey_page
from collab_map_generator import create_collab_map


def main():
    st.set_page_config(layout="wide")

    # Load data manager and completed works data only once
    my_token = st.secrets['key']
    data_manager = ExploreStreetManagerData(connect_to_motherduck(my_token, "sm_permit"))

    # Sidebar header
    st.sidebar.header("**Navigation Bar**")
    page = st.sidebar.radio("**Please Select a Page**", [":house: Home",
                                                         ":one: Overview",
                                                         ":two: Flow Charts"])

    if page == ":house: Home":
        home_page()
    elif page == ":one: Overview":
        st.title('Collaborative Streetworks Overview (Jan 2022 to Dec 2023)')
        filtered_df = search_collaborative_street_works(data_manager)
        if filtered_df is not None:
            map_display = create_collab_map(filtered_df)
            if map_display:
                folium_static(map_display, width=1300, height=1000)
            else:
                st.write("No data available to display on the map")
    elif page == ":two: Flow Charts":
        st.title('Collaborative Streetwork Flow Charts (Jan 2022 to Dec 2023)')
        st.markdown("### Select multiple highway authorities and analyse the differences between them - a random one"
                    " has been chosen for you")
        st.info("**A good tip is to select highway authorities within similar areas (e.g. London Boroughs)**")
        explore_collab_works_sankey_page(data_manager)


if __name__ == "__main__":
    main()
