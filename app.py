import dash
from dash import html, dcc, Input, Output, State, ALL, callback
from data.plot import bar_plot, map_plot, moving_average_plot
from data.utils import update_value
from data.components import header, selectors, date_selector, figures, kpi_cards

app = dash.Dash(__name__) ## Create instance of Dashboard app
#for deployment
server = app.server #for deployment

# Over writing the default white background to make the whole dashboard background black
app.index_string = '''
<!DOCTYPE html>
<html>
<head>{%metas%}{%title%}{%favicon%}{%css%}</head>
<body style="margin:0; background-color:#0d1117;">
{%app_entry%}
{%config%}{%scripts%}{%renderer%}
</body>
</html>
'''

app.layout = html.Div(style={'backgroundColor': '#0d1117', 'padding': '20px'},children=[        # app.layout is the entire Dash app
   # Header of app
   header(),
   # Window Day selectors and Data Point selectors
   selectors(),
   # The target_date selector
   date_selector(),
   # KPI Cards
   kpi_cards(),
   # Bar Chart, Nigerian Map, Moving Averages
   figures()
 ]) 
# The nervous system of the app: @app.callback is responsible for the input and output of data within
@app.callback(
        Output({"type": "input","index": ALL}, "value"),
        Input({"type": "plus","index": ALL}, "n_clicks"),
        Input({"type": "minus","index": ALL}, "n_clicks"),
        State({"type": "input","index": ALL}, "value"),
        prevent_initial_call=True
)

def update_selector(plus_clicks, minus_clicks, current_values):
    return update_value(plus_clicks, minus_clicks, current_values)

# The nervous system of the app: @app.callback is responsible for the input and output of data within the app like
@app.callback(
    Output('bar-chart','figure'), 
    Output('nigerian-map', 'figure'),
    Output('line-chart', 'figure'),
    Input('date-picker', 'date'),
    Input({"type":"input", "index":1}, 'value'),
    Input({"type":"input", "index":2}, "value")
)

def get_growth_metrics(selected_date, WINDOW_DAYS, plot_points):
    return bar_plot(selected_date, WINDOW_DAYS, plot_points), map_plot(selected_date, WINDOW_DAYS, plot_points), moving_average_plot(selected_date, WINDOW_DAYS, plot_points)
    
if __name__ == "__main__":
    app.run(debug=True) 