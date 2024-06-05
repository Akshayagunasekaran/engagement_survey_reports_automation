import pandas as pd
import reports_automation_v1.utilities as utilities



def get_long_term_trend_ques_rpt(df_data, scoring_weightage, report_config):
    """
    Generates a report on the long-term trend of performance.
    
    Args:
        df_data (pd.DataFrame): The DataFrame containing the survey data.
        scoring_weightage (dict): A dictionary containing the weightage of each question.
        report_config (dict): A dictionary containing the configuration for the report.
    
    Returns:
        pd.DataFrame: A DataFrame containing the report.
    """


    # Getting the question weightage for each question
    questions_weightage = scoring_weightage['question_weightage']
    # Getting the Survey Months for the filter
    filter_month_cols = list(set(df_data['Survey Assesment Window']))


    # Declaring the Report columns and creating a DataFrame structure
    df_rpt_columns = ['Survey Assesment Window']
    df_rpt_columns.extend(list(questions_weightage.keys()))
    df_rpt = pd.DataFrame(columns=df_rpt_columns)


    # Running a Loop for each metrics
    for each_metric in report_config['metric_cols']:
        # Filtering the master dataframe for each survey months
        for filter_val in filter_month_cols:
            df = df_data[df_data[each_metric]==filter_val]
            # Updating the dictionary with the month values
            df_row_dict = {each_metric: filter_val}
            # Getting the percentage for each question based on the weightage of each question
            ques_dict = utilities.get_aggregation_values(df, questions_weightage)
            # Updating the dictionary
            df_row_dict.update(ques_dict)
            # Updating it in the DataFrame
            df_rpt.loc[len(df_rpt)] = df_row_dict
        del df_row_dict
    # Transposing the whole dataframe to see question-wise Survey Month ranges
    df_rpt = df_rpt.T
    
    # Replacing null values with '-'
    df_rpt.fillna('-',inplace= True)
    
    

    return df_rpt