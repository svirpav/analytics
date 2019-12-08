import matplotlib.pyplot as plt
import math
import os
import statistics
import numpy as np
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
        dm = dict()
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
            x_mean = toolbox.find_closest(sorted_y, math.ceil(y_mean))
            ax.grid(linestyle='-')
            ax.plot(sorted_y)
            ax.plot(y_mean, x_mean, marker='x', color='r')
            ax.set(ylabel='Sales Qty', xlabel='Amount of parts sold')
            # self.__simple_analys(x, y, case)
            dt[case] = sorted_x[:x_mean]
            dm[case] = math.ceil(y_mean)
        self.__save_plot(fig, file)
        return dt, dm

    def plot_mean_parts(self, parts_year, mean_year):
        pass

    def plot_qty_vs_gross(self, data, years):
        name = 'Qty vs Gross Sales'
        col = len(years)
        rows = 2
        fig, axs = plt.subplots(rows, col, figsize=(35, 10))
        fig.suptitle(name)
        years += years
        axs = axs.flat
        k = len(years)
        qty_peak_dict = dict()
        for ax, case in zip(axs, years):
            y = []
            x = []
            if k > (len(years) / 2):
                title = str(case) + ' : Parts Qty Graph'
                ax.set_title(title)
                ax.grid()
                for part in data[case]:
                    y.append(data[case][part][0])
                    x.append(part)
                copy_y = y
                copy_x = x
                for i in range(len(copy_y)):
                    y_max = max(copy_y)
                    if y_max < 100:
                        break
                    max_index = copy_y.index(y_max)
                    if case not in qty_peak_dict:
                        qty_peak_dict[case] = {}
                        qty_peak_dict[case][copy_x.pop(max_index)] = copy_y.pop(max_index)
                    else:
                        qty_peak_dict[case][copy_x.pop(max_index)] = copy_y.pop(max_index)
                ax.plot(y)
                k = k - 1
            else:
                title = str(case) + ' : Parts Gross Sales Graph'
                ax.set_title(title)
                ax.grid()
                for part in data[case]:
                    y.append(data[case][part][1])
                ax.plot(y)
        self.__save_plot(fig, name)

    def plot_gross_sales_bl(self, data, bl_dict):
        x = []
        y = bl_dict
        fig, axs = plt.subplots()
        fig.suptitle('Gross Sales for BL')
        axs.grid()
        width = 0.1
        for year in data:
            x.append(year)
            for bl in data[year]:
                y[bl].append(int(data[year][bl]))
        x = np.arange(len(x))
        for i in y:
            if len(y[i]) < len(x):
                y[i].insert(0, 0)
        axs.bar(x-width/2, y['PRODUCTS'], width, label = 'PRODUCTS')
        axs.bar(x+width/2, y['EINO'], width, label = 'EINO')
        plt.show()

    def site_supplier_qty_pie(self, data, year):
        cols = 3
        sites = []
        for site in data:
            sites.append(site)
        rows = math.ceil(len(site) / 2)
        fig, axs = plt.subplots(rows, cols,
                                figsize=(18, 10),
                                subplot_kw=dict(aspect="equal"))
        axs = self.__axes_trim(axs, len(sites))
        fig.suptitle(year)
        for ax, site in zip(axs, sites):
            labels = []
            values = []
            explods = []
            for suppliers in data[site]:
                for supplier in suppliers:
                    labels.append(supplier)
                    values.append(suppliers[supplier])
                    explods.append(0.1)
            ax.set_title(site, pad=20)
            wedges, texts, autotexts = ax.pie(values, explode=explods,
                                              autopct='%1.1f%%',  # lambda pct: self.__func(pct, values)
                                              textprops=dict(color="b"),
                                              # labels=labels,
                                              radius=1.2)
            ax.legend(wedges, zip(labels, values),
                      title="Supliers",
                      loc="upper left",
                      bbox_to_anchor=(0.8, 1.3))  # 1, 0, 0.5, 1

            plt.setp(autotexts, size=8, weight="bold")
        plt.show()

    def __func(self, pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d} units)".format(pct, absolute)

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
