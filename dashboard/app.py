import dash
from dash import Input, Output, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])

MMteam_stats_df = pd.read_csv(r"C:\Users\Suhana\Spring23\ballinsights\tourney_stats_team.csv")


app.layout = html.Div(children=[
    html.H1(children="ballIn'sights"),

    html.H5(children="A dashboard to deliver comprehensive insights in aid predictions for the NCAA Men's Basketball March Madness."),

    html.Hr(),

    html.H6("Choose two teams to compare!"),
    html.Div([
        "Team 1: ",
        dcc.Input(id='team1-input', value='Team 1', type='text', className="dash-materia", style={"margin-right": "15px"}),
        "Team 2: ",
        dcc.Input(id='team2-input', value='Team2', type='text', className="dash-materia")
    ]),

])


@app.callback(
    Output('shotchartout', 'image'),
    Input('team1-input', 'team2-input')
)
def get_shotcharts(team1, team2):
    x = create_plot(team1, team2)
    x = np.reshape(x, (1024, 720))
    data = im.fromarray(x)
    return data



if __name__ == '__main__':
    app.run_server(debug=True)
