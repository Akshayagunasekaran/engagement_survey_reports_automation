import sys
sys.path.append('../')
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import reader.config_reader as config_reader
import survey_reports.current_score_report as current_score_report
import survey_reports.emp_long_term_trend_rpt as emp_long_term_trend_rpt
import survey_reports.long_term_trend_ques_rpt as long_term_trend_ques_rpt
import survey_reports.long_term_trend_group_rpt as long_term_trend_group_rpt

import file_updater.google_sheet_updater as google_sheet_updater

def map_team(team, team_clubbing_config):
    for key, value in team_clubbing_config.items():
        if team in key:
            return value
    return team
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
    left_df= merge_config["left_dataframe"]
    right_df = merge_config["right_dataframe"]

    # Getting the filter month configs 
    filter_month_cols = data_pre_process_configs["filter_month_cols"]
    exclude_configs = data_pre_process_configs["exclude_values"]
    merge_df = pd.merge(df_data_dict[left_df], df_data_dict[right_df], on= merge_config["grouping_cols"], how=merge_config['how'])
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
            df.drop_duplicates(subset=dup_col_subset, keep= 'last', ignore_index=True, inplace=True)
            # Updating it with the master dataframe
            df_processed = pd.concat([df_processed, df])
    
    print("Data Pre-Process is done")
    # Concatenating with the master dataframe
    df_concat = pd.concat([df_data_dict['emp_manager_mapping_data'],df_processed], ignore_index=True)
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

def get_engagement_reports_raw_data(source_configs):
    """
    Function to generate the raw data for engagement survey reports. This data would be merged 
    with the employee manager mapping data.

    """
     # Creating an empty dictionary
    df_data_dict = dict()
    for source_config in source_configs:
        # Getting the google sheet as a dataframe
        df_data = config_reader.read_con_credentials(source_config)
        # Updating it in the dictionary
        source_sheet_name = source_config['source_sheet_name']
        df_data_dict[source_config['source_name']] = df_data
        del df_data
    # Getting the keys of the dictionary for merge
    #merge_df_list = list(df_data_dict.keys())
    #merge_df = pd.merge(df_data_dict[merge_df_list[0]], df_data_dict[merge_df_list[1]], on= merge_sources["grouping_cols"], how=merge_sources['how'])

    return df_data_dict

def engagement_reports_generator():
    """
        Main Function to generate the required reports
    """
    # Getting the report configs
    report_config = config_reader.read_config("engagement_survey_report_configs.json", "Org_Wide_reports")

    # Getting the source config
    source_configs = report_config['source_config']
    sources = source_configs['sources']
    data_pre_process_configs = report_config["data_pre_process_configs"]
    question_id_mapping = report_config['question_id_mapping']
    # Reading the google sheets
    df_data = get_engagement_reports_raw_data(sources)
    # Getting the data pre-processed
    df_data = get_data_preprocessed(df_data, data_pre_process_configs, question_id_mapping)
    gen_rep_congig = report_config['org_wide_reports'] 
    df_rpts_dict = dict()
    date = pd.to_datetime('now').strftime('%B_%Y')

    for key,value in gen_rep_congig.items():
        print("Report generating for ", key)
        if key == 'curr_score':
            df_curr_scr_rpt = current_score_report.get_curr_score_engagement_survey_rpt(df_data.copy(), report_config['scoring_weightage'], value )
            df_rpts_dict.update({key: df_curr_scr_rpt})
            df_curr_scr_rpt.to_excel(key + "_" + date + ".xlsx")
            print("Report Generated for current score")
        
        elif key == "long_term_trend":
            df_long_trm_trend = long_term_trend_ques_rpt.get_long_term_trend_ques_rpt(df_data.copy(), report_config['scoring_weightage'], value )
            df_rpts_dict.update({key: df_long_trm_trend})
            df_long_trm_trend.to_excel(key + "_" + date + ".xlsx")
            print("Report generated for long term trend")
        elif key == "long_term_trend_emp":
            df_emp_long_trm_trend = emp_long_term_trend_rpt.get_emp_trend_rpt(df_data.copy(), report_config['scoring_weightage'] )
            df_rpts_dict.update({key: df_emp_long_trm_trend})
            df_emp_long_trm_trend.to_excel(key + "_" + date + ".xlsx")
            print("Report generated for employee long term trend")
        else:
            df_long_trm_trend_team = long_term_trend_group_rpt.get_long_term_trend_rpt(df_data.copy(), report_config['scoring_weightage'], 'Team' )
            print("Report Generated for team")
            df_long_term_trend_cohort = long_term_trend_group_rpt.get_long_term_trend_rpt(df_data.copy(), report_config['scoring_weightage'], 'Cohort' )
            print("Cohort")
            df_rpts_dict.update({key: df_long_trm_trend_team})
            df_long_trm_trend_team.to_excel(key + "_" + date + ".xlsx")
            df_long_term_trend_cohort.to_excel("Cohort" + "_" + date + ".xlsx")


    print("Save Done")
if __name__ == "__main__":
    engagement_reports_generator()
