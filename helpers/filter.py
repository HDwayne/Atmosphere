from pandas.api.types import is_datetime64_any_dtype
import pandas as pd
import streamlit as st


def filter_dataframe(df: pd.DataFrame, filter_name:str) -> pd.DataFrame:
  """
  Filter a dataframe with a slider for each numeric column.
  The filter is stored in the session state.

  Parameters
  ----------
  df : pd.DataFrame
  The dataframe to filter
  filter_name : str
  The name of the filter

  Returns
  -------
  pd.DataFrame
  The filtered dataframe
  """

  # TODO: Solve rollback issue on slider

  df = df.copy()

  if 'valid' not in df.columns:
    df['valid'] = True

  if not filter_name in st.session_state:
    st.session_state[filter_name] = {}

  modification_container = st.container()
  with modification_container:
    filtrable_columns = df.select_dtypes(include=["category", "int64", "float64"]).columns
    to_filter_columns = st.multiselect(
      "Appliquer un filtre sur les colonnes suivantes",
      filtrable_columns,
      default=st.session_state[filter_name].get("to_filter_columns", [])
    )
    st.session_state[filter_name]["to_filter_columns"] = to_filter_columns
    for column in to_filter_columns:
      if not is_datetime64_any_dtype(df[column]):
        left, right = st.columns((1, 20))
        left.write("↳")

        _min = float(df[column].min())
        _max = float(df[column].max())
        step = (_max - _min) / 100
        user_num_input = right.slider(
          f"Valeur de {column}",
          min_value=_min,
          max_value=_max,
          value=st.session_state[filter_name].get(column, (_min, _max)),
          step=step,
        )
        df.loc[~df[column].between(*user_num_input), 'valid'] = False
        st.session_state[filter_name][column] = tuple(user_num_input)

  for key in list(st.session_state[filter_name].keys()):
    if key not in to_filter_columns:
      st.session_state[filter_name].pop(key)
  return df