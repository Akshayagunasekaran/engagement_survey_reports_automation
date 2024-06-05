"""
Script for all the common helper functions

"""
import pandas as pd

def get_aggregation_values(filter_df: pd.DataFrame, ques_weightage: dict):
    """
    Function to find the percentage for the given question weightage
    
    Args:
        filter_df (pd.DataFrame): The filtered DataFrame containing the survey data.
        ques_weightage (dict): A dictionary containing the weightage of each question.
    
    Returns:
        dict: A dictionary with the question as the key and the corresponding percentage as the value.
    """

    ques_dict = dict()
    for question, ques_weightage in ques_weightage.items():
        month_perc = ((sum(filter_df[question] >= ques_weightage ) / filter_df[question].count()))
        #month_perc = str(month_perc) + '%'
        ques_dict.update({question: month_perc})
    return ques_dict
