import sys
sys.path.append('./')
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import reader.config_reader as config_reader
import survey_reports.current_score_report as current_score_report
import survey_reports.emp_long_term_trend_rpt as emp_long_term_trend_rpt
import survey_reports.long_term_trend_ques_rpt as long_term_trend_ques_rpt
import survey_reports.long_term_trend_group_rpt as long_term_trend_group_rpt


def get_data_preprocessed(df_data, filter_month_cols):
    """
    Function to prepare the data before creating the reports

    Parameters:
    ----------
        df: DataFrame to be pre-processed
    Returns:
    ----------
    Pre-Processed DataFrame
    """
    print("Data is being pre-processed before creating the reports")
    # Adding date and year as a separate columns to create a report for long term trend
    df_data['Month & Year'] = pd.DatetimeIndex(df_data['Timestamp']).strftime('%b %Y')
    df_processed = pd.DataFrame()
    for month, filter_val in filter_month_cols.items():
            df = df_data[df_data['Month & Year'].isin(filter_val)]
            df['Survey Assesment Window'] = month
            df_processed = pd.concat([df_processed, df])
            #print(df_processed.columns)
    #df_processed.to_excel('Engagement_survey_merged_raw_data_v1.xlsx')
    return df_processed

def get_engagement_reports_raw_data(source_configs, merge_cols):
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
    merge_df_list = list(df_data_dict.keys())
    merge_df = pd.merge(df_data_dict[merge_df_list[0]], df_data_dict[merge_df_list[1]], on= merge_cols)

    return merge_df

def engagement_reports_generator():
    """
        Main Function to generate the required reports
    """
    # Getting the report configs
    report_config = config_reader.reading_config("engagement_survey_report_configs.json", "Org_Wide_reports")

    # Getting the source config
    source_configs = report_config['source_config']
    sources = source_configs['sources']
    merge_cols = report_config['merge_cols']
    filter_month_cols = report_config['filter_month_cols']
    df_data = get_engagement_reports_raw_data(sources, merge_cols)
    df_data = get_data_preprocessed(df_data, filter_month_cols)
    gen_rep_congig = report_config['org_wide_reports'] 
    df_rpts_dict = dict()
    
    for key,value in gen_rep_congig.items():
        print("Report generating for ", key)
        if key == 'curr_score':
            df_curr_scr_rpt = current_score_report.get_curr_score_engagement_survey_rpt(df_data.copy(), report_config['scoring_weightage'], value )
            df_rpts_dict.update({key: df_curr_scr_rpt})
            df_curr_scr_rpt.to_excel(key + "_rpt_latest.xlsx")
            print("Report Generated for current score")
        
        elif key == "long_term_trend":
            df_long_trm_trend = long_term_trend_ques_rpt.get_long_term_trend_ques_rpt(df_data.copy(), report_config['scoring_weightage'], value )
            df_rpts_dict.update({key: df_long_trm_trend})
            df_long_trm_trend.to_excel(key + "_rpt_latest.xlsx")
            print("Report generated for long term trend")
        elif key == "long_term_trend_emp":
            df_emp_long_trm_trend = emp_long_term_trend_rpt.get_emp_trend_rpt(df_data.copy(), report_config['scoring_weightage'] )
            df_rpts_dict.update({key: df_emp_long_trm_trend})
            df_emp_long_trm_trend.to_excel(key+ "_latest.xlsx")
            print("Report generated for employee long term trend")
        else:
            df_long_trm_trend_team = long_term_trend_group_rpt.get_long_term_trend_rpt(df_data.copy(), report_config['scoring_weightage'], 'Team' )
            print("Report Generated for team")
            df_long_term_trend_cohort = long_term_trend_group_rpt.get_long_term_trend_rpt(df_data.copy(), report_config['scoring_weightage'], 'Cohort' )
            print("Cohort")
            df_rpts_dict.update({key: df_long_trm_trend_team})
            df_long_trm_trend_team.to_excel("engagement_survey_responses_" +key + "_rpt_latest.xlsx")
            df_long_term_trend_cohort.to_excel("cohort.xlsx")
        
    print("Save Done")
if __name__ == "__main__":
    engagement_reports_generator()
