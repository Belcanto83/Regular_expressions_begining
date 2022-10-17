import csv
from collections import namedtuple
from custom_parser import ContactsParser
import contextlib


def merge_rows(data_list):
    pos = 0
    table_columns = data_list[0]
    while pos < len(data_list) - 1:
        row_1 = data_list[pos]
        row_1 = {table_columns[i]: row_1[i] for i in range(len(table_columns))}

        row_2 = data_list[pos + 1]
        row_2 = {table_columns[i]: row_2[i] for i in range(len(table_columns))}

        merge_possible = 0
        if row_1['lastname'] == row_2['lastname'] and row_1['firstname'] == row_2['firstname']:
            merge_possible = 1
            for column in table_columns[2:]:
                if row_1[column] == row_2[column] or (row_1[column] and not row_2[column]):
                    merge_possible *= 1
                elif row_2[column] and not row_1[column]:
                    merge_possible *= 1
                    row_1[column] = row_2[column]
                    data_list[pos] = list(row_1.values())
                else:
                    merge_possible *= 0
        if merge_possible:
            del data_list[pos + 1]
        else:
            pos += 1
    return data_list


@contextlib.contextmanager
def repair_contact_list(file_for_repair, encoding='UTF-8'):
    with open(file_for_repair, encoding=encoding) as f:
        rows = csv.reader(f, delimiter=',')
        rows = list(rows)
    try:
        yield rows
    except RuntimeError as err:
        print('Error: ', err)


def main():
    with repair_contact_list('phonebook_raw.csv') as rows_for_processing:
        contact_list = []
        parser = ContactsParser()
        column_names = rows_for_processing[0]
        TableRow = namedtuple('TableRow', column_names)
        for ind, row_raw in enumerate(rows_for_processing):
            print(row_raw)
            if ind == 0:
                contact_list.append(row_raw)
                continue
            row_raw = row_raw[:len(column_names)]
            new_table_row = TableRow(*row_raw)
            row = dict.fromkeys(column_names, '')
            for col in column_names:
                if col == 'lastname':
                    name_for_parsing = new_table_row.lastname + ' ' + new_table_row.firstname + ' ' + \
                                       new_table_row.surname
                    parsed_name = parser.get_parsed_name(name_for_parsing)
                    row['lastname'] = parsed_name['lastname']
                    row['firstname'] = parsed_name['firstname']
                    row['surname'] = parsed_name['surname']
                elif col in ['organization', 'position', 'email']:
                    row[col] = getattr(new_table_row, col)
                elif col == 'phone':
                    phone_for_parsing = new_table_row.phone
                    parsed_phone = parser.get_substituted_phone(phone_for_parsing)
                    row['phone'] = parsed_phone['phone']

            contact_list.append(list(row.values()))

        print('*' * 50)
        for row_clean in contact_list:
            print(row_clean)

        print('*' * 50)
        merged_contact_list = merge_rows(contact_list)
        for row in merged_contact_list:
            print(row)

        with open('phonebook.csv', 'w') as f:
            data_writer = csv.writer(f, delimiter=',')
            data_writer.writerows(merged_contact_list)


if __name__ == '__main__':
    main()
