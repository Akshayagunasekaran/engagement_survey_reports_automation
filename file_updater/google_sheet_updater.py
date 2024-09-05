"""
    Script to update the master responses sheet with the new survey responses
"""
from gspread_dataframe import set_with_dataframe
import reader.config_reader as config_reader

def master_sheet_updater(df, source_config):
    """
        Function to update the google sheet
                Parameters:
        -----------
            df: Table to be updated
            source_config: File Location to update
        Returns:
        --------   
            Pandas DataFrame
    """
    # Reading the master dataframe
    master_worksheet = config_reader.read_worksheet(source_config)

    # Update the Google Sheet with the DataFrame
    set_with_dataframe(master_worksheet, df)
    print("Master Sheet is updated.")

