"""
Module with utility functions related to opening, reading and writing files
that can be commonly used across the project.
"""

import os
import sys
import pandas as pd

from easygui import fileopenbox
from pathlib import Path
from datetime import datetime


def read_sheet(file_path, sheet_name, skiprows=0):
    """
    Function to read an excel sheet in a given excel file as a Pandas DataFrame object

    Parameters:
    ----------
    file_path: str
        The full file path that will be used to read the excel file
    sheet_name: str
        The name of the sheet within the excel file to read
    skiprows: int
        The number of rows to skip from the top. Default value is 0.
    Returns:
    -------
    Return a Pandas DataFrame object of the excel sheet read
    """
    print('Loading ', sheet_name, 'sheet in ', file_path, ' as a data frame object...')
    data_frame = pd.read_excel(file_path, sheet_name, skiprows=skiprows)
    if data_frame is None and not data_frame.empty:
        sys.exit('Not able to load data frame')
    if (data_frame.empty):
        sys.exit('The data frame object is empty. Most likely, the sheet is empty')
    else:
        print('Loading done.')
        return data_frame

def save_to_excel(df_sheet_dict, file_name, dir_path = get_gen_reports_dir_path(), index=False, engine='openpyxl'):
    """
    Function to save a data frame to excel using openpyxl engine

    Parameters:
    ----------
    df_sheet_dict: dictionary
        A dictionary containing sheet-dataframe key-value pairs
    file_name: str
        File name to save the data in
    dir_path: str, optional
        The directory path to save the file in. Default is the generated reports directory path
    index: bool, optional
        Boolean value indicating if row names need to be written. Default is False
    engine: str
        The name of the Excel engine to be used. xlsxwriter or openpyxl. Default is openpyxl.
    """
    file_path = os.path.join(dir_path, file_name)
    datatoexcel = pd.ExcelWriter(file_path, engine=engine)
    for key in df_sheet_dict.keys():
        df_sheet_dict[key].to_excel(datatoexcel, sheet_name=key, index=index)
        print('Saving ', key, ' sheet in excel file: ', file_name, '....')
    datatoexcel.close()
    print('Save done')