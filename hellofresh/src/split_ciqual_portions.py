import csv
import re

def split_csv_portions(file_path, output_file_path):
    with open(file_path, 'r') as file, open(output_file_path, 'w', newline='') as output_file:
        reader = csv.reader(file)
        next(reader, None)

        writer = csv.writer(output_file)
        writer.writerow(['id', 'name', 'portion', 'quantity', 'unit'])
        for row in reader:
            id, alim_now_fr, portions, quantities = row
            portions_list = portions.split(',')
            quantities_list = quantities.split(',')

            for i in range(0, len(portions_list)):
                name = alim_now_fr
                portion = portions_list[i].strip().capitalize()
                quantity = re.findall(r'\d+', quantities_list[i])[0]
                unit = re.sub(r'\d+', '', quantities_list[i]).strip()
                 
                new_row = [id, name, portion, quantity, unit]
                writer.writerow(new_row)

input = '/home/adrien/git/flavor_forest/hellofresh/src/ciqual_portions_wrk.csv'
output = '/home/adrien/git/flavor_forest/hellofresh/src/ciqual_portions_output.csv'

split_csv_portions(input, output)

#4