from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.graph_objects as go

# Carica il dataset
df = pd.read_csv('data/stads_data_parsed_cleaned_pop_gdp_v1.csv')

# Crea un'app Dash
app = Dash(__name__)

# Stili CSS
app.css.append_css({
    'external_url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'
})

# Crea il layout dell'app
app.layout = html.Div([
    html.Div([
        html.H1("Energy Data Visualization", className="text-center mb-4"),
    ], className="row"),

    html.Div([
        html.Div([
            html.Label("Select a State:", className="font-weight-bold"),
            dcc.Dropdown(
                id="state-dropdown",
                options=[{'label': state, 'value': state} for state in df['StateCode'].unique()],
                value=df['StateCode'].unique()[0],
                multi=False  # Consentiamo una sola selezione
            ),
        ], className="col-md-3"),

        html.Div([
            html.Label("Select Category:", className="font-weight-bold"),
            dcc.Dropdown(
                id="category-dropdown",
                options=[
                    {'label': 'TETCB', 'value': 'TETCB'},
                    {'label': 'TEPRB', 'value': 'TEPRB'}
                ],
                value='TETCB',
                multi=False
            ),
        ], className="col-md-3"),
    ], className="row"),

    html.Div([
        html.Label("Select Variables of Interest:", className="font-weight-bold"),
        dcc.Checklist(
            id="variable-checklist",
            options=[],
            value=[],
            inline=False  # Visualizza l'elenco puntato in verticale
        ),
    ], className="row", id="variable-checklist-container"),

    html.Div([
        dcc.Graph(id="energy-chart")
    ], className="container mt-4")
])

# Funzione di callback per aggiornare le opzioni del checklist delle variabili in base alla categoria selezionata
@app.callback(
    Output("variable-checklist", "options"),
    Input("category-dropdown", "value")
)
def update_variable_options(selected_category):
    if selected_category == 'TETCB':
        variable_options = [
            {'label': 'CLTCB', 'value': 'CLTCB'},
            {'label': 'NNTCB', 'value': 'NNTCB'},
            {'label': 'PMTCB', 'value': 'PMTCB'},
            {'label': 'FFTCB', 'value': 'FFTCB'},
            {'label': 'NUETB', 'value': 'NUETB'},
            {'label': 'RETCB', 'value': 'RETCB'},
            {'label': 'ELISB', 'value': 'ELISB'},
            {'label': 'ELNIB', 'value': 'ELNIB'}
        ]
    else:
        variable_options = [
            {'label': 'CLPRB', 'value': 'CLPRB'},
            {'label': 'NGMPB', 'value': 'NGMPB'},
            {'label': 'PAPRB', 'value': 'PAPRB'},
            {'label': 'NUEGB', 'value': 'NUEGB'},
            {'label': 'BFPRB', 'value': 'BFPRB'},
            {'label': 'WWPRB', 'value': 'WWPRB'},
            {'label': 'NCPRB', 'value': 'NCPRB'},
            {'label': 'REPRB', 'value': 'REPRB'}
        ]

    return variable_options

# Funzione di callback per aggiornare il grafico in base alle selezioni
@app.callback(
    Output("energy-chart", "figure"),
    Input("state-dropdown", "value"),
    Input("variable-checklist", "value")
)
def update_energy_chart(selected_state, selected_variables):
    # Filtra il DataFrame in base allo stato e alle variabili selezionate
    filtered_df = df[(df['StateCode'] == selected_state) & (df['MSN'].isin(selected_variables))]

    # Crea un grafico a area sovrapposto per le variabili selezionate
    fig = go.Figure()

    for msn in filtered_df['MSN'].unique():
        msn_data = filtered_df[filtered_df['MSN'] == msn]
        fig.add_trace(go.Scatter(
            x=msn_data['Year'],
            y=msn_data['Data'],
            fill='tonexty',
            mode='none',
            name=msn
        ))

    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Data',
        title=f'Energy Data Over Time in {selected_state}'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)