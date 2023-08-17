import datetime
import io
import matplotlib
import pandas
import pandas_datareader
import pathlib
import requests
import zipfile

def create_directory(data_path):
    if not data_path.exists():
        print(f'creating directory for {data_path}...')
        data_path.mkdir(exist_ok=True, parents=True)

def dera_url():
    return 'https://www.sec.gov/files/dera/data/financial-statement-and-notes-data-sets/'

def today():
    return pandas.Timestamp(datetime.date.today())

def current_year():
    return today().year

def current_quarter():
    return today().quarter

def past_years():
    return range(2009, current_year()+1)

def get_filing_periods():
    return [(year, quarter) for year in past_years() for quarter in range(1, 5)]

def get_url_content(url):
    print(f'getting {url}...')
    return requests.get(url).content

def write_zip_file(data_path=None, url_content=None):
    with zipfile.ZipFile(io.BytesIO(url_content)) as zip_file:
        for file in zip_file.namelist():
            local_file = data_path / file
            if local_file.exists():
                continue
            with local_file.open('wb') as output:
                for line in zip_file.open(file).readlines():
                    output.write(line)

def create_zip_file(data_path=None, url_content=None):
    try:
        write_zip_file(
            data_path=data_path,
            url_content=url_content
        )
    except zipfile.BadZipFile as error:
        print(error)

def get_data(data_path=None, url=None):
    for (year, quarter) in get_filing_periods():
        filename = f'{year}q{quarter}'
        path = data_path / filename / 'source'
        create_directory(path)
        create_zip_file(
            data_path=path,
            url_content=get_url_content(f'{url}{filename}_notes.zip')
        )

def write_parquet_file(source=None, destination=None):
    try:
        dataframe = pandas.read_csv(
            source,
            sep='\t',
            encoding='latin1',
            low_memory=False,
        )
    except Exception as error:
        print(f'{source} FAILED: {error}')
    else:
        dataframe.to_parquet(destination)

def convert_text_to_parquet(data_path):
    for source in data_path.glob('**/*.tsv'):
        filename = source.stem + '.parquet'
        path = pathlib.Path(source.parents[1]) / 'parquet'
        create_directory(path)
        destination = path / filename
        if destination.exists():
            continue
        write_parquet_file(
            source=source,
            destination=destination
        )

def get_submission(data_path=None, year=None, quarter=None):
    return pandas.read_parquet(data_path / f'{year}q{quarter}' / 'parquet' / 'sub.parquet')

def get_companies(submission):
    return submission.name.values

def get_company_submission(name=None, submission=None):
    return submission[submission.name == name].T.dropna().squeeze()

def get_filings(data_path=None, cik=None):
    result = pandas.DataFrame()
    for submission in data_path.glob('**/sub.parquet'):
        submission = pandas.read_parquet(submission)
        company_submission = submission[
            (submission.cik.astype(int) == cik) &
            (submission.form.isin(['10-Q', '10-K']))
        ]
        result = pandas.concat([result, company_submission])
    return result

def get_numbers(data_path=None, submission=None, dataframe=None):
    for num in data_path.glob('**/num.parquet'):
        num = pandas.read_parquet(num).drop('dimh', axis=1)
        numbers = num[num.adsh.isin(submission.adsh)]
        dataframe = pandas.concat([dataframe, numbers])
    return dataframe

def get_numerical_filing(data_path=None, submission=None, cik=None):
    # how can we speed this up?
    dataframe = pandas.DataFrame()
    dataframe = get_numbers(data_path=data_path, submission=submission, dataframe=dataframe)
    dataframe.ddate = pandas.to_datetime(dataframe.ddate, format='%Y%m%d')
    dataframe.to_parquet(data_path / f'{submission.cik[0]}_nums.parquet')
    return dataframe

def get_eps_after_split(dataframe=None, split_date=None, stock_split=None):
    split_date = pandas.to_datetime(split_date)
    dataframe = dataframe.groupby('adsh').apply(lambda x: x.nlargest(n=1, columns=['ddate']))
    dataframe.loc[dataframe.ddate < split_date,'value'] = dataframe.loc[dataframe.ddate < split_date, 'value'].div(stock_split)
    return dataframe

def get_eps_quarters(dataframe):
    return dataframe[
        (dataframe.tag == 'EarningsPerShareDiluted') & (dataframe.qtrs == 1)
    ].drop('tag', axis=1)

def get_eps(dataframe):
    series = dataframe.groupby('adsh').apply(lambda x: x.nlargest(n=1, columns=['ddate']))
    series = series[['ddate', 'value']].set_index('ddate').squeeze().sort_index()
    series = series.rolling(4,min_periods=4).sum().dropna()
    return series

def plot_eps(series):
    series.plot(lw=2, figsize=(14, 6), title='EPS')
    matplotlib.pyplot.xlabel('')
    matplotlib.pyplot.savefig('diluted eps')

def get_prices(ticker=None, start=None, end=None):
    return pandas_datareader.data.DataReader(ticker, 'yahoo', start=start, end=end)['Adj Close']

def get_values(dataframe=None, tag=None):
    dataframe[dataframe.tag == tag].drop('tag', axis=1)
    series = dataframe.groupby('adsh').apply(lambda x: x.nlargest(n=1, columns=['ddate']))
    series = series[['ddate', 'value']].set_index('ddate').squeeze().sort_index()
    series = series.rolling(4,min_periods=4).sum().dropna()
    return series

def plot(series=None, title=None):
    return series.plot(lw=2, figsize=(14,3), title=title)




# download_financial_statements
# get_company_names
# for company in get_company_names build company_dataframe and write to file