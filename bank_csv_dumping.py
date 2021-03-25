import re
import os
import csv
import argparse
import json
from glob import glob
from dateutil.parser import parse

def csv_file_identifier():
    '''To return csv list from directory.'''

    base_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(base_path, 'csv_repo', "*.csv")
    csv_file_list = glob(path)
    return csv_file_list


def date_converter(date):
    '''To return formated date.'''

    data = re.split(r"\s|-|/", date)
    try:
        if data[0].isdigit() and data[1].isdigit():
            if int(data[0]) < int(data[1]):
                return parse(date).strftime('%Y-%d-%m')
        return parse(date).strftime('%Y-%m-%d')
    except Exception as exc:
        print("Please check the date formate", exc)


def data_genrator(row):
    '''Return a data which is require to save in csv file.'''

    converted_euro = ""
    converted_cents = ""
    if row.get('amount', row.get('amounts', '')):
        converted_euro, converted_cents = row.get('amount', row.get('amounts','')).split('.')
    row_data = {
        'date':date_converter(row[list(row.keys())[0]]),
        'type':row.get('transaction', row.get('type', '')),
        'euro':row.get('euro', converted_euro),
        'cents':row.get('cents', converted_cents),
        'from':row.get('from', ''),
        'to':row.get('to', '')}
    return row_data


def write_consolidated_data_csv(csv_dump_for_bank):
    '''Generate consolidated csv file for bank statements.'''

    base_path = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(base_path, 'consolidated_bank_statement.csv')
    field_names = ['date', 'type', 'euro', 'cents', 'from', 'to']
    try:
        with open(file_name, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            for line in csv_dump_for_bank:
                writer.writerow(line)
        return file_name
    except Exception as exc:
        print('Some error in file generation please check', exc)
    return False

def get_consolidated_bank_statement():
    '''Get consolidated csv data from multiple csv file.'''

    csv_file_list = csv_file_identifier()
    csv_dump_for_bank = []
    if csv_file_list:
        for file in csv_file_list:
            with open(file) as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    csv_dump_for_bank.append(data_genrator(row))
    return csv_dump_for_bank


def csv_generator(csv_dump_for_bank):
    '''Generate consolidated json for csv dump.'''

    file_name = write_consolidated_data_csv(csv_dump_for_bank)
    if file_name:
        print(f'File generated at path {file_name}')
    else:
        print('File not generated properly please have a look')


def json_generator(csv_dump_for_bank):
    '''Generate consolidated json for csv dump.'''

    base_path = os.path.dirname(os.path.realpath(__file__))
    file_name = os.path.join(base_path, 'consolidated_bank_statement.json')
    try:
        with open(file_name, 'w') as json_file:
            json.dump(csv_dump_for_bank, json_file)
        print(f'File generated at path {file_name}')
    except Exception as exc:
        print('File not generated properly please have a look', exc)


def main(args):
    '''Entry point to save csv generation.'''

    csv_dump_for_bank = get_consolidated_bank_statement()
    if csv_dump_for_bank:
        if args.json:
            print("Selected json file to generate")
            json_generator(csv_dump_for_bank)
        else:
            print("Selected csv file to generate")
            csv_generator(csv_dump_for_bank)
    else:
        print('Csv dump not generated properly, mostly csv file are not there in folder')


if __name__ == "__main__":
    parser_args = argparse.ArgumentParser('Arguments for consolidated bank statement generation')
    parser_args.add_argument('--json', action='store_true', default=False)
    args = parser_args.parse_args()
    main(args)