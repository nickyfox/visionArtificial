import csv

list_of_column_names = []


def read_labels():
    with open('util/csv/etiquetas.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            class_label = row.pop()
            list_of_column_names.append(class_label)


def get_label(number_label):
    position = number_label - 1
    return list_of_column_names[position]


def get_number_for_label(label):
    return list_of_column_names.index(label) + 1
