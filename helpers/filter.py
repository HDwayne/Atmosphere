import pandas as pd
import datetime
import plotly.graph_objects as go
import streamlit as st


def filtre_ebarbeur(
    df: pd.DataFrame,
    type_donnees: str,
    val_manq: int,
    track_bar_coupure: int,
    track_bar_nbre_pts: int,
    track_bar_ebarbage: int,
) -> pd.DataFrame:
    """
    Applies a trimming filter to a dataframe.
    It basically replaces the lowest value with one that is slightly higher and the highest value with one that is slightly lower until the curve of the graph is smooth

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to filter
    type_donnees :
        Name of the column to filter
    val_manq : int
        An int representing invalid data (-999 for ex)
    track_bar_coupure : int
        The chosen time interval for the sliding window
    track_bar_nbre_pts : int
        The minimum number of points required within a sliding window to trigger the filtering process.
    track_bar_ebarbage : int
        The number of points that need to get fixed

    Returns
    -------
    pd.DataFrame
        The filtered dataframe (copy).
    """
    filtered_df = df.copy()
    nb_data = len(df)
    nb_pts = 0
    i_deb = 0
    is_calcul = False
    coupure = datetime.datetime.combine(
        datetime.date.today(), datetime.time.min
    ) + datetime.timedelta(minutes=track_bar_coupure)
    coupure = coupure - datetime.datetime.combine(
        datetime.date.today(), datetime.time.min
    )

    stat = []
    date = filtered_df.iloc[0]["20t_Date"]
    date_float = date.timestamp()

    for jj in range(1, nb_data):
        if filtered_df.iloc[jj][type_donnees] > val_manq:
            if (
                filtered_df.iloc[jj]["20t_Date"]
                - pd.Timestamp.fromtimestamp(date_float)
                < coupure
            ):
                stat.append(filtered_df.iloc[jj][type_donnees])
            else:
                is_calcul = True

            date = filtered_df.iloc[jj]["20t_Date"]

        if jj == nb_data - 1:
            is_calcul = True

        if is_calcul:
            stat.sort()
            nb_pts = min(track_bar_nbre_pts, len(stat) - 1)

            if nb_pts > (len(stat) - 1) // 2:
                nb_pts = (len(stat) - 1) // 2

            if nb_pts >= 0:
                filtre_min = stat[nb_pts - 1]
                filtre_max = stat[-nb_pts]

            else:
                filtre_min = -1000000.0
                filtre_max = 1000000.0

            for ii in range(i_deb, jj):
                if (
                    ii < len(filtered_df)
                    and filtered_df.iloc[ii][type_donnees] > val_manq
                ):
                    if filtered_df.iloc[ii][type_donnees] < filtre_min:
                        filtered_df.at[ii, type_donnees] = filtre_min
                    elif filtered_df.iloc[ii][type_donnees] > filtre_max:
                        filtered_df.at[ii, type_donnees] = filtre_max
                    else:
                        filtered_df.at[ii, type_donnees] = df.iloc[ii][type_donnees]
                else:
                    if ii < len(filtered_df):
                        filtered_df.at[ii, type_donnees] = df.iloc[ii][type_donnees]

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
