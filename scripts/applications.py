from scripts import toolbox
from scripts import menu
from scripts import dataplot
import pandas as pd


class Analytics:

    def __init__(self):
        self.menu = menu.Menu()
        self.plot = dataplot.Plot()

    def app(self, file):
        # Read CSV and create Pandas data frame
        data = pd.read_csv(file, encoding='unicode-escape')

        # Create data selection
        selections = ['Order No',
                      'Order Type',
                      'Supply Code',
                      'Sales Part Type',
                      'Sales Part No',
                      'Sales Qty',
                      'Customer No',
                      'Site',
                      'Supplier',
                      'Cust Stat Grp',
                      'Created',
                      'Confirmed Date',
                      'Eur Value',
                      'Total Cost Eur',
                      'SalesGroup',
                      'Price/Curr',
                      'Gross Amt/Curr',
                      'Currency',
                      'Cost',
                      'Total Cost/Base',
                      'Promised Delivery Date/Time',
                      'Planned Delivery Date/Time',
                      'Planned Due Date',
                      'First Actual Ship Date',
                      'Last Actual Ship Date',
                      'Region Code',
                      'Order Ref 1',
                      'Project ID',
                      'Project Name',
                      'Cost Cent',
                      'BusinessLi',
                      'Counterpar',
                      'Customs Stat No']

        # Create new data frame
        selected_data = pd.DataFrame()
        for selection in selections:
            col = []
            col = data[selection]
            selected_data[selection] = pd.Series(col)

        # Remove all internal orders
        indexIntern = selected_data[(selected_data['Order Type'] == 'INT') |
                                    (selected_data['Order Type'] == 'WAR')
                                    ].index
        selected_data.drop(indexIntern, inplace=True)
        selected_data.reset_index(drop=True, inplace=True)

        # Create Month and Yea column
        date = selected_data['Created']
        year, month = toolbox.date_to_year_month_lst(date)
        selected_data['Year'] = pd.Series(year)
        selected_data['Month'] = pd.Series(month)

        # Refacto Total Cost Eur and Eur Value to INT
        selected_data['Total Cost Eur'] =\
            toolbox.value_to_int(selected_data['Total Cost Eur'])
        selected_data['Eur Value'] =\
            toolbox.value_to_int(selected_data['Eur Value'])
        print(selected_data['Eur Value'])


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
        print(year_site_sup_cost)

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
            except ValueError:
                var = i.split(',')
                tmp = int(var[0])
                tmp = tmp * 1000
                x = tmp + float(var[1])
                x = int(x)
                col.append(x)
        return col
