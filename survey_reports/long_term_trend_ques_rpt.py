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
    quest_list = list(questions_weightage.keys())
    df_rpt_columns.extend(quest_list)
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
    df_rpt_melt = pd.melt(df_rpt, id_vars=['Survey Assesment Window'], value_vars= quest_list, var_name='Questions', value_name='Overall %')
    df_rpt_pivot = pd.pivot_table(df_rpt_melt, index=['Questions'], columns=['Survey Assesment Window'], values='Overall %', aggfunc='mean')
    df_rpt_pivot.reset_index(inplace=True)
    print(df_rpt_pivot.columns)
    # Better Readability
    rpt_cols = ['Questions']
    df_rpt_pivot = utilities.column_better_readability(filter_month_cols,rpt_cols,df_rpt_pivot )
    df_rpt_pivot = utilities.question_better_readability(df_rpt_pivot,quest_list, 'Questions', 'quest_id', ['quest_id'])

    # Replacing null values with '-'
    df_rpt_pivot.fillna('-',inplace= True)
    
    

    return df_rpt_pivot