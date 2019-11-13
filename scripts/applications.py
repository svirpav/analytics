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
        selected_parts_list = self.__create_list(selected_parts)

        # Create data row list
        columns = toolbox.get_data_rows(file)
        selected_colums = self.menu.checkbox_menu(columns)
        selcted_columns_list = self.__create_list(selected_colums)

        # Created data structure with sellected items
        data_list = self.__create_data_st(file, selected_parts_list,
                                          selcted_columns_list)
   
        # Prepare data
        final_data = dict()
        for item in data_list:
           sorted_data_dict =  self.__data_sort_by_date(item, selcted_columns_list)
           for name in item:
               final_data[name] = sorted_data_dict

        print(final_data)
                   

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
    
    def __create_list(self, selections):
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
  
    def __data_sort_by_date(self, data, selected_column_list):
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
        for item in data:
            sorted_data = self.__sort_data(data[item], date_index)
        return sorted_data
    

    def __sort_data(slef, data, date_index):
        y = dict()
        for i in data:
            year = toolbox.get_year(i[date_index])
            month = toolbox.get_month(i[date_index])
            formated_data = toolbox.format_data_array(i)
            if year in y:
                if month in y[year]:
                    y[year][month].append(formated_data)
                else:
                    y[year][month] = []
                    y[year][month].append(formated_data)
            else:
                y[year] = {}
                y[year][month] = []
                y[year][month].append(formated_data)
        return y