"""
 Script to generate Long Term Percentage Survey Reports based on a particular metric name
"""
import pandas as pd
import reports_automation_v1.utilities as utilities
from datetime import datetime


def get_long_term_trend_rpt(df_data: pd.DataFrame, scoring_weightage: dict, metric_name: str):
    """
    Generates a report on the long-term trend base on the given metric.
    
    Args:
        df_data (pd.DataFrame): The DataFrame containing the survey data.
        scoring_weightage (dict): A dictionary containing the weightage of each question.
        metric_name (str): Column Name to group the survey months
                           Example: "Cohort"
    
    Returns:
        pd.DataFrame: A DataFrame containing the report.
    """
    # Getting the question weightage for each question
    questions_weightage = scoring_weightage['question_weightage']
    # Getting the unique teams and Survey Assessment Windows
    unique_groups = df_data[metric_name].unique()
    unique_survey_months = df_data['Survey Assesment Window'].unique()
    # Initialize an empty list to store the report data
    report_data = []

    # Loop through each team and survey month
    for team in unique_groups:
        for survey_month in unique_survey_months:
            # Filter the data for the current team and survey month
            filter_df = df_data[(df_data[metric_name] == team) & (df_data['Survey Assesment Window'] == survey_month)]
            
            # Calculate the percentage for each question
            ques_dict = utilities.get_aggregation_values(filter_df, questions_weightage)

            # Create a dictionary to store the report data
            report_row = {metric_name: team, 'Survey Assesment Window': survey_month}
            report_row.update(ques_dict)

            # Add the report data to the list
            report_data.append(report_row)
    
    # Create a DataFrame from the report data
    df_rpt = pd.DataFrame(report_data)
    
    # Melt the DataFrame to have questions as rows
    df_rpt = pd.melt(df_rpt, id_vars=[metric_name, 'Survey Assesment Window'], var_name='Question', value_name='Percentage')
    
    # Pivot the DataFrame to have Survey Assessment Windows as columns
    df_rpt = df_rpt.pivot_table(index=[metric_name, 'Question'], columns='Survey Assesment Window', values='Percentage')
    # Reset the index to have Team and Question as columns
    df_rpt = df_rpt.reset_index()
    
    # Column Reordering for better readability
    
    months_list = list(unique_survey_months)

    months_list.sort(key = lambda month_year: datetime.strptime(month_year, "%b %Y"))

    
    df_rpt_cols = [metric_name, 'Question']
    df_rpt_cols.extend(months_list)
    df_rpt = df_rpt.loc[:, df_rpt_cols]
    df_rpt.fillna('-',inplace= True)
    
    # Sortin the questions 
    ques_list = list(questions_weightage.keys())
    ques_order = {ques: i+1 for i, ques in enumerate(ques_list)}

    df_rpt['ques_id'] = df_rpt['Question'].apply(lambda ques: ques_order[ques])

    df_rpt.sort_values(by = [ metric_name, 'ques_id'],inplace=True)
    # Dropping the question id column
    df_rpt.drop(columns=['ques_id'],inplace=True)
        
    # Return the final report
    return df_rpt
