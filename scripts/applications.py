from scripts import toolbox
from scripts import menu
from scripts import dataplot
from scripts import csvhandler


class Analytics:

    def __init__(self):
        self.menu = menu.Menu()
        self.plot = dataplot.Plot()
        self.csvh = csvhandler.CSVReader()

    def app(self, file):
        # Create available column list
        column_list = self.csvh.get_column_list(file)

        # Create all available columns index dictionary
        index_dict = self.__index_dict(column_list)

        # Open data file read and creade data list
        data_list = self.csvh.get_data_list(file)

        year_list = self.__years(data_list, index_dict['Created'])

        selected_years = self.menu.checkbox_menu(year_list)
        selected_years = self.__from_dict_to_list(selected_years)

        parts_qty = dict()
        for item in data_list:
            year = toolbox.get_year(item[index_dict['Created']])
            part = item[index_dict['Sales Part No']]
            qty = float(item[index_dict['Sales Qty']])
            if year in selected_years:
                if year in parts_qty:
                    if part in parts_qty[year]:
                        parts_qty[year][part] += qty
                    else:
                        parts_qty[year][part] = qty
                else:
                    parts_qty[year] = {}
                    parts_qty[year][part] = qty
        top_parts = self.plot.plot_by_year(parts_qty, selected_years)
        for year in top_parts:
            for item in top_parts[year]:
                for row in data_list:
                    if item in row[index_dict['Sales Part No']]:
                        pass

    # Class helper functions
    def __index_dict(self, data):
        index_dict = dict()
        for i in data:
            index_dict[i] = data.index(i)
        return index_dict

    def __years(self, data, ix):
        year_list = []
        for i in data:
            year = toolbox.get_year(i[ix])
            if year not in year_list:
                year_list.append(year)
        year_list = sorted(year_list)
        return year_list

    def __from_dict_to_list(self, selections):
        selected_list = []
        for i in selections:
            for k in selections[i]:
                tmp = toolbox.get_part_string(k, ':')
                selected_list.append(tmp)
        return selected_list
