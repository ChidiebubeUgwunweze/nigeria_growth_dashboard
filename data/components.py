from .utils import human_format
from dash import html, dcc
from data.filtering_logic import data
# Function for creating number pickers
def number_picker(index: int, header: str) -> html.Div:
  return html.Div([

        html.Label(f"{header}", style={'margin-right': '15px', 'font-weight': 'bold', 'color': 'white'}),
        
        # The Stepper Container
        html.Div([
            html.Button(
                        "-",
                        id={"type": "minus", "index": index},
                        n_clicks=0,
                        style={
                            'width': '40px',
                            'height': '40px',
                            'color': '#ff1744',
                            'backgroundColor': '#1a1a2e',
                            'border': '2px solid #ff1744',
                            'borderRadius': '8px',
                            'fontSize': '20px',
                            'fontWeight': 'bold',
                            'cursor': 'pointer',
                            'lineHeight': '1',
                            'transition': 'all 0.2s ease'
                        }
                    ),
            
            dcc.Input(
                id={"type": "input", "index": index},
                type="number",
                value=7,
                style={
                    'width': '60px',
                    'height': '40px',
                    'textAlign': 'center',
                    'backgroundColor': '#1a1a2e',
                    'color': 'white',
                    'border': '2px solid #00d4ff',
                    'borderRadius': '8px',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'margin': '0 5px'
                }
            ),
                
       html.Button(
            "+",
            id={"type": "plus", "index": index},
            n_clicks=0,
            style={
                'width': '40px',
                'height': '40px',
                'color': '#00c853',
                'backgroundColor': '#1a1a2e',
                'border': '2px solid #00c853',
                'borderRadius': '8px',
                'fontSize': '20px',
                'fontWeight': 'bold',
                'cursor': 'pointer',
                'lineHeight': '1',
                'transition': 'all 0.2s ease'
            }
        )],style={'display': 'flex', 'align-items': 'center'}),
        
        # html.Hr(),
        
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'width': '180px', 'border-radius': '8px'})





def header() -> html.H1:
    return html.H1("Nigerian Downstream Quantity Loaded Dashboard (January 2026 focused)", style={'textAlign': 'center', 'color': 'white'})   # Heading and title of the page

def selectors() -> html.Div:
    return html.Div(
        [
            number_picker(1, "Window Days"),
            number_picker(2, "Data Points (Line Graph)"),
        ],
        style={
            "display": "flex",
            "gap": "30px",            # spacing between them
            "alignItems": "flex-start",
            "justifyContent": "center"
        }
    )
agg_date = data().groupby("Truckout date")["Quantity loaded"].sum().to_frame().reset_index()
def kpi_cards() -> html.Div:
            return html.Div(
                        children=[
                            # Total Loaded
                            html.Div(
                                children=[
                                    html.P('Total Quantity Loaded', style={
                                        'color': '#00d4ff',
                                        'fontSize': '14px',
                                        'margin': '0',
                                        'textTransform': 'uppercase',
                                        'letterSpacing': '1px'
                                    }),
                                    html.H2(f'{human_format(data()["Quantity loaded"].sum())}', style={
                                        'color': 'white',
                                        'fontSize': '28px',
                                        'margin': '8px 0 0 0',
                                        'fontWeight': 'bold'
                                    })
                                ],
                                style={
                                    'backgroundColor': '#1a1a2e',
                                    'border': '1px solid #00d4ff',
                                    'borderRadius': '12px',
                                    'padding': '20px',
                                    'flex': '1',
                                    'textAlign': 'center'
                                }
                            ),
                            # Daily Average
                            html.Div(
                                children=[
                                    html.P('Daily Average', style={
                                        'color': '#00d4ff',
                                        'fontSize': '14px',
                                        'margin': '0',
                                        'textTransform': 'uppercase',
                                        'letterSpacing': '1px'
                                    }),
                                    html.H2(f'{human_format(agg_date["Quantity loaded"].mean())}', style={
                                        'color': 'white',
                                        'fontSize': '28px',
                                        'margin': '8px 0 0 0',
                                        'fontWeight': 'bold'
                                    })
                                ],
                                style={
                                    'backgroundColor': '#1a1a2e',
                                    'border': '1px solid #00d4ff',
                                    'borderRadius': '12px',
                                    'padding': '20px',
                                    'flex': '1',
                                    'textAlign': 'center'
                                }
                            ),
                            # Peak Day
                            html.Div(
                                children=[
                                    html.P('Peak Day', style={
                                        'color': '#00d4ff',
                                        'fontSize': '14px',
                                        'margin': '0',
                                        'textTransform': 'uppercase',
                                        'letterSpacing': '1px'
                                    }),
                                    html.H2(f'{agg_date.loc[agg_date["Quantity loaded"] == agg_date["Quantity loaded"].max(), "Truckout date"].item()}', style={
                                        'color': 'white',
                                        'fontSize': '28px',
                                        'margin': '8px 0 0 0',
                                        'fontWeight': 'bold'
                                    })
                                ],
                                style={
                                    'backgroundColor': '#1a1a2e',
                                    'border': '1px solid #00d4ff',
                                    'borderRadius': '12px',
                                    'padding': '20px',
                                    'flex': '1',
                                    'textAlign': 'center'
                                }
                            ),
                        ],
                        style={
                            'display': 'flex',
                            'gap': '20px',
                            'margin': '20px 0',
                            'padding': '0 20px'
                        }
                    )

def date_selector() -> html.Div:
   return html.Div(
    children=[
        html.Label('Select Analysis Date:', style={'color': 'white', 'font-weight': 'bold', 'fontSize': '24px'}),
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=data()['Truckout date'].min(),
            max_date_allowed=data()['Truckout date'].max(),
            date=data()['Truckout date'].max(),
            display_format='DD MMM YYYY',
            className='dark-date-picker'
        )
    ],
    style={'backgroundColor': '#0d1117'}
)

def figures() -> html.Div:
   return html.Div([
        # The Bar Chart
        dcc.Graph(id='bar-chart', style={'width': '100%', 'height': '120vh', 'marginBottom':'80px', 'backgroundColor': '#16213e', 'borderRadius': '10px', 'padding': '15px', 'marginBottom': '20px'}),
        #The Moving Average Line Chart
        dcc.Graph(id='line-chart', style={'width': '100%', 'height': '120vh', 'marginBottom':'80px', 'backgroundColor': '#16213e', 'borderRadius': '10px', 'padding': '15px', 'marginBottom': '20px'}),
        # The Nigerian Map
        dcc.Graph(id='nigerian-map', style={'width': '100%', 'height': '150vh', 'backgroundColor': '#16213e', 'borderRadius': '10px', 'padding': '15px', 'marginBottom': '20px'})
        ],style={'padding':'30px'})