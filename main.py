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
    for ind, row_raw in enumerate(contact_list_raw):
        print(row_raw)
        if ind == 0:
            contact_list.append(row_raw)
            continue
        row = []
        for col_nr in range(len(row_raw)):
            if col_nr == 0:
                name_for_parsing = ' '.join(row_raw[:3])
                parsed_name = parser.get_parsed_name(name_for_parsing)
                row[:3] = parsed_name.values()
            elif 3 <= col_nr <= 4 or col_nr == 6:
                row.append(row_raw[col_nr])
            elif col_nr == 5:
                phone_for_parsing = row_raw[col_nr]
                parsed_phone = parser.get_substituted_phone(phone_for_parsing)
                row.append(parsed_phone['phone'])

        contact_list.append(row)

    print('*' * 50)
    for row_clean in contact_list:
        print(row_clean)

    with open('phonebook.csv', 'w') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(contact_list)


if __name__ == '__main__':
    main()
