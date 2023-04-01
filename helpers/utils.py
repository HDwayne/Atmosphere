import base64
from io import StringIO
import zipfile
import pandas as pd
import streamlit as st

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
    
    
    with open('assets/Laero_bg.png', 'rb') as f:
        data = f.read()
    
    bin_str = base64.b64encode(data).decode()
    html_code = f'''
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
                '''

    return html_code

def checkFileName(file_name, contain_date=True):
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


def CheckZipFileName(file_name):
    info = file_name.replace(".zip", "").split("_")
    if len(info) != 3:
        return False
    if info[0] != "BrtPdm":
        return False
    if info[1] != "CHIMIE":
        return False
    if len(info[2]) != 8:
        return False
    return True

def read_zip_file(zip_file_path: str) -> dict[str, pd.DataFrame]:
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
                    df = pd.read_csv(StringIO(data), header=None,
                                     names=header_list, sep=" ")
                except ValueError:
                    header_list = file_contents.strip().split(sep=",")
                    df = pd.DataFrame(columns=header_list)
                file_name = deleteDateFromFileNames(file_name)
                df.Name = file_name
                dfs[file_name] = df
    return dfs

def getDateFromZipFileName(file_name):
    info = file_name.replace(".zip", "").split("_")
    return info[2]

def deleteDateFromFileNames(file_name):
    info = file_name.replace(".txt", "").split("_")
    return info[0] + "_" + info[1] + "_" + info[2]

def delete_session_state():
    """
    Delete all session state variables
    """
    for key in st.session_state.keys():
        del st.session_state[key]

def delete_session_state_rule(rule: callable, **kwargs):
    """
    Delete all session state variables
    """
    for key in list(st.session_state.keys()):
        if rule(key, **kwargs):
            del st.session_state[key]

def getNumberFileImpoted():
    return len([key for key in st.session_state.keys() if checkFileName(key, contain_date=False)])

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


def deleteDaysFromDataframe(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Delete days from a date column.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to modify.

    column_name : str
        The name of the date column.

    Returns
    -------
    pd.DataFrame
        The modified DataFrame.
    """
    format="%d/%m/%Y,%H:%M:%S"
    newformat="%H:%M:%S"

    # si le dataframe est vide, on retourne un dataframe vide
    if not df.empty:
        try:
            df[column_name] = pd.to_datetime(df[column_name], format=format)
            df[column_name] = df[column_name].dt.strftime(newformat)
        except ValueError:
            print(f"Failed to convert column {column_name} to datetime64 on {df.Name}.")
