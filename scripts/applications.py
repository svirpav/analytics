from scripts import toolbox
from scripts import menu
from scripts import dataplot
# from scripts import csvhandler
import pandas as pd


class Analytics:

    def __init__(self):
        self.menu = menu.Menu()
        self.plot = dataplot.Plot()

    def app(self, file):
        # Read CSV and create Pandas data frame
        data = pd.read_csv(file, encoding='unicode-escape')

        # Create Year and Month column
        dates = data['Act. Del. Date']
        year, month = self.__return_month_year(dates)
        data['Year'] = pd.Series(year)
        data['Month'] = pd.Series(month)

        # Group By Year
        grp_year_bl = data.groupby(['Year', 'Business Line'])
        year_bl_dict = self.__prepare_data(grp_year_bl)
        bl_units = self.__find_bl_units(data['Business Line'])
        self.plot.plot_gross_sales_bl(year_bl_dict, bl_units)

    def __return_month_year(self, dates):
        list_year = []
        list_month = []
        for k, i in enumerate(dates):
            i = self.__return_latest_date(i, ' ')
            year = toolbox.get_year(i)
            month = toolbox.get_month(i)
            list_year.append(year)
            list_month.append(month)
        return list_year, list_month

    def __return_latest_date(self, string, sep):
        spl = string.split(sep)
        if toolbox.is_date(spl[-1]):
            return spl[-1]
        else:
            return spl[0]

    def __prepare_data(self, data):
        data_dict = dict()
        for name, group in data:
            if name[0] not in data_dict:
                data_dict[name[0]] = {}
                data_dict[name[0]][name[1]] = group['Sales EUR'].sum()
            else:
                data_dict[name[0]][name[1]] = group['Sales EUR'].sum()
        return data_dict

    def __find_bl_units(self, data):
        bl_units = dict()
        for unit in data:
            if unit not in bl_units:
                bl_units[unit] = []
        return bl_units


'''Using Pandas.'''


class Application:

    def __init__(self):
        self.menu = menu.Menu()
        self.plot = dataplot.Plot()

    def app(self, file):
        # Read CSV file
        inital_data = pd.read_csv(file, encoding='unicode-escape')
        data_copy = inital_data

        # Create Month and Yea column
        year, month = self.__create_year_month_col(data_copy)
        data_copy['Year'] = pd.Series(year)
        data_copy['Month'] = pd.Series(month)

        self.__remove_internal_lines(data_copy)

        part_year_group = data_copy.groupby(['Sales Part No', 'Year'])
        '''
        x = dict()
        for name, group in part_year_group:
            if name[1] in x:
                if name[0] in x[name[1]]:
                    x[name[1]][name[0]] += group['Sales Qty'].sum()
                else:
                    x[name[1]][name[0]] = group['Sales Qty'].sum()
            else:
                x[name[1]] = {}
                x[name[1]][name[0]] = group['Sales Qty'].sum()
        years = []
        for year in x:
            years.append(year)
        years.sort() '''
        # self.plot.plot_by_year(x, years)
        print('Group by Yaer')
        y = dict()
        for name, group in part_year_group:
            if name[1] in y:
                y[name[1]][name[0]] = [group['Sales Qty'].sum(),
                                       group['Gross Amt/Base'].sum()]
            else:
                y[name[1]] = {}
                y[name[1]][name[0]] = [group['Sales Qty'].sum(),
                                       group['Gross Amt/Base'].sum()]
        years = []
        for year in y:
            years.append(year)
        years = years.sort()
        self.plot.plot_qty_vs_gross(y, years)

    def __create_year_month_col(self, data):
        a = data['Created']
        list_year = []
        list_month = []
        for i in a:
            year = toolbox.get_year(i)
            month = toolbox.get_month(i)
            list_year.append(year)
            list_month.append(month)
        return list_year, list_month

    def __remove_internal_lines(self, data):
        for row_index, row in data.iterrows():
            if '*' in row['Order No']:
                data.drop(row_index)


'''Supplier Analytics.'''


class Supplier:

    def __init__(self):
        self.menu = menu.Menu()
        self.plot = dataplot.Plot()

    def app(self, file):
        inital_data = pd.read_csv(file, encoding='unicode-escape')
        data_copy = inital_data

        # Create Month and Yea column
        dates = data_copy['Created']
        year, month = toolbox.date_to_year_month_lst(dates)
        data_copy['Year'] = pd.Series(year)
        data_copy['Month'] = pd.Series(month)

        df = pd.DataFrame()
        int_list = ['Year', 'Site', 'Supplier', 'Sales Qty', 'Total Cost Eur']
        for item in int_list:
            df[item] = data_copy[item]

        # Refactor supplier column
        a = df['Supplier']
        a = self.__refactor_supplier(a)
        df['Supplier'] = pd.Series(a)

        # Refactor Total Cost Eur

        a = df['Total Cost Eur']
        a = self.__refactor_num_st_to_int(a)
        df['Total Cost Eur'] = pd.Series(a)

        # group by YEAR
        grp_year_site_sup = df.groupby(['Year', 'Site', 'Supplier'])

        # Create data Year Site, supplier -> Qty
        year_stie_sup_qty = self.__df_year_site(grp_year_site_sup, 'Sales Qty')

        for year in year_stie_sup_qty:
            self.plot.site_supplier_qty_pie(year_stie_sup_qty[year], year)

        # Create data Year Site, supplier -> gross cost
        year_site_sup_cost = self.__df_year_site(grp_year_site_sup,
                                                 'Total Cost Eur')
        # print(year_site_sup_cost)

    def __refactor_supplier(self, column):
        a = column
        ref_list = []
        in_sup_list = [21, 22, 31, 35, 56, 60, 64]
        # 21;22;31;35;56;60;64
        for i in a:
            if i not in in_sup_list:
                ref_list.append('EXT')
            else:
                ref_list.append(str(int(i)))
        return ref_list

    def __df_year_site(self, data, key):
        year_site_qty = dict()
        for name, group in data:
            if name[0] in year_site_qty:
                if name[1] in year_site_qty[name[0]]:
                    sup = dict()
                    sup[name[2]] = int(group[key].sum())
                    year_site_qty[name[0]][name[1]].append(sup)
                else:
                    year_site_qty[name[0]][name[1]] = []
                    sup = dict()
                    sup[name[2]] = int(group[key].sum())
                    year_site_qty[name[0]][name[1]].append(sup)
            else:
                year_site_qty[name[0]] = {}
                year_site_qty[name[0]][name[1]] = []
                sup = dict()
                sup[name[2]] = int(group[key].sum())
                year_site_qty[name[0]][name[1]].append(sup)
        return year_site_qty

    def __refactor_num_st_to_int(self, data):
        col = []
        for i in data:
            try:
                x = float(i)
                x = int(x)
                col.append(x)
            except ValueError as ve:
                var = i.split(',')
                tmp = int(var[0])
                tmp = tmp * 1000
                x = tmp + float(var[1])
                x = int(x)
                col.append(x)
        return col

