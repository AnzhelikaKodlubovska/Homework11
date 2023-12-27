from datetime import datetime

class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid value")
        self._value = value

    def __str__(self):
        return str(self._value)

    def is_valid(self, value):
        return True

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError("Invalid value")
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    def is_valid(self, value):
        return len(str(value)) == 10 and str(value).isdigit()

    @Field.value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            raise ValueError("Invalid phone number format")
        self._value = new_value


class Birthday(Field):
    def is_valid(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            return (next_birthday - today).days
        return None


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        else:
            return False

    def __iter__(self):
        return iter(self.data.values())

    def iterator(self, batch_size):
        all_records = list(self.data.values())
        for i in range(0, len(all_records), batch_size):
            yield all_records[i:i + batch_size]
