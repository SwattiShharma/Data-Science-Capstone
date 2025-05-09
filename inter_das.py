from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
# Initialize Dash app
app = Dash(__name__)

# Load dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get unique launch sites
launch_sites = spacex_df['Launch Site'].unique()

# Task 1: Add Dropdown
dropdown = dcc.Dropdown(
    id='site-dropdown',
    options=[{'label': 'All Sites', 'value': 'ALL'}] +
            [{'label': site, 'value': site} for site in launch_sites],
    value='ALL',
    placeholder='Select a Launch Site here',
    searchable=True
)

# Define app layout
app.layout = html.Div([
    html.H1("SpaceX Launch Dashboard"),
    dropdown
])
dcc.Graph(id='success-pie-chart')
app.layout = html.Div([
    html.H1("SpaceX Launch Dashboard"),
    dropdown,
    dcc.Graph(id='success-pie-chart')
])
@app.callback(Output('success-pie-chart', 'figure'),
              Input('site-dropdown', 'value'))
def get_pie_chart(selected_site):
    if selected_site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
        return fig
    else:
        # Filter data for selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        # Count success/failure
        site_counts = filtered_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']
        site_counts['class'] = site_counts['class'].replace({1: 'Success', 0: 'Failure'})

        fig = px.pie(
            site_counts,
            names='class',
            values='count',
            title=f'Success vs Failure for {selected_site}'
        )
        return fig
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()
dcc.RangeSlider(
    id='payload-slider',
    min=0,
    max=10000,
    step=1000,
    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
    value=[min_payload, max_payload]
)
app.layout = html.Div([
    html.H1("SpaceX Launch Dashboard"),
    dropdown,
    dcc.Graph(id='success-pie-chart'),
    html.Hr(),
    html.P("Select Payload Range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),
    dcc.Graph(id='success-payload-scatter-chart')
])
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter(selected_site, selected_payload):
    low, high = selected_payload
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload vs. Launch Success'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run(port=8050)
