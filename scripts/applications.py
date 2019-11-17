from scripts import toolbox
from scripts import menu
from scripts import dataplot
from scripts import csvhandler
import csv


class Salespart:

    def __init__(self):
        self.menu = menu.Menu()
        self.plot = dataplot.Partplot()

    def app(self, file):
        
        # Create menu list with key['Sales Part No', 'Sales Parts Description']
        parts_list = self.__create_parts_list(file)
        sorted_parts_list = sorted(parts_list)

        # Call the menu and get sellected items
        selected_parts = self.menu.checkbox_menu(sorted_parts_list)

        # Return selected items as list
        selected_parts_list = self.__create_list(selected_parts)

        # Create data row list
        columns = toolbox.get_data_rows(file)
        selected_colums = self.menu.checkbox_menu(columns)
        selected_columns_list = self.__create_list(selected_colums)

        # Created data structure with sellected items
        data_list = self.__create_data_st(file, selected_parts_list,
                                          selected_columns_list)
   
        # Prepare data
        final_data = dict()
        for item in data_list:
           sorted_data_dict =  self.__data_sort_by_date(item, selected_columns_list)
           for name in item:
               final_data[name] = sorted_data_dict
        
        # Show parts with structured data select parts and ploting options
        plot_list = []
        for item in final_data:
            plot_list.append(item) 
        plot_list.append('exit')

        while (True):
            plot_selected = self.menu.checkbox_menu(plot_list)
            plot_selected_list = self.__create_list(plot_selected)
            if 'exit' not in plot_selected_list:
                self.plot.plot_data(final_data, selected_columns_list, plot_selected_list)
            else:
                print('You have selected exit')
                exit(0)



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
    
    # Create ploting options
    def __create_plot_options(self, selected_column_list):
        order_nr = 'Order No'
        sales_part = 'Sales Part No'
        sales_qty = 'Sales Qty'
        customer_no = 'Customer No'
        promised_date = 'Promised Delivery Date/Time'
        last_ship_date = 'Last Actual Ship Date'
        gross_amt = 'Gross Amt/Curr'
        cost = 'Total Cost/Base'
        created_date = 'Created'
        confirmed_date = 'Confirmed Date'
        plot_options_list = []
        # 2D Plot Part Sales Qty -> Y Created Date -> X
        if(sales_qty in selected_column_list and created_date in selected_column_list):
            name = 'Sales Qty by Date'
            plot_options_list.append(name)
        # 2D Plot Delta(Created - Confirmed) -> Y : Created Date -> X
        if(confirmed_date in selected_column_list and created_date in selected_column_list):
            name = 'Delta Created vs Confimed'
            plot_options_list.append(name)
        else:
            print('No good data found for plot')
            exit(0)
        return plot_options_list

    def __index_plot_option(self, plot_option):
        options = ['Sales Qty by Date', 'Delta Created vs Confimed']
        return options.index(plot_option)


class Analytics:

    def __init__(self):
        self.menu = menu.Menu()
        self.plot = dataplot.Partplot()
        self.csvh = csvhandler.CSVReader()

    def app(self, file):
        # Create available column list
        column_list = self.csvh.get_column_list(file)
        index_dict = self.__index_dict(column_list)    
        data_list = self.csvh.get_data_list(file)

    def __index_dict(self, data):
        index_dict = dict()
        for i in data:
            index_dict[i] = data.index(i)
        return index_dict
                
    

