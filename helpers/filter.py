from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype
import pandas as pd
import streamlit as st


def import_filter_params(filter_name) -> None:
    file = st.file_uploader(
        "Importer les filtres",
        type=["csv", "xlsx"],
        help="Importer un fichier contenant les filtres.",
    )
    if "uploaded_file" not in st.session_state:
        st.error("Merci d'importer un fichier.")
        return


def reset_filter_params(df, filter_name) -> None:
    # remove filter from session_state
    if filter_name in st.session_state["filters"]:
        del st.session_state["filters"][filter_name]

    # refresh form (all key of the form are store in session_state)
    for y in df.columns.tolist():
        if not is_numeric_dtype(df[y]) or is_datetime64_any_dtype(df[y]):
            continue
        _min = float(df[y].min())
        _max = float(df[y].max())
        if _min == _max:
            continue
        st.session_state[f"filter_form.{filter_name}.{y}"] = (_min, _max)


def save_filter_params(df, filter_name, widget_dict):
    # save filter in session_state
    for key, value in widget_dict.items():
        print(key, value)
        st.session_state["filters"][filter_name][key] = (
            value[0] if value[0] != df[key].min() else float("-inf"),
            value[1] if value[1] != df[key].max() else float("inf"),
        )


def filters_widgets(df: pd.DataFrame, filter_name: str) -> None:
    if not "filter" in st.session_state:
        st.session_state["filters"] = {}

    if not filter_name in st.session_state["filters"]:
        st.session_state["filters"][filter_name] = {}

    filter_widgets = st.container()

    widget_dict = {}
    unavailable_columns = []
    with filter_widgets.form(key="filter_form"):
        for y in df.columns.tolist():
            if not is_numeric_dtype(df[y]) or is_datetime64_any_dtype(df[y]):
                continue

            _min = float(df[y].min())
            _max = float(df[y].max())
            selected_opts = st.session_state["filters"][filter_name].get(
                y, (_min, _max)
            )

            if selected_opts[0] == selected_opts[1]:
                unavailable_columns.append(y)
                widget_dict[y] = (float("-inf"), float("inf"))
                continue

            widget_dict[y] = st.slider(
                label=y,
                min_value=_min,
                max_value=_max,
                value=selected_opts,
                key=f"filter_form.{filter_name}.{y}",
            )

        st.write(
            "Les colonnes suivantes ne sont pas filtrables : "
            + ", ".join(unavailable_columns)
        )

        # buttons on same line
        BTN1, BTN2, BTN3, SPACE = st.columns([1, 1, 1, 3])

        BTN1.form_submit_button(
            "Importer les filtres",
            on_click=import_filter_params,
            args=(filter_name,),
        )

        BTN2.form_submit_button(
            "Sauvegarder les filtres",
            on_click=save_filter_params,
            args=(
                df,
                filter_name,
                widget_dict,
            ),
        )

        BTN3.form_submit_button(
            "Réinitialiser les filtres",
            on_click=reset_filter_params,
            args=(
                df,
                filter_name,
            ),
        )


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
