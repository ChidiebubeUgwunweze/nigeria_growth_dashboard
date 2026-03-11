import dash
from dash import html, dcc, Input, Output, State, ALL, callback
from data.utils import state_centers, number_picker, update_value, human_format
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

#Loading the Nigerian map coordinates into nigera_geo
with open('data/ng.json') as f:
    nigeria_geo = json.load(f)

df = pd.read_parquet("data/data.parquet") # Reading 'data.parquet' as DataFrame
df["Truckout date"] = df["Truckout date"].dt.date # Removing data timestamp Truckout date

app = dash.Dash(__name__) ## Create instance of Dashboard app
# server = app.server

app.layout = html.Div([                     # app.layout is the entire Dash app
    # Header of app
    html.H1("Nigerian Downstream Chain Growth Monitor by Quantity loaded", style={'textAlign': 'center'}),   # Heading and title of the page 
    
   # Date Picker Div. html.Div is a demarcated section of the app.layout. In this html.Div we will have the date picker
    html.Div(
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
    ),

    html.Div([ html.Label('Select Analysis Date:'),   
               dcc.DatePickerSingle(id='date-picker',
                                   min_date_allowed = df['Truckout date'].min(), 
                                   max_date_allowed= df['Truckout date'].max(), 
                                   date= df['Truckout date'].max())],
                                   style = {'margin': '20px'}),
    # In this html.Div the sections for the bar chart and the nigerian map are created
    html.Div([
        # The Bar Chart
        dcc.Graph(id='bar-chart', style={'width': '100%', 'height': '120vh', 'marginBottom':'80px'}),
        #The Moving Average Line Chart
        dcc.Graph(id='line-chart', style={'width': '80%', 'height': '500px', 'marginBottom':'80px'}),
        # The Nigerian Map
        dcc.Graph(id='nigerian-map', style={'width': '100%', 'height': '150vh'})
        ],style={'padding':'30px'})
    
    ]) 

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
# ... the date selected and the bar chart and map figures so they are reflected on the app
@app.callback(
    Output('bar-chart','figure'), 
    Output('nigerian-map', 'figure'),
    Output('line-chart', 'figure'),
    Input('date-picker', 'date'),
    Input({"type":"input", "index":1}, 'value'),
    Input({"type":"input", "index":2}, "value")
)

def get_growth_metrics(selected_date, WINDOW_DAYS, plot_points): #selected_date (date selected), WINDOW_DAYS (Averaging days), plot_points i.e no. of plot points for line graph
    #STEP 1: Create current date and the starting date
    target_date = pd.to_datetime(selected_date).date()  # Current date
    start_date = target_date - pd.Timedelta(days=WINDOW_DAYS)    # Starting date
    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #BAR CHART LOGIC
    # Filtering Logic for Bar Chart and Line Chart
    mask_30d = (df['Truckout date'] > start_date) & (df['Truckout date'] <= target_date)
    window_df = df[mask_30d] 

    #Creating Dataframe for plotting bar chart
    bar_dataframe = pd.DataFrame(window_df.groupby("Truckout date")["Quantity loaded"].sum()).reset_index()
    

    # Average for 30 days for bar plot
    average = window_df["Quantity loaded"].sum() / WINDOW_DAYS

    #Today's info:
    today_data = df[(df['Truckout date'] == target_date)] # Filtering for only today's data
    today_value = today_data["Quantity loaded"].sum() # Total quantity loaded today
    #--------------------------------------------------------------------------------------------------------------------------------------------
    #LINE CHART (MOVING AVERAGE) LOGIC
    end_date = bar_dataframe['Truckout date'].max()
    begin_date = end_date - pd.Timedelta(days=plot_points)
    
    line_chart_data = df.groupby("Truckout date")["Quantity loaded"].sum().reset_index()

    line_chart_data["Moving average"] = (
    line_chart_data["Quantity loaded"]
    .rolling(window=WINDOW_DAYS, min_periods=1)
    .mean()
    )

    linechart_filtered = line_chart_data[
    (line_chart_data['Truckout date'] >= begin_date) &
    (line_chart_data['Truckout date'] <= end_date)
      ]
    
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    #MAP LOGIC
    #Data filter for map
    mask_map = (df['Truckout date'] >= start_date) & (df['Truckout date'] < target_date)
    data_map = df[mask_map]
    # Creating the ultimate DataFrame for the Nigerian Map
    state_info_1 = pd.DataFrame({
    "Truckout date": data_map["Truckout date"],
    "Destination state": data_map["Destination state"], 
    "Quantity loaded": data_map["Quantity loaded"]
    })
    
    state_info = pd.DataFrame(state_info_1.groupby(["Truckout date","Destination state"])["Quantity loaded"].sum()).reset_index()

    state_info = pd.DataFrame(state_info.groupby("Destination state")["Quantity loaded"].sum()).reset_index()

    state_info["Average"] = state_info["Quantity loaded"] / WINDOW_DAYS

    today_map = pd.DataFrame(today_data.groupby(["Truckout date","Destination state"])["Quantity loaded"].sum()).reset_index() #Today data per state
    state_info["Percentage Growth %"] = ((today_map["Quantity loaded"] - state_info["Average"]) / state_info["Average"]) * 100
    #----------------------------------------------------------------------------------------------------------------------------------------------
    # Plotting FIGURE 1: Bar Chart
    bar_fig = go.Figure() # Creating instance of a figure (bar chart)
    # Drawing the bar chart
    bar_fig.add_trace(go.Bar(x= bar_dataframe['Truckout date'], y= bar_dataframe['Quantity loaded'], marker_color= 'royalblue')) 
    # Adding the average line
    bar_fig.add_hline(y=average, line_dash= "solid", line_color="orange", annotation_text=f"{WINDOW_DAYS}-Day(s) Avg: {human_format(average)}", annotation_position = "top left")
    bar_fig.update_layout(title=f"{WINDOW_DAYS}-Day Trend leading to {target_date}", xaxis_title= "Days", yaxis_title="Quantiy loaded")
    #----------------------------------------------------------------------------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------------------------------------------------------------------------
    # Plotting FIGURE 2: Nigerian Map
    limit = state_info['Percentage Growth %'].abs().max()

    map_fig = px.choropleth(
    state_info,
    geojson=nigeria_geo,
    locations='Destination state',
    featureidkey="properties.name", 
    color='Percentage Growth %',
    color_continuous_scale=[
        [0, 'red'],          # The lowest negative value
        [0.5, 'lightgrey'],   # Zero (the midpoint)
        [1, 'green']],        # Ther highest positive value
    range_color = [-limit, limit]
    )

    # Name of State + percentage change to appear on the state
    state_info['text_label'] = state_info['Destination state'] + " " + state_info['Percentage Growth %'].round(1).astype(str) + "%"
    
    #Assigning the dictionary of longitudes and latitudes to STATE_CENTERS
    STATE_CENTERS = state_centers()
    #Getting Latitude and Longitude from STAT_CENTERS dictionary
    state_info['lat'] = state_info['Destination state'].map(lambda x: STATE_CENTERS.get(x, {}).get('lat'))
    state_info['lon'] = state_info['Destination state'].map(lambda x: STATE_CENTERS.get(x, {}).get('lon'))

    # Bolden text in text_label column
    state_info['text_label'] = "<b>" + state_info['text_label'].astype(str) + "</b>"

    # Add Name of State + Percentage on the intersection of the latitude and logitude of each state
    map_fig.add_scattergeo(lat=state_info['lat'], lon=state_info['lon'], text=state_info['text_label'], mode='text',
                            textfont={"color": "black", "size": 9, "family": "Arial"},
                            showlegend=False,
                            customdata=state_info[['Destination state','Percentage Growth %']],
                            hovertemplate="<b>State: </b> %{customdata[0]}<br>" +
                                          "<b>Percent:</b> %{customdata[1]:.1f}%<extra></extra>" )

    #Removing hover results of chloropleth
    map_fig.data[0].hoverinfo = "skip"
    map_fig.data[0].hovertemplate= None

    # Removing the rest of the WORLD
    map_fig.update_geos(
        visible=False,
        fitbounds="locations"
    )

    map_fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0},   # Cleaning up Margins
                            geo=dict(
                            projection_scale=1,       # This is the 'zoom' level
                            center={'lat': 9.082, 'lon': 8.675}, # Centers the map on Nigeria
                            visible=False,            # Removes the 'ocean' box/background
                            resolution=50,
                            scope='africa',           # Narrow the scope to Africa
                            lataxis_range=[4, 14],    # Tighten the 'camera' to Nigerian latitudes
                            lonaxis_range=[2, 15],),    # Tighten the 'camera' to Nigerian longitudes 
                            height=1000)
    #------------------------------------------------------------------------------------------------------------------------------------------------       
    # Plotting FIGURE 3: LineGraph (Moving average)
    line_fig = go.Figure()

    line_fig.add_trace(go.Scatter(
        x=linechart_filtered["Truckout date"],
        y=linechart_filtered["Moving average"],
        mode="lines",
        name="Quantity"
        ))
    
    line_fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    line_fig.update_layout(title=f"Moving average from {linechart_filtered["Truckout date"].iloc[0]} to {linechart_filtered["Truckout date"].iloc[-1]} with {WINDOW_DAYS} days window and {plot_points} data points", xaxis_title= "Date", yaxis_title="Moving Averages")
    line_fig.update_xaxes(autorange=True)
    line_fig.update_yaxes(autorange=True)

    return bar_fig, map_fig, line_fig
    
if __name__ == "__main__":
    app.run(debug=True) 