from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
# ваш код

EXPECTED_FIELDS_COUNT = 7

for contact in contacts_list:
    while len(contact) < EXPECTED_FIELDS_COUNT:
        contact.append('')

for contact in contacts_list:
    fio_parts = " ".join(contact[:3]).split()
    contact[0] = fio_parts[0] if len(fio_parts) > 0 else ''
    contact[1] = fio_parts[1] if len(fio_parts) > 1 else ''
    contact[2] = fio_parts[2] if len(fio_parts) > 2 else ''


phone_pattern = re.compile(
    r'(?:\+7|8)?\D*(\d{3})\D*(\d{3})\D*(\d{2})\D*(\d{2})\D*(?:доб\.?\D*(\d+))?$',
     re.IGNORECASE
)

for contact in contacts_list:
    phone = contact[5]
    match = phone_pattern.search(phone.replace(' ', ''))
    if match:
        new_phone = f"+7({match.group(1)}){match.group(2)}-{match.group(3)}-{match.group(4)}"
        if match.group(5):
            new_phone += f" доб.{match.group(5)}"
        contact[5] = new_phone


phonebook_dict = {}
for contact in contacts_list:
    key = (contact[0].strip(), contact[1].strip())
    if key not in phonebook_dict:
        phonebook_dict[key] = contact.copy()
    else:
        existing_contact = phonebook_dict[key]
        for i in range(EXPECTED_FIELDS_COUNT):
            if existing_contact[i].strip() == '' and contact[i].strip() != '':
                existing_contact[i] = contact[i]


normalized_contacts_list = list(phonebook_dict.values())

pprint(normalized_contacts_list)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(normalized_contacts_list)