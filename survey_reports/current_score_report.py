import pandas as pd
import reports_automation_v1.utilities as utilities



def get_curr_score_engagement_survey_rpt(df_data, scoring_weightage, report_config):
    """
        Function to create a report based on the scores
    """
    # Getting the question weightage from the report configs
    questions_weightage = scoring_weightage['question_weightage']
    print(df_data)
    # Declaring the report columns for the generated report
    df_rpt_columns = report_config['report_cols']
    df_rpt_columns.extend(list(questions_weightage.keys()))
    df_rpt = pd.DataFrame(columns=df_rpt_columns)

    # Getting the Dataset for the current month
    filter_month = report_config['filter_month_cols']
    df = df_data[df_data['Survey Assesment Window'].isin(filter_month)]
    col_to_add_metric_name = report_config["col_to_add_metric_name"]

    # Checking for duplicates
    duplicate_check_col_name = report_config["duplicate_check_col_name"]
    df.drop_duplicates(subset= duplicate_check_col_name, keep = "last", inplace= True, ignore_index=True)

    # Getting the number of empty rows to be added for the generated report
    empty_rows = report_config["empty_rows"]

    # Running the loop for the metrics to be added for the report - Team-wise, Cohort-wise, Manager-wise
    for each_metric in report_config['metric_cols']:
        
        if each_metric == "Overall Org":          
            df_row_dict = {col_to_add_metric_name: each_metric + "-wide"} 
            ques_dict = utilities.get_aggregation_values(df, questions_weightage)
            df_row_dict.update(ques_dict)
            df_rpt.loc[len(df_rpt)] = df_row_dict
            df_rpt = pd.concat([df_rpt, df], join="inner")
            df_rpt.reset_index(inplace=True)
            
        else:
            metric_names_list = list(set(df[each_metric]))
            empty_df_dict = {col: ['' for i in range(empty_rows)] for col in df_rpt.columns}
            empty_df = pd.DataFrame(index=empty_df_dict, columns=df_rpt_columns)
            # Concatenate the original DataFrame with the empty DataFrame
            df_rpt = pd.concat([df_rpt, empty_df], ignore_index=True)
            df_row_dict = {col_to_add_metric_name: each_metric + "-wise"}
            ques_dict = {ques: "" for ques in questions_weightage.keys()}
            df_row_dict.update(ques_dict)
            df_rpt.loc[len(df_rpt)] = df_row_dict
            
            for metric_name in metric_names_list:
                df_row_dict = {col_to_add_metric_name: metric_name}
                df_filter = df[df[each_metric]==metric_name]
                ques_dict = utilities.get_aggregation_values(df_filter, questions_weightage)
                df_row_dict.update(ques_dict)
                df_rpt.loc[len(df_rpt)] = df_row_dict   
                
        del  df_row_dict
    

    # For Formatting
    for col in questions_weightage.keys():
        df_rpt[col] = pd.to_numeric(df_rpt[col], errors='coerce')

    #df_rpt = df_rpt.astype(updating_cols_to_float)
    # Getting the colour coding configs
    #colour_coding_configs = report_config["colour_coding"]
    #color_coding_cols = list(questions_weightage.keys()) 

    #formatted_df = conditional_formatting.colour_coding(df_rpt, color_coding_cols, colour_coding_configs)

    return df_rpt