import pandas as pd

def get_futures_contract():
    df = pd.DataFrame([[1 for i in range(4)] for j in range(6)], columns=list('ABCD'))
    return df
    