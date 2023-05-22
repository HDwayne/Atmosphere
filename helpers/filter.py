import pandas as pd
import streamlit as st
import numpy as np
from pandas.api.types import is_numeric_dtype, is_datetime64_any_dtype


def import_filter_params(filter_name) -> None:
    if "yaml" in st.session_state and filter_name in st.session_state["yaml"]:
        filter_params = st.session_state["yaml"][filter_name]
        st.session_state["filters"][filter_name] = filter_params

        for key, value in filter_params.items():
            if f"filter_form.{filter_name}.{key}" in st.session_state:
                st.session_state[f"filter_form.{filter_name}.{key}"] = (
                    float(value["min"]),
                    float(value["max"]),
                )


def reset_filter_params(df, filter_name) -> None:
    if filter_name in st.session_state["filters"]:
        del st.session_state["filters"][filter_name]

    for y in df.select_dtypes(include=[np.number]):
        _min, _max = float(df[y].min()), float(df[y].max())
        if pd.notnull(_min) and pd.notnull(_max) and _min != _max:
            st.session_state[f"filter_form.{filter_name}.{y}"] = (_min, _max)


def save_filter_params(df, filter_name, widget_dict):
    if filter_name not in st.session_state["filters"]:
        st.session_state["filters"][filter_name] = {}

    for key, value in widget_dict.items():
        _min = value[0] if value[0] != df[key].min() else float("-inf")
        _max = value[1] if value[1] != df[key].max() else float("inf")
        st.session_state["filters"][filter_name][key] = {"min": _min, "max": _max}


def filters_widgets(df: pd.DataFrame, filter_name: str) -> None:
    if not "filter" in st.session_state:
        st.session_state["filters"] = {}

    if not filter_name in st.session_state["filters"]:
        st.session_state["filters"][filter_name] = {}

    filter_widgets = st.container()

    widget_dict = {}
    unavailable_columns = []
    with filter_widgets.form(key="filter_form"):
        for y in df.select_dtypes(include=[np.number]):
            _min, _max = float(df[y].min()), float(df[y].max())

            if pd.notnull(_min) and pd.notnull(_max) and _min != _max:
                widget_dict[y] = st.slider(
                    label=y,
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    key=f"filter_form.{filter_name}.{y}",
                )
            else:
                unavailable_columns.append(y)
                widget_dict[y] = (float("-inf"), float("inf"))

        if unavailable_columns:
            st.write(
                "Les colonnes suivantes ne sont pas filtrables : "
                + ", ".join(unavailable_columns)
            )

        BTN1, BTN2, BTN3, SPACE = st.columns([1, 1, 1, 3])
        with BTN1:
            st.form_submit_button(
                "Charger depuis YAML",
                disabled=not "yaml" in st.session_state,
                on_click=import_filter_params,
                args=(filter_name,),
            )

        with BTN2:
            st.form_submit_button(
                "Sauvegarder les filtres",
                on_click=save_filter_params,
                args=(df, filter_name, widget_dict),
            )

        with BTN3:
            st.form_submit_button(
                "Réinitialiser les filtres",
                on_click=reset_filter_params,
                args=(df, filter_name),
            )

    if "yaml" in st.session_state and filter_name in st.session_state["yaml"]:
        st.write(st.session_state["yaml"][filter_name])

    st.write(st.session_state["filters"])


# def filter_dataframe(df: pd.DataFrame, filter_name: str) -> pd.DataFrame:
#     """
#     Filter a dataframe based on the values of the filter widgets.

#     Parameters
#     ----------
#     df : pd.DataFrame
#         The dataframe to filter.
#     filter_name : str
#         The name of the filter to use.

#     Returns
#     -------
#     pd.DataFrame
#         The filtered dataframe (copy).
#     """

#     filtered_df = df.copy()
#     filtered_df["valid"] = True

#     if not filter_name in st.session_state:
#         return filtered_df

#     for key, value in st.session_state["filters"][filter_name].items():
#         filtered_df.loc[~filtered_df[key].between(*value), "valid"] = False

#     return filtered_df
