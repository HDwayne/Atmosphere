import pandas as pd
import datetime
import plotly.graph_objects as go
import streamlit as st



def trimming_filter(df, time_column, data_columns, time_interval):
    
    smoothed_df = df.copy()

    for column in data_columns:
        smoothed_data = []

        for i in range(len(df)):
            start_time = df[time_column][i] - pd.Timedelta(minutes=time_interval/2)
            end_time = df[time_column][i] + pd.Timedelta(minutes=time_interval/2)

            window = df[(df[time_column] >= start_time) & (df[time_column] <= end_time)][column]

            min_value = min(window)
            max_value = max(window)

            if df[column][i] == min_value:
                smoothed_value = df[(df[time_column] >= start_time) & (df[time_column] <= end_time)][column].iloc[
                    df[(df[time_column] >= start_time) & (df[time_column] <= end_time)][column].values.argmin()]
            elif df[column][i] == max_value:
                smoothed_value = df[(df[time_column] >= start_time) & (df[time_column] <= end_time)][column].iloc[
                    df[(df[time_column] >= start_time) & (df[time_column] <= end_time)][column].values.argmax()]
            else:
                smoothed_value = df[column][i]

            smoothed_data.append(smoothed_value)

        smoothed_df[column] = smoothed_data

    return smoothed_df
            i_deb = jj
            is_calcul = False
            stat.clear()
    return filtered_df


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
