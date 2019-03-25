import csv
from .exceptions import InvalidFile

class CSVParser:
    def __init__(self, filename=None):
        csv.register_dialect('semicolon-delimited', delimiter=';')
        self.filename = filename or 'cars.csv'
        self.validate_file()

    def validate_file(self):
        try:
            with open(self.filename) as file:
                file.close()
        except FileNotFoundError as e:
            raise InvalidFile(e)

    def items(self):
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile, dialect='semicolon-delimited')
            for row in reader:
                if self.item_is_valid(row):
                    yield row

    @staticmethod
    def item_is_valid(row):
        for val in row.values():
            if val:
                return True
        return False
