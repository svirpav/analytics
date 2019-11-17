import matplotlib.pyplot as plt
from scripts import toolbox


class Partplot:

    # Create data vectors for ploting
    def plot_data(self, data_st, selected_columns_list, parts):
        for name in data_st:
            if name in parts:
                for year in data_st[name]:
                    plot_data = dict()
                    for month in data_st[name][year]:
                        sales_qty_sum = self.__sum_qty(data_st[name][year][month], selected_columns_list)
                        plot_data[int(month)] = sales_qty_sum
                    x = list(plot_data.keys())
                    y = list(plot_data.values())
                    print(x, y)
                    x, y = toolbox.sort(x, y)
                    print(x, y)
                    plt.scatter(x, y, label=year)
                    plt.legend()
                plt.show()



    def __sum_qty(self, data, selected_columns_list):
        key = 'Sales Qty'
        i = selected_columns_list.index(key)
        value = 0
        for k in data:
            value += k[i]
        return value
