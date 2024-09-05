import pandas as pd
import gspread

import json
# Getting the config file location
config = r"C:\Users\SSEMIS-Rashmi\engagement_survey_reports/read_gsheet_configs.json"

def read_config(json_file_name, report_name):
    file_path = r"C:\Users\SSEMIS-Rashmi\engagement_survey_reports\reports_automation_v1\configs/" + json_file_name
    with open(file_path, 'r', encoding='utf-8') as file_open:
        file_content = file_open.read()
        config = json.loads(file_content)
        for report_config in config['report_configs']:
            if report_config['report_name'] == report_name:
                return report_config
            else:
                return None

def read_con_credentials(source_config):
    """
        Function to read the google sheet as a pandas dataframe
        Parameters:
        -----------
            file_name: Google Sheet File Name
            sheet_name: Sheet Name
        Returns:
        --------   
            Pandas DataFrame
    """
    file_name = source_config['source_file_name']
    sheet_name = source_config['source_sheet_name']
    
    # Reading the credentials
    conn_cred = gspread.service_account(config)
    # Establish the connection
    df_connection = conn_cred.open(file_name)
    # Reading the Excel Sheet
    wks = df_connection.worksheet(sheet_name)
    # Converting to a pandas dataframe
    df = pd.DataFrame(wks.get_all_records())
    print("Succcessfully read " +sheet_name+ " sheet")

    
    return df

def read_worksheet(source_config):
    """
    Function to return the Google worksheet
    Parameters:
        -----------
            source_config: Google Sheet File Name
        Returns:
        --------   
            Google worksheet
    """
    file_name = source_config['source_file_name']
    sheet_name = source_config['source_sheet_name']
    
    # Reading the credentials
    conn_cred = gspread.service_account(config)
    # Establish the connection
    df_connection = conn_cred.open(file_name)
    # Reading the Excel Sheet
    wks = df_connection.worksheet(sheet_name)

    return wks
