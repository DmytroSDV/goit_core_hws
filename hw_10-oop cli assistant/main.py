from collections import UserDict


class Field:
    def __init__(self, value):
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
        self.value = self.validation(value)

    def validation(self, value):
        if len(value) == 10 and value.isdigit():
            return value
        else:
            raise ValueError


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


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
