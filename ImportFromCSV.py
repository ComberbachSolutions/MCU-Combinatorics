import csv
import json



def csv_file_to_dict(filepath, delimiter=',', encoding='utf-8-sig'):  # Adjusted encoding
    nested_dict = {}
    with open(filepath, 'r', newline='', encoding=encoding) as file:  # Specified encoding
        reader = csv.reader(file, delimiter=delimiter)
        for row in reader:
            # Process row to handle potential issues with the first item
            if row:  # Ensure row is not empty
                row[0] = row[0].lstrip('\ufeff')  # Strip BOM if present
                keys = row
                temp = nested_dict
                for key in keys[:-1]:
                    if key not in temp:
                        temp[key] = {}
                    temp = temp[key]
                temp[keys[-1]] = ''
    return nested_dict

def write_dict_to_file(dict_data, filename):
    with open(filename, 'w') as file:
        json.dump(dict_data, file)

def read_dict_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    nested_dict_result = csv_file_to_dict('RA6M3 LQFP176 Pinout.csv')
    print(nested_dict_result)

    for Name, Functions in nested_dict_result.items():
        print(Name, end="")
        for Function in Functions.items():
            print(f"\t{Function}")

    write_dict_to_file(nested_dict_result, 'RA6M3 LQFP176 Pinout.JSON')