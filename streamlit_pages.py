import streamlit as st
from data_loader import get_cached_completed_works
from sankey_generator import prepare_completed_sankey_data
import pandas as pd
from constants import london_highway_authorities, columns_to_keep


# Home Page
def home_page():
    st.title(':mag_right: Welcome to the Streetworks Collaboration Tracker')
    st.info("""
    **This app contains public sector information licensed under the Open Government Licence v3.0
    (DfT Street Manager Data).**
    \n**Please note that this tracker is for educational purposes only and does not have the 
    endorsement, affiliation, support or approval of the Secretary of State for Transport.**
    \n**If you notice a bug or want to contribute please email me at <StreetManagerExplorer@gmail.com> or via GitHub.**
    """)


# Overview Page
def search_collaborative_street_works(data_manager):
    df = get_cached_completed_works(data_manager)

    df_collaborative = df[columns_to_keep]

    # Filter for London highway authorities
    df_london = df_collaborative[df_collaborative['highway_authority'].isin(london_highway_authorities)]

    # Calculate the overall total number of records
    total_records_overall = len(df_collaborative)
    total_records_london = len(df_london)  # Total for London

    # Find the promoter with the most collaborations and count
    promoter_counts = df_collaborative['promoter_organisation'].value_counts()
    top_promoter, top_promoter_count = promoter_counts.idxmax(), promoter_counts.max()

    london_promoter_counts = df_london['promoter_organisation'].value_counts()
    top_london_promoter, top_london_promoter_count = london_promoter_counts.idxmax(), london_promoter_counts.max()

    # Find the highway authority with the most collaborations and count
    authority_counts = df_collaborative['highway_authority'].value_counts()
    top_authority, top_authority_count = authority_counts.idxmax(), authority_counts.max()

    london_authority_counts = df_london['highway_authority'].value_counts()
    london_top_authority, london_top_authority_count = london_authority_counts.idxmax(), london_authority_counts.max()

    # Create a DataFrame for the table
    table_data = {
        'Category': ['Total Collaborations', 'Top Works Promoter', 'Top Highway Authority'],
        'Detail': [f'{total_records_overall} collaborations',
                   f'{top_promoter} with {top_promoter_count} collaborations',
                   f'{top_authority} with {top_authority_count} collaborations']
    }
    info_df = pd.DataFrame(table_data)

    # Create a DataFrame for London-specific table
    london_table_data = {
        'Category': ['Total London Collaborations', 'Top London Works Promoter', 'Top London Highway Authority'],
        'Detail': [f'{total_records_london} collaborations',
                   f'{top_london_promoter} with {top_london_promoter_count} collaborations',
                   f'{london_top_authority} with {london_top_authority_count} collaborations']
    }
    london_info_df = pd.DataFrame(london_table_data)

    # Display the tables side by side
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Overall Collaboration Stats")
        st.dataframe(info_df, hide_index=True)
    with col2:
        st.markdown("### Overall Collaboration Stats for London")
        st.dataframe(london_info_df, hide_index=True)

    # Get unique values for filters directly from df_collaborative
    unique_highway_authorities = df_collaborative['highway_authority'].unique()
    unique_promoter_organisations = df_collaborative['promoter_organisation'].unique()
    unique_months = df_collaborative['month'].unique()
    unique_years = df_collaborative['year'].unique()
    unique_activity_types = df_collaborative['activity_type'].unique()
    unique_work_categories = df_collaborative['work_category'].unique()
    unique_street_names = df_collaborative['street_name'].unique()

    # Sidebar filters
    selected_highway_authorities = st.sidebar.multiselect('Select Highway Authorities',
                                                          unique_highway_authorities)
    selected_promoter_organisations = st.sidebar.multiselect('Select Promoter Organisations',
                                                             unique_promoter_organisations)
    selected_months = st.sidebar.multiselect('Select Months', unique_months)
    selected_years = st.sidebar.multiselect('Select Years', unique_years)
    selected_activity_types = st.sidebar.multiselect('Select Activity Types', unique_activity_types)
    selected_work_categories = st.sidebar.multiselect('Select Work Categories', unique_work_categories)
    selected_street_names = st.sidebar.multiselect('Select Street Names', unique_street_names)

    # Apply any filter
    filter_applied = any([
        selected_highway_authorities,
        selected_promoter_organisations,
        selected_months,
        selected_years,
        selected_activity_types,
        selected_work_categories,
        selected_street_names
    ])

    if filter_applied:
        # Apply filters conditionally
        if selected_highway_authorities:
            df_collaborative = df_collaborative[df_collaborative['highway_authority'].isin(selected_highway_authorities)]
        if selected_promoter_organisations:
            df_collaborative = df_collaborative[df_collaborative['promoter_organisation'].isin(selected_promoter_organisations)]
        if selected_months:
            df_collaborative = df_collaborative[df_collaborative['month'].isin(selected_months)]
        if selected_years:
            df_collaborative = df_collaborative[df_collaborative['year'].isin(selected_years)]
        if selected_activity_types:
            df_collaborative = df_collaborative[df_collaborative['activity_type'].isin(selected_activity_types)]
        if selected_work_categories:
            df_collaborative = df_collaborative[df_collaborative['work_category'].isin(selected_work_categories)]
        if selected_street_names:
            df_collaborative = df_collaborative[df_collaborative['street_name'].isin(selected_street_names)]

        columns_to_display = ["promoter_organisation",
                              "highway_authority",
                              "work_category",
                              "activity_type",
                              "collaboration_type",
                              "permit_reference_number",
                              "street_name",
                              "month",
                              "year",
                              "actual_start_date_time",
                              "actual_end_date_time",
                              "works_location_coordinates"]
        df_display = df_collaborative[columns_to_display].reset_index(drop=True)

        st.markdown("### Filtered Selection Overview")
        st.dataframe(df_display, hide_index=True)
        return df_display
    else:
        st.info("**Please select at least one filter to view the data.**")
        return None


# Flow Chart Sankey Page
def explore_collab_works_sankey_page(data_manager):
    df_completed_works = get_cached_completed_works(data_manager)

    # Get unique values for filters directly from df_completed_works
    unique_highway_authorities = df_completed_works['highway_authority'].unique()
    unique_months = df_completed_works['month'].unique()
    unique_years = df_completed_works['year'].unique()  # Extracting unique years
    unique_activity_types = df_completed_works['activity_type'].unique()
    unique_work_categories = df_completed_works['work_category'].unique()

    # Sidebar filters
    selected_highway_authorities = st.sidebar.multiselect('Select Highway Authorities', unique_highway_authorities,
                                                          default=unique_highway_authorities[0])
    selected_months = st.sidebar.multiselect('Select Months', unique_months, default=unique_months)
    selected_years = st.sidebar.multiselect('Select Years', unique_years, default=unique_years)  # Year filter
    selected_activity_types = st.sidebar.multiselect('Select Activity Types', unique_activity_types,
                                                     default=unique_activity_types)
    selected_work_categories = st.sidebar.multiselect('Select Work Categories', unique_work_categories,
                                                      default=unique_work_categories)

    # Display Sankey diagram based on the selected filters
    filtered_data = df_completed_works[
        (df_completed_works['highway_authority'].isin(selected_highway_authorities)) &
        (df_completed_works['month'].isin(selected_months)) &
        (df_completed_works['year'].isin(selected_years)) &  # Filtering by selected years
        (df_completed_works['activity_type'].isin(selected_activity_types)) &
        (df_completed_works['work_category'].isin(selected_work_categories))
        ]

    if not filtered_data.empty:
        fig = prepare_completed_sankey_data(filtered_data, selected_highway_authorities, selected_months,
                                            selected_years, selected_activity_types, selected_work_categories)
        st.plotly_chart(fig)
    else:
        st.info("**Please select filters to view the Sankey diagram!**")