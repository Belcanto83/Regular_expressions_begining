import csv
from collections import namedtuple
from custom_parser import ContactsParser


def merge_rows(contact_list):
    pos = 1
    while pos < len(contact_list) - 1:
        pass


def main():
    with open('phonebook_raw.csv', encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=',')
        contact_list_raw = list(rows)

    contact_list = []
    parser = ContactsParser()
    column_names = contact_list_raw[0]
    TableRow = namedtuple('TableRow', column_names)
    for ind, row_raw in enumerate(contact_list_raw):
        print(row_raw)
        if ind == 0:
            contact_list.append(row_raw)
            continue
        row_raw = row_raw[:7]
        new_table_row = TableRow(*row_raw)
        row = dict.fromkeys(column_names, '')
        for col in column_names:
            if col == 'lastname':
                name_for_parsing = new_table_row.lastname + ' ' + new_table_row.firstname + ' ' + new_table_row.surname
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

    with open('phonebook.csv', 'w') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(contact_list)


if __name__ == '__main__':
    main()
