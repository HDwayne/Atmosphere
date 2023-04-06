from pandas.api.types import is_datetime64_any_dtype
import pandas as pd
import streamlit as st

def reset_filter_widgets_to_default(filter_name) -> None:
    """
    Reset all filter widgets to their default values.
    
    Parameters
    ----------
    filter_name : str
        The name of the filter to reset.
    """
    if not isinstance(filter_name, str):
        raise TypeError(f"Expected filter_name to be a str, got {type(filter_name)} instead.")
    if filter_name in st.session_state:
      del st.session_state[filter_name]

def filters_widgets(df: pd.DataFrame, filter_name: str) -> None:
    if not filter_name in st.session_state:
      st.session_state[filter_name] = {}
    
    filter_widgets = st.container()
    filter_widgets.warning("Veillez cliquer sur le bouton 'Appliquer les filtres' pour appliquer les filtres.")

    widget_dict = {}
    with filter_widgets.form(key="filter_form"):
        for y in df.columns.tolist():
            if is_datetime64_any_dtype(df[y]):
              continue
                        
            _min = float(df[str(y)].min())
            _max = float(df[str(y)].max())
            selected_opts = st.session_state[filter_name].get(str(y), (_min, _max))
            
            widget_dict[y] = st.slider(
              label=str(y),
              min_value=_min,
              max_value=_max,
              value=selected_opts,
              key=str(y),
            )

        submit_button = st.form_submit_button("Appliquer les filtres")

        if submit_button:
            for key, value in widget_dict.items():
                # only save filter if itsn't the default value
                if not value == (df[key].min(), df[key].max()):
                    st.session_state[filter_name][key] = value
    
        filter_widgets.button(
            "Réinitialiser les filtres",
            key="reset_buttons",
            on_click=reset_filter_widgets_to_default,
            args=(filter_name,),
        )

def filter_dataframe(df: pd.DataFrame, filter_name: str) -> pd.DataFrame:
    """
    Filter a dataframe based on the values of the filter widgets.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to filter.
    filter_name : str
        The name of the filter to use.

    Returns
    -------
    pd.DataFrame
        The filtered dataframe (copy).
    """

    filtered_df = df.copy()
    filtered_df['valid'] = True

    if not filter_name in st.session_state:
        return filtered_df

    for key, value in st.session_state[filter_name].items():
        filtered_df.loc[~filtered_df[key].between(*value), 'valid'] = False

    return filtered_df


def getIndexRow(filtered_df: pd.DataFrame, filter_name: str, points:list[dict], column: str) -> list[int]:
    """
    Get the index of the rows in the dataframe that match the points.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to filter.
    filter_name : str
        The name of the filter to use.
    points : list[dict]
        The points to match.

    Returns
    -------
    list[int]
        The index of the rows in the dataframe that match the points.
    """
    index = []
    for point in points:
        if point['pointIndex'] == None:
            continue
        _min, _max = st.session_state[filter_name].get(column, (filtered_df[column].min(), filtered_df[column].max()))
        if not _min <= point['y'] <= _max:
            id = filtered_df.loc[filtered_df['valid'] == False].index[point['pointIndex']]
        else:
            id = filtered_df.loc[filtered_df['valid'] == True].index[point['pointIndex']]
        index.append(id)
    return index

def setRowInvalid(filtered_df: pd.DataFrame, index: list[int]) -> pd.DataFrame:
    """
    Set the rows with the given index to invalid.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to filter.
    index : list[int]
        The index of the rows to set to invalid.
    """
    print(filtered_df['valid'].value_counts())

    for i in index:
        filtered_df.loc[i, 'valid'] = False

    print(filtered_df['valid'].value_counts())
    return filtered_df