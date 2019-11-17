import sys
import csv
import datetime
from datetime import date


def version_check():
    return sys.version()


def is_date(date_string):
    if(is_date_and_time(date_string)):
        return True
    else:
        try:
            datetime.datetime.strptime(date_string, '%m/%d/%Y')
            return True
        except ValueError:
            return False


def is_date_and_time(date_string):
    try:
        datetime.datetime.strptime(date_string, '%m/%d/%Y   %H:%M')
        return True
    except ValueError:
        return False


def is_number(value):
    try:
        float(value)
        return True
    except ValueError as ve:
        return False


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


def get_data_rows(file):
    col = []
    with open(file, newline='', encoding='unicode-escape') as f:
        data = csv.reader(f)
        for row in data:
            col = row
            break
    f.close()
    return col


def get_year(date_string):
    if(is_date_and_time(date_string)):
        date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M')
        year = date_obj.strftime('%Y')
        return str(year)
    else:
        date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y')
        year = date_obj.strftime('%Y')
        return str(year)


def get_month(date_string):
    if(is_date_and_time(date_string)):
        date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M')
        month = date_obj.strftime('%m')
        return str(month)
    else:
        date_obj = datetime.datetime.strptime(date_string, '%m/%d/%Y')
        month = date_obj.strftime('%m')
        return str(month)


def format_data_array(data):
    tmp = data
    for i, k in enumerate(data):
        if(is_number(k)):
            tmp[i] = str_to_num(k)
        elif(is_date(k)):
            tmp[i] = str_to_date(k)
    return tmp


def str_to_num(value):
    a = value
    try:
        return float(a)
    except ValueError as i:
        return value


def str_to_date(value):
    if(is_date_and_time(value)):
        date_obj = datetime.datetime.strptime(value, '%m/%d/%Y %H:%M')
    else:
        date_obj = datetime.datetime.strptime(value, '%m/%d/%Y')
    return date_obj.date()

def sort(x, y):
    a = x
    b = y
    for i, k in enumerate(a):
        index = __find_smalest(a, i)
        a, b = __swap(a, b, i, index)
    return a, b

def __find_smalest(x, startIndex):
    minIndex = startIndex
    minValue = x[startIndex]
    for i in range(startIndex, len(x)):
        if(x[i] < minValue):
            minIndex = i
            minValue = x[i]
    return minIndex

def __swap(x, y, index_1, index_2):
    a = x
    b = y
    a[index_1], a[index_2] = a[index_2], a[index_1]
    b[index_1], b[index_2] = b[index_2], b[index_1]
    return a, b