import pandas

def get_sp_500():
    return pandas.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
        header=0
    )