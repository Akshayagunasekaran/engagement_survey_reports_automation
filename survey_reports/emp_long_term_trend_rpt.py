import pandas as pd
from datetime import datetime
def get_emp_trend_rpt(df_data, scoring_weightage):
    """
    """
    questions_weightage = scoring_weightage['question_weightage']
    ques_cols_list = list(questions_weightage.keys())
    filter_month_val = list(set(df_data['Survey Assesment Window'].unique()))
    df = df_data[ques_cols_list] >= 4
    df_data['Overall %'] = ((df.sum(axis=1)) / len(ques_cols_list))
    df_rpt = pd.DataFrame()
    for filter_val in filter_month_val:
        filter_df = df_data[df_data['Survey Assesment Window'] == filter_val]
        filter_df = filter_df[['Survey Assesment Window', 'Name', 'Overall %']]
        df_rpt = pd.concat([filter_df, df_rpt])
    df_pivot_rpt = pd.pivot_table(df_rpt,index=['Name'], columns= ['Survey Assesment Window'], values=['Overall %'], aggfunc='mean')
    df_pivot_rpt.columns = df_pivot_rpt.columns.get_level_values(1)
    df_pivot_rpt.reset_index(inplace=True)
    print(df_pivot_rpt.columns)
    df_pivot_rpt.rename(columns={'Survey Assesment Window': 'Name'}, inplace=True)
    #df_pivot_rpt = df_pivot_rpt.drop(df_pivot_rpt.index[0])

    print(df_pivot_rpt.columns)
    # Column Reordering for better readability

    months_list = list(filter_month_val)

    months_list.sort(key=lambda month_year: datetime.strptime(month_year, "%b %Y"))
    df_rpt_cols = ["Name"] + months_list
    df_pivot_rpt = df_pivot_rpt.loc[:, df_rpt_cols]
    return df_pivot_rpt