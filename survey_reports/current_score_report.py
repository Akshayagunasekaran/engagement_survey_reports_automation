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
    group_cols = report_config['group_cols']

    # Getting the Dataset for the current month
    filter_month = report_config['filter_month_cols']
    df = df_data[df_data['Survey Assesment Window'].isin(filter_month)]

    # Adding Average to the current month report
    df['Average'] = df[list(questions_weightage.keys())].mean(axis=1)
    # Finding the Current month percentage for overall org
    df_rpt = df.groupby(by="Survey Assesment Window").agg({q: lambda x: utilities.ques_score_perc for q in questions_weightage.keys()})
    # Adding grouping columns to the report template
    df_rpt["group_cols"] = "Overall Org-wide"
    # Adding questions to the grouping columns to the report column list
    group_cols = group_cols.extend(list(questions_weightage.keys()))
    df_rpt = df_rpt[group_cols]
    # Dropping the Survey Assessment window column
    df_rpt.drop(columns="Survey Assesment Window", inplace=True)
    # Concatenating the latest month employee scores to the report
    df_rpt = pd.concat([df_rpt, df], ignore_index=True)
    

    # For Formatting
    for col in questions_weightage.keys():
        df_rpt[col] = pd.to_numeric(df_rpt[col], errors='coerce')

    #df_rpt = df_rpt.astype(updating_cols_to_float)
    # Getting the colour coding configs
    #colour_coding_configs = report_config["colour_coding"]
    #color_coding_cols = list(questions_weightage.keys()) 

    #formatted_df = conditional_formatting.colour_coding(df_rpt, color_coding_cols, colour_coding_configs)

    return df_rpt

def get_curr_metric_engagement_survey_rpt(df_data, report_config):
    """
    Get the current score percentage
    :param df_data:
    :param report_config:
    :return:
    """
