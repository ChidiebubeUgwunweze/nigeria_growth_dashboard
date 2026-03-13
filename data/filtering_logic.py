
import pandas as pd
def data():
    df = pd.read_parquet("data/data.parquet") # Reading 'data.parquet' as DataFrame
    df["Truckout date"] = df["Truckout date"].dt.date # Removing data timestamp Truckout date
    return df
    

def bar_logic(selected_date, WINDOW_DAYS, plot_points):
    #STEP 1: Create current date and the starting date
    target_date = pd.to_datetime(selected_date).date()  # Current date
    start_date = target_date - pd.Timedelta(days=WINDOW_DAYS)    # Starting date
    #---------------------------------------------------------------------------------------------------------------------------------------------------
    #BAR CHART LOGIC
    # Filtering Logic for Bar Chart and Line Chart
    mask_30d = (data()['Truckout date'] > start_date) & (data()['Truckout date'] <= target_date)
    window_df = data()[mask_30d]

    #Creating Dataframe for plotting bar chart
    bar_dataframe = pd.DataFrame(window_df.groupby("Truckout date")["Quantity loaded"].sum()).reset_index()
    
    # Average for WINDOW_DAYS days for bar plot average line
    average = window_df["Quantity loaded"].sum() / WINDOW_DAYS
    return bar_dataframe, average, start_date, target_date, WINDOW_DAYS, plot_points

def moving_average_logic(selected_date, WINDOW_DAYS, plot_points):
    #------------------------------------------------------------------------------------------------------------------------------------------
    #LINE CHART (MOVING AVERAGE) LOGIC
    bar_dataframe, _, _, _, _, plot_points = bar_logic(selected_date, WINDOW_DAYS, plot_points)
    end_date = bar_dataframe['Truckout date'].max()
    begin_date = end_date - pd.Timedelta(days=plot_points-1)
    
    line_chart_data = data().groupby("Truckout date")["Quantity loaded"].sum().reset_index()

    line_chart_data["Moving average"] = (
    line_chart_data["Quantity loaded"]
    .rolling(window=WINDOW_DAYS, min_periods=1)
    .mean()
    )

    linechart_filtered = line_chart_data[
    (line_chart_data['Truckout date'] >= begin_date) &
    (line_chart_data['Truckout date'] <= end_date)
      ]
    return linechart_filtered

def map_logic(selected_date, WINDOW_DAYS, plot_points):
    #-----------------------------------------------------------------------------------------------------------------------------------------------
    #MAP LOGIC
    #Data filter for map
    _, _, start_date, target_date, _, _ = bar_logic(selected_date, WINDOW_DAYS, plot_points)
    mask_map = (data()['Truckout date'] >= start_date) & (data()['Truckout date'] < target_date)
    data_map = data()[mask_map]
    # Creating the ultimate DataFrame for the Nigerian Map
    state_info_1 = pd.DataFrame({
    "Truckout date": data_map["Truckout date"],
    "Destination state": data_map["Destination state"], 
    "Quantity loaded": data_map["Quantity loaded"]
    })

    state_info = pd.DataFrame(state_info_1.groupby(["Truckout date","Destination state"])["Quantity loaded"].sum()).reset_index()
    state_info = pd.DataFrame(state_info.groupby("Destination state")["Quantity loaded"].sum()).reset_index()
    state_info["Average"] = state_info["Quantity loaded"] / WINDOW_DAYS

    today_data = data()[(data()['Truckout date'] == target_date)] # Filtering for only today's data
    today_map = pd.DataFrame(today_data.groupby(["Truckout date","Destination state"])["Quantity loaded"].sum()).reset_index() #Today data per state
    state_info["Percentage Growth %"] = ((today_map["Quantity loaded"] - state_info["Average"]) / state_info["Average"]) * 100
    
    return state_info