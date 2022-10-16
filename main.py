import csv
from collections import namedtuple
from custom_parser import ContactsParser


def merge_rows(contact_list):
    pos = 0
    column_names = contact_list[0]
    while pos < len(contact_list) - 1:
        row_1 = contact_list[pos]
        row_1 = {column_names[i]: row_1[i] for i in range(len(column_names))}

        row_2 = contact_list[pos+1]
        row_2 = {column_names[i]: row_2[i] for i in range(len(column_names))}

        merge_possible = 0
        if row_1['lastname'] == row_2['lastname'] and row_1['firstname'] == row_2['firstname']:
            merge_possible = 1
            for col in column_names[2:]:
                if row_1[col] == row_2[col] or (row_1[col] and not row_2[col]):
                    merge_possible *= 1
                elif row_2[col] and not row_1[col]:
                    merge_possible *= 1
                    row_1[col] = row_2[col]
                    contact_list[pos] = list(row_1.values())
                else:
                    merge_possible *= 0
        if merge_possible:
            del contact_list[pos+1]
        else:
            pos += 1
    return contact_list


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
        row_raw = row_raw[:len(column_names)]
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

    print('*' * 50)
    merged_contact_list = merge_rows(contact_list)
    for row in merged_contact_list:
        print(row)

    with open('phonebook.csv', 'w') as f:
        data_writer = csv.writer(f, delimiter=',')
        data_writer.writerows(merged_contact_list)


if __name__ == '__main__':
    main()
