import sys
import csv
import datetime

def get_part_string(string, sep):
    spl = string.split(sep)
    return spl[0]


def concat_array_str(array_1, array_2):
    array = []
    separator = ':  '
    if(len(array_1) == len(array_2)):
        size = len(array_1)
        for i in range(size):
            tmp = array_1[i] + separator + array_2[i]
            array.append(tmp)
    return array

def version_check():
    return sys.version()

def get_data_rows(file):
    col = []
    with open(file, newline='', encoding='unicode-escape') as f:
        data = csv.reader(f)
        for row in data:
            col = row
            break
    f.close()
    return col

def is_a_date(date_string):
    try:
        datetime.datetime.strptime(date_string, '%m/%d/%Y')
        return True
    except ValueError:
        return False
def get_year(date_string):
    date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y')
    year = date_obj.strftime('%Y')
    return str(year)