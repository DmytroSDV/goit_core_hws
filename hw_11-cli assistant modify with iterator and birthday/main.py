from collections import UserDict
from datetime import datetime
import re


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
                raise ValueError(
                    "After year YYYY you must enter month (1-12)!")
            self._value = datetime.strptime(val, '%Y-%m-%d').date()
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
            what_year = today_date.year + \
                1 if self.birthday.value.month <= today_date.month and self.birthday.value.day < today_date.day else today_date.year
            user_birthday = datetime(
                year=what_year, month=self.birthday.value.month, day=self.birthday.value.day).date()
            return f'{(user_birthday - today_date).days} days'
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


# Створення нової адресної книги
book = AddressBook()
# 1
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday('1993-06-01')
book.add_record(john_record)

# 2
mate_record = Record("Mate")
mate_record.add_phone("1234567890")
mate_record.add_phone("5555555555")
book.add_record(mate_record)

# 3
kamila_record = Record("Kamila")
kamila_record.add_phone("1234567890")
kamila_record.add_phone("5555555555")
book.add_record(kamila_record)

# 4
ivan_record = Record("Ivan")
ivan_record.add_phone("1234567890")
ivan_record.add_phone("5555555555")
book.add_record(ivan_record)

# 5
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday('1994-07-01')
book.add_record(jane_record)

# 6
misha_record = Record("Misha")
misha_record.add_phone("9876543210")
misha_record.add_birthday('1994-07-01')
book.add_record(misha_record)

for name, record in book.data.items():
    print(record)

john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john.days_to_birthday())
print(john)

found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")

# book.delete("Ivan")

print('\n\n')

generator = book.iterator(4)


for item in generator:
    for from_list in item:
        print(from_list)
    print('\n')

print('\n\n')

for item in generator:
    print(item)
