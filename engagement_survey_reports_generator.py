"""
Script to generate the Q12 Engagement Survey Reports in one go
"""

import reader.config_reader as config_reader
import pandas as pd

def get_data_preprocessed(df_data_dict, data_pre_process_configs, question_id_mapping):
    """
    Function to prepare the data before creating the reports

    Parameters:
    ----------
        df: DataFrame to be pre-processed
        data_pre_process_configs: dict()
            Survey Months,
            Creating Month and Year Specific Configs,
            Duplicates checking columns list,
            Excluding filter values from the dataframe
    Returns:
    ----------
    Pre-Processed DataFrame
    """
    print("Data is being pre-processed before creating the reports....")
    # Getting the Column Names for the year columns
    month_year_configs = data_pre_process_configs["month_year"]
    col_check = month_year_configs["col_check"]
    new_col_name = month_year_configs["insert_col_name"]

    # Getting the duplicate and column name config for the newly created column
    dup_col_subset = month_year_configs["duplicate_check_col_name"]
    survey_month_range_col = month_year_configs["updated_col_name"]

    merge_config = data_pre_process_configs["merge_sources"]
    left_df = merge_config["left_dataframe"]
    right_df = merge_config["right_dataframe"]

    # Getting the filter month configs
    filter_month_cols = data_pre_process_configs["filter_month_cols"]
    exclude_configs = data_pre_process_configs["exclude_values"]
    merge_df = pd.merge(df_data_dict[left_df], df_data_dict[right_df], on=merge_config["grouping_cols"],
                        how=merge_config['how'])
    for key, value in exclude_configs.items():
        merge_df = merge_df[~merge_df[key].isin(value)]
    # Adding date and year as a separate columns to create a report for long term trend
    merge_df[new_col_name] = pd.DatetimeIndex(merge_df[col_check]).strftime('%b %Y')
    # Creating an empty dataframe
    df_processed = pd.DataFrame()
    for month, filter_val in filter_month_cols.items():
        # Filtering for each months and updating it with a pre-determined range
        df = merge_df[merge_df[new_col_name].isin(filter_val)]
        df[survey_month_range_col] = month
        # Removing the duplicates in the dataset
        df.drop_duplicates(subset=dup_col_subset, keep='last', ignore_index=True, inplace=True)
        # Updating it with the master dataframe
        df_processed = pd.concat([df_processed, df])

    print("Data Pre-Process is done")
    # Concatenating with the master dataframe
    df_concat = pd.concat([df_data_dict['emp_manager_mapping_data'], df_processed], ignore_index=True)
    # Changing the column name to better readability
    df_concat.rename(columns=question_id_mapping, inplace=True)
    """
    print("Updating the master google worksheet....")
    # Getting the master sheet configs to update the google master shet
    master_sheet_configs = data_pre_process_configs["concat_master_config"]
    google_sheet_updater.master_sheet_updater(df_concat,master_sheet_configs)
    """
    date = pd.to_datetime('now').strftime('%B_%Y')

    df_concat.to_excel("Engagement_survey_merged_raw_data_" + date + ".xlsx")
    return df_concat


def generate_all():
    """
    Function to generate all the reports in one go

    """
    # Getting the report configs
    report_config = config_reader.read_config("engagement_survey_configs.json", "Q12_FIRST_LEVEL_ANALYSIS")

    # Getting the pre-process configs
    pre_process_configs = report_config['pre_process_configs']

