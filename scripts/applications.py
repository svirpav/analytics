from scripts import toolbox
from scripts import menu
import csv


class Salespart:

    def __init__(self):
        self.menu = menu.Menu()

    def app(self, file):
        
        # Create menu list with key['Sales Part No', 'Sales Parts Description']
        parts_list = self.__create_parts_list(file)

        # Call the menu and get sellected items
        selected_parts = self.menu.checkbox_menu(parts_list)

        # Return selected items as list
        selected_parts_list = self.__create_list_from_selected(selected_parts)

        # Create data row list
        columns = toolbox.get_data_rows(file)
        selected_colums = self.menu.checkbox_menu(columns)
        selcted_columns_list = self.__create_list_from_selected(selected_colums)

        # Created data structure with sellected items
        data = self.__create_data_st(file, selected_parts_list,
                                     selcted_columns_list)

        # Prepare data
        for sub_data in data:
           st_data =  self.__data_sort_by_year_month(sub_data, selcted_columns_list)
           for y in st_data:
               for m in st_data[y]:
                    print(y, m)
        print(st_data['2019']['08'])

    def __create_parts_list(self, file):
        key = 'Sales Part No'
        des = 'Sales Part Description'
        part = []
        description = []
        selection = []
        with open(file, encoding='unicode-escape', newline='') as f:
            data = csv.DictReader(f)
            for row in data:
                name = row[key]
                dsc = row[des]
                if name not in part:
                    part.append(name)
                    description.append(dsc)
        f.close()
        selection = toolbox.concat_array_str(part, description)
        return selection
    
    def __create_list_from_selected(self, selections):
        selected_list = []
        for i in selections:
            for k in selections[i]:
                tmp = toolbox.get_part_string(k, ':')
                selected_list.append(tmp)
        return selected_list

    def __create_data_st(self, file, selected_parts, selected_colums):
        data_st = []
        key = 'Sales Part No'
        for item in selected_parts:
            d = []
            a = {item: d}
            with open(file, encoding='unicode-escape', newline='') as f:
                data = csv.DictReader(f)
                for row in data:
                    if(item == row[key]):
                        tmp = []
                        for col in selected_colums:
                            tmp.append(row[col])
                        a[item].append(tmp)
            f.close()
            data_st.append(a)
        return data_st
  
    def __data_sort_by_year_month(self, data, selected_column_list):
        column_list = selected_column_list
        confirmed_date = 'Confirmed Date'
        created_date = 'Created'
        promised_date = 'Promised Delivery Date/Time'
        last_ship_date = 'Last Actual Ship Date'
        if created_date in column_list:
            date_index = column_list.index(created_date)
        elif confirmed_date in column_list:
            date_index = column_list.index(confirmed_date)
        elif promised_date in column_list:
            date_index = column_list.index(promised_date)
        elif last_ship_date in column_list:
            date_index = column_list.index(last_ship_date)
        else:
            print('Date column is not found in the data EXIT')
            exit(0)
        data_st = dict()
        for name in data:
            data_year = self.__data_sort_by_year(data[name], date_index)
            data_st = data_year
            for year in data_year:
                data_month = self.__data_sort_by_month(data_year[year], date_index, year)
                data_st[year] = data_month
        return data_st
    
    def __data_sort_by_year(self, data, date_index):
        y = dict()
        for sub_data in data:
            year = toolbox.get_year(sub_data[date_index])
            if year in y:
                y[year].append(sub_data)
            else:
                y[year] = []
                y[year].append(sub_data)
        return y
    
    def __data_sort_by_month(self, data, date_index, year):
        m = dict()
        for sub_data in data:
            month = toolbox.get_month(sub_data[date_index])
            if month in m:
                m[month].append(sub_data)
            else:
                m[month] = []
                m[month].append(sub_data)
        return m