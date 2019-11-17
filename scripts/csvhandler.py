import csv

class CSVReader:

    def get_column_list(self, file):
        with open(file, encoding='unicode-escape', newline='') as f:
            column_list = []
            data = csv.reader(f)
            for row in data:
                column_list = row
                break
        f.close()
        return column_list

    def get_data_list(self, file):
        data_list = []
        with open(file, encoding='unicode-escape', newline='') as f:
            data = csv.reader(f)
            for row in data:
                data_list.append(row)
        f.close()
        return data_list
