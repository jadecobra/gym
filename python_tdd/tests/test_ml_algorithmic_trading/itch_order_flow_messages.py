import collections
import datetime
import gzip
from re import M
import matplotlib
import pathlib
import pandas
import seaborn
import shutil
import struct
import time
import urllib.request
import urllib.parse
import warnings

warnings.filterwarnings('ignore')

def convert_timestamp(timestamp):
    return divmod(timestamp, 60)

def format_time(timestamp):
    '''Return formatted time string 'HH:MM:SS'
    based on a numeric time() value
    '''
    minutes, seconds = convert_timestamp(timestamp)
    hours, minutes = convert_timestamp(minutes)
    return f'{hours:0>2.0f}:{minutes:0>2.0f}:{seconds:0>5.2f}'

def create_directory(data_path):
    if not data_path.exists():
        print(f'creating directory for {data_path}...')
        data_path.mkdir()

def download_data(url=None, filename=None):
    if not filename.exists():
        print(f'downloading {url}...')
        urllib.request.urlretrieve(url, filename)

def unzip_data(filename=None, unzipped=None):
    if not unzipped.exists():
        print(f'Unzipping to {unzipped}...')
        with (
            gzip.open(str(filename), 'rb') as input_file,
            open(unzipped, 'wb') as output_file,
        ):
            shutil.copyfileobj(input_file, output_file)
    return unzipped

def event_codes():
    return {
        'O': 'Start of Messages',
        'S': 'Start of System Hours',
        'Q': 'Start of Market Hours',
        'M': 'End of Market Hours',
        'E': 'End of System Hours',
        'C': 'End of Messages'
    }

def encoding():
    return {
        'primary_market_maker': {'Y': 1, 'N': 0},
        'printable': {'Y': 1, 'N': 0},
        'buy_sell_indicator': {'B': 1, 'S': -1},
        'cross_type': {'O': 0, 'C': 1, 'H': 2},
        'imbalance_direction': {'B': 0, 'S': 1, 'N': 0, 'O': -1}
    }

def formats():
    return {
        ('integer', 2): 'H', # int of length 2 => format string 'H'
        ('integer', 4): 'I',
        ('integer', 6): '6s', # int of length 6 => parse as string, convert later
        ('integer', 8): 'Q',
        ('alpha', 1): 's',
        ('alpha', 2): '2s',
        ('alpha', 4): '4s',
        ('alpha', 8): '8s',
        ('price_4', 4): 'I',
        ('price_8', 8): 'Q',
    }

def get_message_data(filename):
    return pandas.read_excel(
        filename,
        sheet_name='messages',
    ).sort_values(
        'id'
    ).drop(
        'id', axis=1
    )
