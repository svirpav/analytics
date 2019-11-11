from scripts import toolbox
from scripts import menu
import csv


class Salespart:

    def __init__(self):
        self.menu = menu.Menu()

    def app(self, file):
        
        # Create menu list with key['Sales Part No', 'Sales Parts Description']
        parts_list = self.create_parts_list(file)

        # Call the menu and get sellected items
        selected_parts = self.menu.checkbox_menu(parts_list)

        # Return selected items as list
        selected_parts_list = self.create_list_from_selected(selected_parts)

        # Create data row list
        columns = toolbox.get_data_rows(file)
        selected_colums = self.menu.checkbox_menu(columns)
        selcted_columns_list = self.create_list_from_selected(selected_colums)

        # Created data structure with sellected items
        data = self.create_data_st(file, selected_parts_list,
                                   selcted_columns_list)

        # Prepare data and plot data
        for sub_data in data:
            self.data_handler(sub_data, selcted_columns_list)

    def create_parts_list(self, file):
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
    
    def create_list_from_selected(self, selections):
        selected_list = []
        for i in selections:
            for k in selections[i]:
                tmp = toolbox.get_part_string(k, ':')
                selected_list.append(tmp)
        return selected_list

    def create_data_st(self, file, selected_parts, selected_colums):
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
  
    def data_handler(self, data, selected_column_list):
        for name in data:
            a = self.data_sort_by_year(data[name], selected_column_list)

    def data_sort_by_year(self, data, selected_column_list):
        for sub_data in data:
            for item in sub_data:
                print(toolbox.is_a_date(item))
                if toolbox.is_a_date(item):
                    year = toolbox.get_year(item)
                    print(year, sub_data)