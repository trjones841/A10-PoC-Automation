#!/usr/bin/python3

import pandas as pd
#import numpy as np

pd.options.display.max_rows = 550  # default was 60
print('max_rows: ', pd.options.display.max_rows)

pd.options.display.max_columns = 80  # default was 20
print('max_columns: ', pd.options.display.max_columns)
pd.set_option('expand_frame_repr', False)  # Don't wrap data frames

# pd.options.mode.chained_assignment = None  # default='warn'


def get_server_data():
    server_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Servers')
    return server_data.head(10)

def get_vip_data():
    vip_data = pd.read_excel('A10_PoC_Data.xlsm', header=[0], sheet_name='Virtual-Servers')
    return vip_data.head(10)


if __name__ == "__main__":

    print('\n')
    print(get_server_data())
    print('\n')
    print(get_vip_data())