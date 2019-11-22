import sys
import csv
import datetime
import math


def version_check():
    return sys.version()


'''Date Helpers.'''


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


def str_to_date(value):
    if(is_date_and_time(value)):
        date_obj = datetime.datetime.strptime(value, '%m/%d/%Y %H:%M')
    else:
        date_obj = datetime.datetime.strptime(value, '%m/%d/%Y')
    return date_obj.date()


''' Numeric Helpers.'''


def is_number(value):
    try:
        float(value)
        return True
    except ValueError as ve:
        print(ve)
        return False


def str_to_num(value):
    a = value
    try:
        return float(a)
    except ValueError as i:
        print(i)
        return value


'''String Helprs.'''


def get_part_string(string, sep):
    spl = string.split(sep)
    return spl[0]


'''List Helpers.'''


def concat_array_str(array_1, array_2):
    array = []
    separator = ':  '
    if(len(array_1) == len(array_2)):
        size = len(array_1)
        for i in range(size):
            tmp = array_1[i] + separator + array_2[i]
            array.append(tmp)
    return array


def find_closest(array, value):
    for i, k in enumerate(array):
        if value > k:
            return i


''' CSV Helpers.'''


def get_data_rows(file):
    col = []
    with open(file, newline='', encoding='unicode-escape') as f:
        data = csv.reader(f)
        for row in data:
            col = row
            break
    f.close()
    return col


def format_data_array(data):
    tmp = data
    for i, k in enumerate(data):
        if(is_number(k)):
            tmp[i] = str_to_num(k)
        elif(is_date(k)):
            tmp[i] = str_to_date(k)
    return tmp


'''Sorting Helpers.'''


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


def merge_sort(keys, values, start, end):
    if(start < end):
        mid = start + math.floor((end - start) / 2)
        merge_sort(keys, values, start, mid)
        merge_sort(keys, values, mid+1, end)
        __merge_list(keys, values, start, mid, end)
        return keys, values


def __merge_list(keys, values, start, mid, end):
    k = start
    i = 0
    j = 0
    low = values[start:mid+1]
    high = values[mid+1:end+1]
    k_low = keys[start:mid+1]
    k_high = keys[mid+1:end+1]
    # print(low, high)
    while(i <= mid-start and j < end-mid):
        # print('comparing', low[i], high[j])
        if(low[i] <= high[j]):
            # print('inserting low', low[i])
            values[k] = low[i]
            keys[k] = k_low[i]
            # print(array)
            k += 1
            i += 1
        else:
            # print('inserting high', high[j])
            values[k] = high[j]
            keys[k] = k_high[j]
            # print(array)
            k += 1
            j += 1
    while(i < len(low)):
        # print('Inserting left low', low[i])
        values[k] = low[i]
        keys[k] = k_low[i]
        # print(array)
        k += 1
        i += 1
    while(j < len(high)):
        # print('Inserting left high', high[j])
        values[k] = high[j]
        keys[k] = k_high[j]
        # print(array)
        k += 1
        j += 1

    return keys, values
