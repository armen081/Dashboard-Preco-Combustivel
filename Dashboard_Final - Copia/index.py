from dash import html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


from app import *
from dash_bootstrap_templates import ThemeSwitchAIO


template_theme1 = "solar"
template_theme2 = "flatly"
url_theme1 = dbc.themes.SOLAR
url_theme2 = dbc.themes.FLATLY


df = pd.read_csv('data_clean.csv')
state_options = [{"label": x, "value": x} for x in df.ESTADO.unique()]
region_options = [{"label": x, "value": x} for x in df.REGIÃO.unique()]


app.layout = dbc.Container(children=[
    
    dbc.Row([
        
        dbc.Col([       
            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
            html.H3('Preço x Estado'),
            dcc.Dropdown(
                id="estados",
                value=[state['label'] for state in state_options[:3]],
                multi=True,
                options=state_options),
            dcc.Graph(id='animation_graph')
        ], sm=12, md=8 ),
        
        dbc.Col([
            
            html.H3('Preço x Estado'),
            dcc.Dropdown(
                id="estados2",
                value=[state['label'] for state in state_options[:3]],
                multi=True,
                options=state_options),
            dcc.Graph(id='teste2')], sm=12, md= 4, style={'margin-top':'28px'}),
    ]),
    
    dbc.Row([
        
        dbc.Col([                                   
            dcc.Dropdown(
                id="estado1",
                value=state_options[1]['label'],
                options=state_options),
        ], sm=8, md=4),
       
        dbc.Col([
            dcc.Dropdown(
                id="estado2",
                value=state_options[3]['label'],
                options=state_options),
        ], sm=8, md=4),
    ]),
    
    dbc.Row([          
       
        dbc.Col([
            dcc.Graph(id='indicator1'),
        ], sm=8, md =4),
      
        dbc.Col([
            dcc.Graph(id='indicator2')
        ], sm=8, md=4),
        
        dbc.Col([
            dcc.Dropdown(
                id="regioes",
                value=[region['label'] for region in region_options[:3]],
                multi=True,
                options=region_options),
            dcc.Graph(id='teste')], sm=4, md= 4)
    ])
], fluid = True)



@app.callback(
    Output('animation_graph', 'figure'),
    Input('estados', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def animation(estados, toggle):
    template = template_theme1 if toggle else template_theme2
    
    df_data = df.copy(deep=True)
    mask = df_data['ESTADO'].isin(estados)
    fig = px.line(df_data[mask], x='DATA', y='VALOR REVENDA (R$/L)', 
                  color='ESTADO', template=template)

    return fig


@app.callback(
    Output('teste2','figure'),
    Input('estados2', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

def graph_bar(estados2, toggle):
    template = template_theme1 if toggle else template_theme2
    df_data = df.copy(deep=True)
    mask = df_data['ESTADO'].isin(estados2)
    fig = px.bar(df_data[mask], x='ANO', y='VALOR REVENDA (R$/L)', 
                  color='ESTADO', template=template)

    return fig
    


@app.callback(
    Output("indicator1", "figure"),
    Output("indicator2", "figure"),
    Input('estado1', 'value'),
    Input('estado2', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def card1(estado1, estado2, toggle):
    template = template_theme1 if toggle else template_theme2

    df_data = df.copy(deep=True)
    data_estado1 = df_data[df_data.ESTADO.isin([estado1])]
    data_estado2 = df_data[df_data.ESTADO.isin([estado2])]

    initial_date = str(int(df_data['ANO'].min()) - 1)
    final_date = df_data['ANO'].max()
    
    iterable = [(estado1, data_estado1), (estado2, data_estado2)]
    indicators = []

    for estado, data in iterable:
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = "number+delta",
            title = {"text": f"<span>{estado}</span><br><span style='font-size:0.7em'>{initial_date} - {final_date}</span>"},
            value = data.at[data.index[-1],'VALOR REVENDA (R$/L)'],
            number = {'prefix': "R$", 'valueformat': '.2f'},
            delta = {'relative': True, 'valueformat': '.1%', 'reference': data.at[data.index[0],'VALOR REVENDA (R$/L)']}
        ))
        fig.update_layout(template=template)
        indicators.append(fig)
    
    return indicators

@app.callback(
    Output('teste','figure'),
    Input('regioes', 'value'),
    
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

def graph_bar(regioes, toggle):
    template = template_theme1 if toggle else template_theme2
    df_data = df.copy(deep=True)
    year_region = df_data['REGIÃO'].isin(regioes)
    fig = px.bar(df_data[year_region], x='VALOR REVENDA (R$/L)', y='ANO', orientation='h',
                   color="REGIÃO",template=template)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
