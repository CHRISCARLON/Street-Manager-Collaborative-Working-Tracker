import duckdb
import streamlit as st


# Quack quack

@st.cache_resource
def connect_to_motherduck(token, database):
    """
    Establishes a MotherDuck connection.
    """
    connection_string = f'md:{database}?motherduck_token={token}'
    quack = duckdb.connect(connection_string)
    return quack


# Class for creating duckdb queries
class ExploreStreetManagerData:
    def __init__(self, quack):
        self.quack = quack

    def get_all_completed_works(self):
        """
        Fetch records for all completed collaborative works between 2022 and 2023.
        """
        query = """
        SELECT filename,
            activity_type,
            actual_end_date_time,
            actual_start_date_time,
            area_name,
            close_footway_ref,
            collaboration_type,
            collaboration_type_ref,
            collaborative_working,
            current_traffic_management_type,
            current_traffic_management_type_ref,
            current_traffic_management_update_date,
            highway_authority,
            highway_authority_swa_code,
            is_deemed,
            is_traffic_sensitive,
            is_ttro_required,
            permit_conditions,
            permit_reference_number,
            permit_status,
            promoter_organisation,
            promoter_swa_code,
            road_category,
            street_name,
            town,
            traffic_management_type,
            traffic_management_type_ref,
            usrn,
            work_category,
            work_reference_number,
            work_status_ref,
            works_location_coordinates,
            works_location_type,
            year,
            month,
            event_type
        FROM permit_2023_final
        WHERE work_status_ref = 'completed' 
        AND collaborative_working = 'Yes'
        AND event_type = 'work_stop_event'
        UNION ALL
        SELECT filename,
            activity_type,
            actual_end_date_time,
            actual_start_date_time,
            area_name,
            close_footway_ref,
            collaboration_type,
            collaboration_type_ref,
            collaborative_working,
            current_traffic_management_type,
            current_traffic_management_type_ref,
            current_traffic_management_update_date,
            highway_authority,
            highway_authority_swa_code,
            is_deemed,
            is_traffic_sensitive,
            is_ttro_required,
            permit_conditions,
            permit_reference_number,
            permit_status,
            promoter_organisation,
            promoter_swa_code,
            road_category,
            street_name,
            town,
            traffic_management_type,
            traffic_management_type_ref,
            usrn,
            work_category,
            work_reference_number,
            work_status_ref,
            works_location_coordinates,
            works_location_type,
            year,
            month,
            event_type
        FROM permit_2022
        WHERE work_status_ref = 'completed' 
        AND collaborative_working = 'Yes'
        AND event_type = 'work_stop_event'
        """
        result = self.quack.execute(query)
        return result.fetchdf()

    def collab_split(self):
        """
        Fetch records for all completed collaborative works between 2022 and 2023.
        """
        query = """
        SELECT collaborative_working, month, year, COUNT(*) AS count
        FROM permit_2023_final 
        WHERE work_status_ref = 'completed'
        GROUP BY collaborative_working, month, year;
        """
        result = self.quack.execute(query)
        return result.fetchdf()


@st.cache_data(show_spinner=True)
def get_cached_completed_works(_data_manager):
    return _data_manager.get_all_completed_works()


@st.cache_data(show_spinner=True)
def get_collab_split(_data_manager):
    return _data_manager.collab_split()
