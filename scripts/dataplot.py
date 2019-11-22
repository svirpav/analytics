import matplotlib.pyplot as plt
import math
import os
import statistics
from pathlib import Path as path
from scripts import toolbox


class Plot:

    def __init__(self):
        home = str(path.home())
        directorie = 'plots'
        self.path = os.path.join(home, directorie)
        try:
            os.mkdir(self.path)
        except FileExistsError as fex:
            print(fex)

    # Plot by the year
    def plot_by_year(self, data, selected_years):
        name = 'Spareparts Qty sales peaks'
        file = 'qty_peaks.jpeg'
        dt = dict()
        cols = 3
        rows = math.ceil(len(selected_years) / cols)
        fig, axs = plt.subplots(rows, cols, figsize=(18, 12))
        fig.suptitle(name)
        axs = self.__axes_trim(axs, len(selected_years))
        for ax, case in zip(axs, selected_years):
            ax.set_title(str(case))
            x = list(data[case].keys())
            y = list(data[case].values())
            sorted_x, sorted_y = toolbox.merge_sort(x, y, 0, len(y)-1)
            sorted_x.reverse()
            sorted_y.reverse()
            y_mean = statistics.mean(sorted_y)
            x_mean = toolbox.find_closest(sorted_y, int(y_mean))
            ax.grid(linestyle='-')
            ax.plot(sorted_y)
            ax.plot(y_mean, x_mean, marker='x', color='r')
            ax.set(ylabel='Sales Qty', xlabel='Amount of parts sold')
            # self.__simple_analys(x, y, case)
            dt[case] = sorted_x[:x_mean]
        self.__save_plot(fig, file)
        return dt

    def plot_gross_sales(self, data):
        # file = 'gross_sales.jpg'
        name = 'Gross Sales'
        fig, ax = plt.subplots()
        fig.suptitle(name)
        x = list(data.keys())
        for year in data:
            y = list(data[year].values())
            ax.plot(x, y)
        plt.show()

    def __axes_trim(self, axs, N):
        axs = axs.flat
        for ax in axs[N:]:
            ax.remove()
        return axs[:N]

    def __save_plot(self, figure, name):
        file = os.path.join(self.path, name)
        figure.savefig(file, dpi=300)
        # plt.show(figure)
        plt.close(figure)
