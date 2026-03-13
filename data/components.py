from dash import html, dcc
from data.filtering_logic import data
# Function for creating number pickers
def number_picker(index: int, header: str) -> html.Div:
  return html.Div([

        html.Label(f"{header}", style={'margin-right': '15px', 'font-weight': 'bold'}),
        
        # The Stepper Container
        html.Div([
            html.Button("-", id={"type": "minus","index": index}, n_clicks=0, style={'width': '40px', 'height': '40px'}),
            
            dcc.Input(
                id={"type": "input","index": index},
                type="number",
                value=7,  # Default value
                style={
                    'width': '60px', 
                    'height': '34px', 
                    'textAlign': 'center', 
                    'border': '1px solid #ccc',
                    'margin': '0 5px'}),
                
        html.Button("+", id={"type":"plus","index": index}, n_clicks=0, style={'width': '40px', 'height': '40px'})
        ],style={'display': 'flex', 'align-items': 'center'}),
        
        # html.Hr(),
        
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'width': '180px', 'border-radius': '8px'})





def header() -> html.H1:
    return html.H1("Nigerian Downstream Quantity Loaded Monitor ", style={'textAlign': 'center'})   # Heading and title of the page

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

def date_selector() -> html.Div:
   return html.Div([ html.Label('Select Analysis Date:'),   
               dcc.DatePickerSingle(id='date-picker',
                                   min_date_allowed = data()['Truckout date'].min(), 
                                   max_date_allowed= data()['Truckout date'].max(), 
                                   date= data()['Truckout date'].max())],
                                   style = {'margin': '20px'})

def figures() -> html.Div:
   return html.Div([
        # The Bar Chart
        dcc.Graph(id='bar-chart', style={'width': '100%', 'height': '120vh', 'marginBottom':'80px'}),
        #The Moving Average Line Chart
        dcc.Graph(id='line-chart', style={'width': '80%', 'height': '500px', 'marginBottom':'80px'}),
        # The Nigerian Map
        dcc.Graph(id='nigerian-map', style={'width': '100%', 'height': '150vh'})
        ],style={'padding':'30px'})