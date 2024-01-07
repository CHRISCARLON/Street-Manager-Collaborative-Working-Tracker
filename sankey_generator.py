import plotly.graph_objects as go


def prepare_completed_sankey_data(df_completed_works, selected_highway_authorities, selected_months, selected_years,
                                  selected_activity_types, selected_work_categories,
                                  figure_height=1500, figure_width=1500):

    """
    Create an interactive sankey diagram using the returned completed collaboration df.
    """

    # Apply additional filters
    df_filtered = df_completed_works[
        (df_completed_works['highway_authority'].isin(selected_highway_authorities)) &
        (df_completed_works['month'].isin(selected_months)) &
        (df_completed_works['year'].isin(selected_years)) &
        (df_completed_works['activity_type'].isin(selected_activity_types)) &
        (df_completed_works['work_category'].isin(selected_work_categories))
    ]

    # Create labels for nodes
    df_filtered['promoter_label'] = df_filtered['promoter_organisation'] + ' (Works Promoter)'
    df_filtered['authority_label'] = df_filtered['highway_authority'] + ' (Highway Authority)'

    # Aggregate and count the occurrences
    df_grouped = df_filtered.groupby(['promoter_label', 'authority_label']).size().reset_index(name='completed_works')

    # Nodes
    promoters = set(df_grouped['promoter_label'])
    authorities = set(df_grouped['authority_label'])
    nodes = list(promoters | authorities)
    node_dict = {node: i for i, node in enumerate(nodes)}
    node_colors = ['blue' if '(Works Promoter)' in node else 'green' for node in nodes]

    # Links
    links = [{
        'source': node_dict[link['promoter_label']],
        'target': node_dict[link['authority_label']],
        'value': link['completed_works']
    } for link in df_grouped.to_dict('records')]

    # Creating the Sankey diagram
    fig = go.Figure(data=[go.Sankey(node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=nodes, color=node_colors), link=dict(source=[link['source'] for link in links], target=[link['target'] for link in links], value=[link['value'] for link in links]))])
    fig.update_layout(font_size=12, height=figure_height, width=figure_width)
    return fig
