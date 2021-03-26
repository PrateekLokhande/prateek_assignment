import os
from collections import OrderedDict
from bank_csv_dumping import date_converter, csv_file_identifier, data_generator,\
                             get_consolidated_bank_statement, write_consolidated_data_csv

def test_date_converter():
    '''Test for date converter.'''

    date = date_converter("Oct 1 2019")
    assert date == "2019-10-01"


def test_csv_file_identifier():
    '''Test for csv identifier.'''

    data = csv_file_identifier()
    check_path = all([os.path.exists(csv) for csv in data])
    assert check_path


def test_data_generator():
    '''test for data generator.'''

    row = OrderedDict([('date', '03-10-2019'), 
                       ('transaction', 'remove'), 
                       ('amounts', '99.40'), 
                       ('to', '182'), 
                       ('from', '198')])
    data = data_generator(row)
    result = ["2019-10-03", "remove", "99", "40", "198", "182"]
    check_result = all(list(map(lambda x, y: data[x] == y, data, result)))
    assert check_result


def test_get_consolidated_bank_statements():
    ''' test for consolidated bank statements.'''

    data = get_consolidated_bank_statement()
    result = all([isinstance(element, dict) and element for element in data])
    assert result


def test_write_consolidated_data_csv():
    '''test for csv existence after generation.'''

    data = get_consolidated_bank_statement()
    filename = write_consolidated_data_csv(data)
    assert os.path.exists(filename)
