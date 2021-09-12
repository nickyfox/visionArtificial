import csv
import glob


def write_file(label, writer):
    files = glob.glob('./util/shapes/' + label + '/*')  # label recibe el nombre de la carpeta
    for file in files:

        writer.writerow([label, file])


def generate_supervision_file():
    with open('util/csv/supervision.csv', 'w', newline='') as file:  # Se genera un archivo nuevo (W=Write)
        writer = csv.writer(file)
        write_file("1", writer)
        write_file("2", writer)
        write_file("3", writer)


generate_supervision_file()