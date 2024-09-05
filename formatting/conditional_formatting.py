import pandas as pd

# define the conditional formatting function
def conditional_formatting(val):
    if val >= 4:
        return 'background-color: #ACE1AF; color: black;'
    elif val <= 3:
        return 'background-color: #F4CCCC; color: black;'
    elif val >= 0.90:
        return 'background-color: #ACE1AF; color: black;'
    elif 0.80 <= val < 0.90:
        return 'background-color: #C9DAF8; color: black;'
    elif val < 0.80:
        return 'background-color: #F4CCCC; color: black;'
    else:
        return ''