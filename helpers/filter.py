import pandas as pd
import datetime
import plotly.graph_objects as go
import streamlit as st



def trimming_filter(df, data_column, time_interval, num_points_to_fix):

    #copies the inital dataframe
    smoothed_df = df.copy()
    #array to store the filtered data
    smoothed_data = []

    for i in range(len(df)):
        #time interval used for the sliding window 
        start_time = df['20t_Date'][i] - pd.Timedelta(minutes=time_interval/2)
        end_time = df['20t_Date'][i] + pd.Timedelta(minutes=time_interval/2)
        window = df[(df['20t_Date'] >= start_time) & (df['20t_Date'] <= end_time)][data_column]

        #sort the values included in the window 
        sorted_window = sorted(window)
        #doesn't take the incorrect values into account
        positive_values = list(filter(lambda x: x >= 0, sorted_window))
        min_values = positive_values[:num_points_to_fix]
        max_values = positive_values[-num_points_to_fix:]
        
        #calculation of the filtered dataframe
        if df[data_column][i] in min_values and min_values and df[data_column][i] > 0:
            min_values_sorted = sorted(min_values)
            smoothed_value = min_values_sorted[1] if len(min_values_sorted) > 1 else min_values_sorted[0]
        elif df[data_column][i] in max_values and max_values and df[data_column][i] > 0:
            max_values_sorted = sorted(max_values)
            smoothed_value = max_values_sorted[-2] if len(max_values_sorted) > 1 else max_values_sorted[-1]
        else:
            smoothed_value = df[data_column][i]

        smoothed_data.append(smoothed_value)

    smoothed_df[data_column] = smoothed_data

    return smoothed_df



def invalid_datapoints_minmax(x, y, min, max):
    # Define the interval and the color for points outside the interval
    interval_min = min
    interval_max = max
    outside_color = "red"

    # Create a list to store the colors of each data point
    colors = []

    # Iterate over the data points and assign colors based on the interval
    for xi, yi in zip(x, y):
        if yi < interval_min or yi > interval_max:
            colors.append(outside_color)
        else:
            colors.append("blue")  # Default color for points inside the interval

    # Create the line chart
    fig = go.Figure(
        data=go.Scatter(x=x, y=y, mode="lines+markers", marker=dict(color=colors))
    )

    fig.add_trace(
        go.Scatter(
            x=[None], y=[None], mode="markers", marker=dict(color="blue"), name="Valide"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(color="red"),
            name="Non-valide",
        )
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def invalid_datapoints_min(x, y, min):
    # Define the interval and the color for points outside the interval
    interval_min = min
    outside_color = "red"

    # Create a list to store the colors of each data point
    colors = []

    # Iterate over the data points and assign colors based on the interval
    for xi, yi in zip(x, y):
        if yi < interval_min:
            colors.append(outside_color)
        else:
            colors.append("blue")  # Default color for points inside the interval

    # Create the line chart
    fig = go.Figure(
        data=go.Scatter(x=x, y=y, mode="lines+markers", marker=dict(color=colors))
    )

    fig.add_trace(
        go.Scatter(
            x=[None], y=[None], mode="markers", marker=dict(color="blue"), name="Valide"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(color="red"),
            name="Non-valide",
        )
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def invalid_datapoints_max(x, y, max):
    # Define the interval and the color for points outside the interval
    interval_max = max
    outside_color = "red"

    # Create a list to store the colors of each data point
    colors = []

    # Iterate over the data points and assign colors based on the interval
    for xi, yi in zip(x, y):
        if yi > interval_max:
            colors.append(outside_color)
        else:
            colors.append("blue")  # Default color for points inside the interval

    # Create the line chart
    fig = go.Figure(
        data=go.Scatter(x=x, y=y, mode="lines+markers", marker=dict(color=colors))
    )

    fig.add_trace(
        go.Scatter(
            x=[None], y=[None], mode="markers", marker=dict(color="blue"), name="Valide"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            marker=dict(color="red"),
            name="Non-valide",
        )
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
