import pandas as pd
import datetime


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