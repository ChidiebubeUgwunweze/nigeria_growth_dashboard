import plotly.graph_objects as go # Go library for plotting figures such as the bar chart, line graphs e.t.c
import plotly.express as px # Plotly express library for plotting map like figures 
from data.filtering_logic import bar_logic, moving_average_logic, map_logic
from data.utils import human_format, state_centers
import json

#Loading the Nigerian map coordinates into nigera_geo
with open('data/ng.json') as f:
    nigeria_geo = json.load(f)

def bar_plot(selected_date, WINDOW_DAYS, plot_points):
    bar_dataframe, average, _, target_date, _, plot_points = bar_logic(selected_date, WINDOW_DAYS, plot_points)
    #----------------------------------------------------------------------------------------------------------------------------------------------
    # Plotting FIGURE 1: Bar Chart
    bar_fig = go.Figure() # Creating instance of a figure (bar chart)
    # Drawing the bar chart
    bar_fig.add_trace(go.Bar(x= bar_dataframe['Truckout date'], y= bar_dataframe['Quantity loaded'], marker_color= 'royalblue')) 
    # Adding the average line
    bar_fig.add_hline(y=average, line_dash= "solid", line_color="orange", annotation_text=f"{WINDOW_DAYS}-Day(s) Avg: {human_format(average)}", annotation_position = "top left")
    bar_fig.update_layout(title=f"{WINDOW_DAYS}-Day Trend leading to {target_date}", xaxis_title= "Days", yaxis_title="Quantity loaded")
    bar_fig.update_layout(
    paper_bgcolor='#0d1117',  # outer background
    plot_bgcolor='#0d1117',   # inner chart background
    font_color='white'
)
    return bar_fig

def moving_average_plot(selected_date, WINDOW_DAYS, plot_points):
    linechart_filtered = moving_average_logic(selected_date, WINDOW_DAYS, plot_points)
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
        margin=dict(l=20, r=20, t=40, b=20),
    )
    line_fig.update_layout(title=f"{plot_points}-Day Moving Average -- {linechart_filtered["Truckout date"].iloc[0]} to {linechart_filtered["Truckout date"].iloc[-1]}", xaxis_title= "Date", yaxis_title="Moving Averages")
    line_fig.update_xaxes(autorange=True)
    line_fig.update_yaxes(autorange=True)

    line_fig.update_layout(
    paper_bgcolor='#0d1117',  # outer background
    plot_bgcolor='#0d1117',   # inner chart background
    font_color='white'
)
    return line_fig
    


def map_plot(selected_date, WINDOW_DAYS, plot_points):
    state_info = map_logic(selected_date, WINDOW_DAYS, plot_points)
    #----------------------------------------------------------------------------------------------------------------------------------------------
    # Plotting FIGURE 2: Nigerian Map
    limit = state_info['Percentage Growth %'].abs().max()

    map_fig = px.choropleth(
    state_info,
    geojson=nigeria_geo,
    title=f'Growth Rate per State - Average of {WINDOW_DAYS} days before {selected_date} vs {selected_date}',
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
    
    map_fig.update_layout(
    paper_bgcolor='#0d1117',  # outer background
    plot_bgcolor='#0d1117',   # inner chart background
    font_color='white')

    map_fig.update_layout(
    paper_bgcolor='#0d1117',
    geo=dict(bgcolor='#0d1117'),
    font_color='white'
)

    return map_fig