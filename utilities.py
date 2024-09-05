"""
Script for all the common helper functions

"""
import pandas as pd
from datetime import datetime

def get_aggregation_values(filter_df: pd.DataFrame, ques_weightage: dict):
    """
    Function to find the percentage for the given question weightage
    
    Args:
        filter_df (pd.DataFrame): The filtered DataFrame containing the survey data.
        ques_weightage (dict): A dictionary containing the weightage of each question.
    
    Returns:
        dict: A dictionary with the question as the key and the corresponding percentage as the value.
    """
    ques_dict =  {question: (filter_df[question].ge(ques_weightage).mean()) for question, ques_weightage in ques_weightage.items()}
    
    return  ques_dict

def column_better_readability(survey_months, rpt_cols_to_add, df):
    """
    """
    survey_months.sort(key= lambda month_year: datetime.strptime(month_year, "%b %Y"))
    rpt_cols_to_add.extend(survey_months)
    df = df.loc[:, rpt_cols_to_add]

    return df

def question_better_readability(df, quest_list, col_add, insert_col_name, sort_cols):
    """
    """
    ques_order = {ques: i+1 for i, ques in enumerate(quest_list)}
    df[insert_col_name] = df[col_add].apply(lambda ques: ques_order[ques])
    df.sort_values(by = sort_cols,inplace=True)
    # Dropping the question id column
    df.drop(columns=insert_col_name,inplace=True)
    
    return df