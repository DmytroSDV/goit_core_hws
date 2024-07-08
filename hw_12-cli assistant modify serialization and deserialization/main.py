from collections import UserDict
from datetime import datetime
import re
from faker import Faker, Factory
from random import randint
import pickle


class InputDataError(Exception):
    ...


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = self.capitalize(value)

    def capitalize(self, inc):
        return inc.capitalize()


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if len(val) == 10 and val.isdigit():
            self._value = val
        else:
            raise ValueError("Invalid phone format!")


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        if re.match(date_pattern, val):
            date_split = val.split("-")
            if int(date_split[1]) > 12:
                raise ValueError("After year YYYY you must enter month (1-12)!")
            self._value = datetime.strptime(val, "%Y-%m-%d").date()
        else:
            raise ValueError("Invalid date format! Must be YYYY-MM-DD!")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        if Birthday(birthday):
            self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today_date = datetime.now().date()
            what_year = (
                today_date.year + 1
                if self.birthday.value.month <= today_date.month
                and self.birthday.value.day < today_date.day
                else today_date.year
            )
            user_birthday = datetime(
                year=what_year,
                month=self.birthday.value.month,
                day=self.birthday.value.day,
            ).date()
            return f"{(user_birthday - today_date).days} days"
        else:
            raise ValueError("Birthday date not setted!")

    def add_phone(self, phone):
        if str(Phone(phone)):
            self.phones.append(Phone(phone))

    def edit_phone(self, exist_phone, new_phone):
        check_flag = False
        for ind, phone in enumerate(self.phones):
            if phone.value == exist_phone:
                self.phones[ind] = Phone(new_phone)
                check_flag = True
        if not check_flag:
            raise ValueError

    def remove_phone(self, del_phone):
        for phone in self.phones:
            if phone.value == del_phone:
                self.phones.remove(phone)

    def find_phone(self, phone):
        for ind, ph in enumerate(self.phones):
            if ph.value == phone:
                return self.phones[ind]

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday}."


class AddressBook(UserDict):
    def add_record(self, info):
        self.data[info.name.value] = info

    def find(self, name):
        for key in self.data:
            if key == name:
                return self.data[name]

    def delete(self, user):
        temp_dict = self.data.copy()
        for keys in temp_dict:
            if keys == user:
                self.data.pop(user)

    def iterator(self, num):
        return Generator(self.data, num)


class Generator:
    def __init__(self, data_base, num):
        self.num = num
        self.data_base = data_base

    def __iter__(self):
        return Iteration(self.data_base, self.num)


class Iteration:
    def __init__(self, data_base, num):
        self.start_index = 0
        self.data_base = data_base
        self.num = num

    def __next__(self):
        key_list = list(self.data_base.keys())
        if self.start_index < len(key_list):
            records_list = []
            for _ in range(self.num):
                if self.start_index < len(key_list):
                    current_key = key_list[self.start_index]
                    record = self.data_base[current_key]
                    records_list.append(record)
                    self.start_index += 1
                else:
                    break
            return records_list
        else:
            raise StopIteration


class DataPackUnpackFind:
    def __init__(self, file_name: str):
        self._file_name = None
        self.file_name = file_name

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        if file_name.endswith((".txt", ".bin", ".csv", ".json")):
            self._file_name = value
        else:
            raise InputDataError(
                "You enter wrong file extension fromat. Applicable formats are '*.txt', '*.bin', '*.csv', '*.json'"
            )

    def serialize(self, data_book: AddressBook):
        with open(self.file_name, "wb") as fh:
            pickle.dump(data_book, fh)

    def de_serialize(self):
        with open(self.file_name, "rb") as fh:
            data = pickle.load(fh)
            if isinstance(data, AddressBook):
                return data
            else:
                raise InputDataError("Wrong data format in the file.")

    def data_match(self, value: str, data_book: AddressBook) -> list:
        matched_list = []
        for key, item in data_book.data.items():
            for phone in item.phones:
                if item.name.value.lower().__contains__(
                    value.lower()
                ) or phone.value.__contains__(value):
                    matched_list.append(item)
                    break
            if not item.phones:
                if item.name.value.lower().__contains__(value.lower()):
                    matched_list.append(item)
        return matched_list


book = AddressBook()
fake = Factory.create("uK-UA")

for _ in range(randint(111, 291)):
    recording = Record(fake.name())
    recording.add_birthday(fake.date())
    for _ in range(randint(1, 3)):
        recording.add_phone(str(randint(10**9, 10**10 - 1)))
    book.add_record(recording)

generator = book.iterator(5)
for item in generator:
    for from_list in item:
        print(from_list)
    print("\n")

print("\n\n")

file_name = "data.bin"
data_object = DataPackUnpackFind(file_name)
data_object.serialize(book)
restored_book = data_object.de_serialize()

match_data = data_object.data_match("Одарка", restored_book)
for item in match_data:
    print(item)
