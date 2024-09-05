import pandas as pd

def get_emp_trend_rpt(df_data, scoring_weightage):
    """
    """
    questions_weightage = scoring_weightage['question_weightage']
    ques_cols_list = list(questions_weightage.keys())
    filter_month_val = list(set(df_data['Survey Assesment Window'].unique()))
    df = df_data[ques_cols_list]>=4
    df_data['Overall %'] =  ((df.sum(axis = 1)) / len(ques_cols_list)) 
    df_rpt = pd.DataFrame()
    for filter_val in filter_month_val:
        filter_df = df_data[df_data['Survey Assesment Window']==filter_val]
        filter_df = filter_df[['Survey Assesment Window', 'Name', 'Overall %']]
        df_rpt = pd.concat([filter_df, df_rpt])
    df_pivot_rpt = pd.pivot_table(df_rpt,index=['Name'], columns= ['Survey Assesment Window'], values=['Overall %'], aggfunc='mean')
    return df_pivot_rpt