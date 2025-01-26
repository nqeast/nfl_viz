import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Load and clean the data
data = pd.read_csv("team_passing_yards_2016_2024.csv")
data = data.dropna(subset=['posteam'])  # Remove rows with NaN in the posteam column
data['rank'] = data.groupby('year')['total_passing_yards'].rank(ascending=False)  # Calculate rank

# Get unique team names
teams = sorted(data['posteam'].unique())

# Initialize the Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("NFL Team Rank Progression (2016-2024)", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Select Team 1:"),
        dcc.Dropdown(
            id='team1-dropdown',
            options=[{'label': team, 'value': team} for team in teams],
            value='KC',  # Default value
            clearable=False
        ),
        html.Label("Select Team 2:"),
        dcc.Dropdown(
            id='team2-dropdown',
            options=[{'label': team, 'value': team} for team in teams],
            value='BUF',  # Default value
            clearable=False
        )
    ], style={'width': '50%', 'margin': 'auto'}),
    
    dcc.Graph(id='rank-graph', style={'height': '700px'})
])

# Callback to update the graph
@app.callback(
    Output('rank-graph', 'figure'),
    [Input('team1-dropdown', 'value'),
     Input('team2-dropdown', 'value')]
)
def update_graph(team1, team2):
    # Filter data for selected teams
    team1_data = data[data['posteam'] == team1]
    team2_data = data[data['posteam'] == team2]
    
    # Ensure y-axis always covers the full rank range (1 to 32)
    y_axis_range = [32.5, 0.5]  # Adjusted to ensure "1" and "32" are fully visible

    # Create frames for animation
    frames = []
    for i in range(1, len(team1_data) + 1):
        frame = go.Frame(
            data=[
                go.Scatter(
                    x=team1_data['year'][:i],
                    y=team1_data['rank'][:i],
                    mode='lines+markers',
                    line=dict(width=3, color="blue"),
                    marker=dict(size=10, color="blue"),
                    name=team1,
                    hovertemplate="Year: %{x}<br>Rank: %{y}<extra></extra>"
                ),
                go.Scatter(
                    x=team2_data['year'][:i],
                    y=team2_data['rank'][:i],
                    mode='lines+markers',
                    line=dict(width=3, color="red"),
                    marker=dict(size=10, color="red"),
                    name=team2,
                    hovertemplate="Year: %{x}<br>Rank: %{y}<extra></extra>"
                )
            ],
            name=f"Frame {i}"
        )
        frames.append(frame)

    # Create the initial figure
    fig = go.Figure(
        data=[
            go.Scatter(
                x=team1_data['year'][:1],
                y=team1_data['rank'][:1],
                mode='lines+markers',
                line=dict(width=3, color="blue"),
                marker=dict(size=10, color="blue"),
                name=team1,
                hovertemplate="Year: %{x}<br>Rank: %{y}<extra></extra>"
            ),
            go.Scatter(
                x=team2_data['year'][:1],
                y=team2_data['rank'][:1],
                mode='lines+markers',
                line=dict(width=3, color="red"),
                marker=dict(size=10, color="red"),
                name=team2,
                hovertemplate="Year: %{x}<br>Rank: %{y}<extra></extra>"
            )
        ],
        layout=go.Layout(
            title=f"Rank Progression for {team1} and {team2} (2016-2024)",
            xaxis=dict(
                title="Year",
                range=[2015.5, 2024.5],  # Add padding to fully display 2016 and 2024
                fixedrange=True,  # Disable zooming
                showgrid=False,  # Remove gridlines
                tickmode='linear',  # Ensure ticks are evenly spaced
                dtick=1  # One tick per year
            ),
            yaxis=dict(
                title="Rank",
                range=y_axis_range,  # Adjust range to make 1 and 32 fully visible
                tickvals=list(range(1, 33)),  # Explicitly show all ranks, including 1 and 32
                fixedrange=True,  # Disable zooming
                showgrid=False  # Remove gridlines
            ),
            legend=dict(
                title="Teams",
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=60, r=60, t=120, b=60),  # Adjusted margins for better visibility
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                            "label": "Play",
                            "method": "animate"
                        },
                        {
                            "args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                            "label": "Pause",
                            "method": "animate"
                        }
                    ],
                    "direction": "left",
                    "pad": {"r": 10, "t": 87},
                    "showactive": False,
                    "type": "buttons",
                    "x": 0.1,
                    "xanchor": "right",
                    "y": 0,
                    "yanchor": "top"
                }
            ]
        ),
        frames=frames
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)