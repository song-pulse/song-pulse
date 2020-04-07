import pandas as pd
import csv
from collections import defaultdict
import matplotlib.pyplot as plt


def load_file(path_to_file, filename):
    df = pd.read_csv(path_to_file + filename)
    return df


def extract_csv_info(file):
    columns = defaultdict(list)  # each value in each column is appended to a list
    with open(file) as f:
        reader = csv.DictReader(f)  # read rows into dictionary format
        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            for (k, v) in row.items():  # go over each column name and value
                columns[k].append(v)  # append the value into appropriate list based on column name k
    print('columns', columns)
    return columns


if __name__ == "__main__":
    path_to_file = '/home/anjak/Dokumente/UZH/Masterproject/testdata/'
    filename = 'Activities.csv'
    activities = load_file(path_to_file=path_to_file, filename=filename)
    HR_data = load_file(path_to_file='/home/anjak/Dokumente/UZH/Masterproject/testdata/1579246202_A025CB/',
                        filename='HR.csv')
    EDA_data = load_file(path_to_file='/home/anjak/Dokumente/UZH/Masterproject/testdata/1579246202_A025CB/',
                         filename='EDA.csv')

    file_to_extract_csv_info = '/home/anjak/Dokumente/UZH/Masterproject/testdata/Activities.csv'
    colname = 'Title'
    columns = extract_csv_info(file_to_extract_csv_info)
    colnameData = columns[colname]
    print('Activities Title column', colnameData)
    print('activities', activities)
    print('HR Data', HR_data)
    print('EDA Data', EDA_data)
