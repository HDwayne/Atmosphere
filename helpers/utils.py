import base64
from io import StringIO, BytesIO
import zipfile
import pandas as pd
import streamlit as st
import yaml


def print_widgets_separator(n=1, sidebar=False):
    """
    Prints customized separation line on sidebar
    """
    html = """<hr style="height:1px;
            border:none;color:#fff;
            background-color:#999;
            margin-top:5px;
            margin-bottom:10px"
            />"""

    for _ in range(n):
        if sidebar:
            st.sidebar.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown(html, unsafe_allow_html=True)


@st.cache_data
def show_Laero_logo(width, padding, margin):
    padding_top, padding_right, padding_bottom, padding_left = padding
    margin_top, margin_right, margin_bottom, margin_left = margin

    with open("assets/Laero_bg.png", "rb") as f:
        data = f.read()

    bin_str = base64.b64encode(data).decode()
    html_code = f"""
                <img src="data:image/png;base64,{bin_str}"
                style="
                     margin: auto;
                     width: {width}%;
                     margin-top: {margin_top}px;
                     margin-right: {margin_right}px;
                     margin-bottom: {margin_bottom}px;
                     margin-left: {margin_left}%;
                     padding-top: {padding_top}px;
                     padding-right: {padding_right}px;
                     padding-bottom: {padding_bottom}px;
                     padding-left: {padding_left}%;
                     "/>
                """

    return html_code


def checkFileName(file_name: str, contain_date: bool = True):
    """
    Check if a file name is valid.

    Parameters
    ----------
    file_name : str
        The file name.
    contain_date : bool, optional
        If True, the file name must contain a date, by default True.

    Returns
    -------
    bool
        True if the file name is valid, False otherwise.
    """
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")
    if not isinstance(contain_date, bool):
        raise TypeError("contain_date must be a boolean")
    info = file_name.replace(".txt", "").split("_")
    if contain_date and len(info) != 4 or not contain_date and len(info) != 3:
        return False
    if info[0] != "Pdm":
        return False
    if info[1] != "TEI48" and info[1] != "TEI49":
        return False
    if info[2] != "Data" and info[2] != "Zero" and info[2] != "Fonct":
        return False
    if contain_date and len(info[3]) != 8:
        return False
    return True


def CheckZipFileName(file_name: str) -> bool:
    """
    Check if a zip file name is valid.

    Parameters
    ----------
    file_name : str
        The file name.

    Returns
    -------
    bool
        True if the file name is valid, False otherwise.
    """
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")

    info = file_name.replace(".zip", "").split("_")
    if len(info) != 3:
        return False
    if info[0] != "BrtPdm":
        return False
    # if info[1] != "CHIMIE":
    #    return False
    if len(info[2]) != 8:
        return False
    return True


def read_zip_file(zip_file_path: BytesIO) -> dict[str, pd.DataFrame]:
    """
    Read the contents of a zip file and return a dictionary of DataFrames.

    Parameters
    ----------
    zip_file_path : str
        The path to the zip file.

    Returns
    -------
    dict[str, pd.DataFrame]
        A dictionary of DataFrames with the file name as the key.
    """
    dfs: dict[str, pd.DataFrame] = {}

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith(".txt") and checkFileName(file_name):
                with zip_ref.open(file_name) as file:
                    file_contents = file.read().decode("utf-8")
                try:
                    header, data = file_contents.strip().split("\n", 1)
                    header_list = header.split(sep=",")
                    df = pd.read_csv(
                        StringIO(data), header=None, names=header_list, sep=" "
                    )
                except ValueError:
                    header_list = file_contents.strip().split(sep=",")
                    df = pd.DataFrame(columns=header_list)
                file_name = deleteDateFromFileNames(file_name)
                df.Name = file_name
                dfs[file_name] = df
    return dfs


def dfs_to_session_state(dfs: dict[str, pd.DataFrame]) -> list[str]:
    if not "dfs" in st.session_state:
        st.session_state["dfs"] = {}

    added_file = []
    apply_time_dfs(dfs, ["20t_Date"], "%d/%m/%Y,%H:%M:%S")
    for key, value in dfs.items():
        added_file.append(key)
        if not key in st.session_state:
            st.session_state["dfs"][key] = value
        else:
            st.session_state["dfs"][key] = st.session_state["dfs"][key]
            # Iterate over the columns in the DataFrame
        for col in value.columns:
            # Check if the column name contains "\r"
            if "\r" in col:
                # Clean the column name by removing "\r"
                new_col = col.replace("\r", "")
                # Rename the column in the DataFrame
                value.rename(columns={col: new_col}, inplace=True)
    return added_file


# def getDateFromZipFileName(file_name: str) -> str:
#     """
#     Get the date from a zip file name.

#     Parameters
#     ----------
#     file_name : str
#         The file name.

#     Returns
#     -------
#     str
#         The date.
#     """
#     if not isinstance(file_name, str):
#         raise TypeError("file_name must be a string")

#     info = file_name.replace(".zip", "").split("_")
#     return info[2]


def deleteDateFromFileNames(file_name: str) -> str:
    """
    Delete the date from a file name.

    Parameters
    ----------
    file_name : str
        The file name.

    Returns
    -------
    str
        The file name without the date.
    """
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string")

    info = file_name.replace(".txt", "").split("_")
    return info[0] + "_" + info[1] + "_" + info[2]


# def delete_session_state() -> None:
#     """
#     Delete all session state variables
#     """
#     for key in st.session_state.keys():
#         del st.session_state[key]


def delete_session_state_rule(rule: callable, **kwargs) -> None:
    """
    Delete all session state variables

    Parameters
    ----------
    rule : callable
        A function that takes a key and returns a boolean.

    **kwargs
        Keyword arguments to pass to the function.

    Raises
    ------
    TypeError
        If rule is not a callable.
    """
    if not callable(rule):
        raise TypeError("rule must be a callable")

    if "dfs" in st.session_state:
        for key in list(st.session_state["dfs"].keys()):
            if rule(key, **kwargs):
                del st.session_state["dfs"][key]

    if "filters" in st.session_state:
        for key in list(st.session_state["filters"].keys()):
            if rule(key, **kwargs):
                del st.session_state["filters"][key]


def getNumberFileImpoted() -> int:
    """
    Get the number of files imported in the session state.
    """
    return len(
        [
            key
            for key in st.session_state["dfs"].keys()
            if checkFileName(key, contain_date=False)
        ]
    )


def for_each_df(dfs: dict[str, pd.DataFrame], func: callable, **kwargs) -> None:
    """
    Apply a function to each DataFrame in a dictionary of DataFrames.

    Parameters
    ----------
    dfs : dict[str, pd.DataFrame]
        A dictionary of DataFrames.

    func : callable
        A function to apply to each DataFrame.

    **kwargs
        Keyword arguments to pass to the function.

    Raises
    ------
    TypeError
        If dfs is not a dictionary of DataFrames.
    TypeError
        If dfs keys are not strings.
    TypeError
        If dfs values are not DataFrames.
    TypeError
        If func is not a callable.
    """
    if not isinstance(dfs, dict):
        raise TypeError("dfs must be a dictionary of DataFrames")

    if not all(isinstance(key, str) for key in dfs.keys()):
        raise TypeError("dfs keys must be strings")

    if not all(isinstance(df, pd.DataFrame) for df in dfs.values()):
        raise TypeError("dfs values must be DataFrames")

    if not callable(func):
        raise TypeError("func must be a callable")

    for df in dfs.values():
        func(df, **kwargs)


def apply_time_df(
    df: pd.DataFrame, time_columns: list[str], time_format: str | None = None
) -> None:
    """
    Convert columns in a DataFrame to datetime64.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame to convert the columns in.

    time_columns : list[str]
        A list of column names to convert to datetime64.

    time_format : str | None
        The format of the time columns. If None, the default format is used.
    """
    for col in time_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], format=time_format)
            except ValueError as e:
                print(f"Failed to convert column {col} to datetime64 on {df.Name}.")
                print(e)


def apply_time_dfs(
    dfs: dict[str, pd.DataFrame],
    time_columns: list[str],
    time_format: str | None = None,
) -> None:
    """
    Convert columns in a dictionary of DataFrames to datetime64.

    Parameters:
    -----------
    dfs : dict[str, pd.DataFrame]
        The dictionary of DataFrames to convert the columns in.

    time_columns : list[str]
        A list of column names to convert to datetime64.

    time_format : str | None
        The format of the time columns. If None, the default format is used.
    """
    for_each_df(dfs, apply_time_df, time_columns=time_columns, time_format=time_format)


# def export_meandata(df):
#     with open('output.txt', 'w') as f:
#         f.write(df.describe().to_csv(sep='\t'))
#     return f

# @st.cache_data
# def convert_df(df):
#     return df.to_csv(index=False).encode('utf-8')


@st.cache_data
def generate_zip(df, df_name):
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr(f"{df_name}.txt", df.to_csv(index=False).encode("utf-8"))
    return buffer.getvalue()


def load_yaml_file(uploaded_file):
    data = yaml.safe_load(uploaded_file)
    return data


# def save_yaml_file():
#     stream = BytesIO()
#     with stream:
#         yaml.dump(st.session_state["filters"], stream)
#     return stream.getvalue()
