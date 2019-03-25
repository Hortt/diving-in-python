import csv
import os
import sys
from collections import OrderedDict


class InvalidFile(BaseException):
    pass


class BaseCar:

    def __init__(self, photo_file_name, brand, carrying):
        self.brand = brand
        self.carrying = carrying or None
        self.photo_file_path = photo_file_name
        self.photo_file = os.path.split(self.photo_file_path)[1]

    def get_photo_file_ext(self):
        if self.is_valid_photo():
            return self.photo_file.split('.')[1]
        raise InvalidFile('Bad file exception: {}. Make sure it\s a photo'.format(self.photo_file_path))

    def is_valid_photo(self):
        return len(self.photo_file.split('.')) < 2

    def to_dict(self):
        car_data = {}
        for attr in dir(self):
            if self._is_relevant_attribute(attr):
                car_data.update({attr: getattr(self, attr)})
        return car_data

    def _is_relevant_attribute(self, attr):
        return isinstance(getattr(self, attr), (str, int, float)) and '__' not in attr

    def __str__(self):
        string_repr = ''
        for key, value in self.to_dict().items():
            string_repr += str(key) + ': ' + str(value) + '; '
        return string_repr


class PassengerCar(BaseCar):

    def __init__(self, photo_file_name, brand, carrying, passenger_seats_count):
        super(PassengerCar, self).__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count
        self.car_type = 'car'

    def __str__(self):
        return f"Легковой Автомобиль марки {self.brand}, {self.passenger_seats_count} мест, грузоподъемностью " \
               f"{self.carrying} тонн"


class Truck(BaseCar):

    def __init__(self, photo_file_name, brand, carrying, body_whl):
        super(Truck, self).__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        self.body_whl = body_whl

    @property
    def body_width(self):
        return float(self.body_whl.split('x')[0]) if self.body_whl else 0

    @property
    def body_height(self):
        return float(self.body_whl.split('x')[1]) if self.body_whl else 0

    @property
    def body_length(self):
        return float(self.body_whl.split('x')[2]) if self.body_whl else 0

    @property
    def body_volume(self):
        return str(self.body_height * self.body_width * self.body_length) + ' м.куб'

    def __str__(self):
        return f"Грузовик марки {self.brand}, Объем кузова: {self.body_volume}, грузоподъемностью " \
               f"{self.carrying} тонн"


class SpecMachine(BaseCar):

    def __init__(self, photo_file_name, brand, carrying, extra):
        super(SpecMachine, self).__init__(brand, photo_file_name, carrying)
        self.car_type = 'spec_machine'
        self.extra = extra

    def __str__(self):
        return f"Спецтехника марки {self.brand}, грузоподъемностью " f"{self.carrying}. {self.extra}"


class BaseCarDataExtractor:

    def __init__(self, raw_data: OrderedDict):
        self.input_data = raw_data
        self.arguments = self.get_arguments()

    def get_arguments(self):
        return [self.input_data['brand'], self.input_data['photo_file_name'], self.input_data['carrying']]


class PassengerCarDataExtractor(BaseCarDataExtractor):

    def __init__(self, raw_data: OrderedDict):
        super(PassengerCarDataExtractor, self).__init__(raw_data)
        self.input_data = raw_data
        self.arguments = self.get_arguments()
        self.extend_arguments()

    def extend_arguments(self):
        self.arguments.append(self.input_data['passenger_seats_count'])


class TruckDataExtractor(BaseCarDataExtractor):

    def __init__(self, raw_data: OrderedDict):
        super(TruckDataExtractor, self).__init__(raw_data)
        self.extend_arguments()

    def extend_arguments(self):
        self.arguments.append(self.input_data['body_whl'])


class SpecMachineDataExtractor(BaseCarDataExtractor):

    def __init__(self, raw_data: OrderedDict):
        super(SpecMachineDataExtractor, self).__init__(raw_data)
        self.extend_arguments()

    def extend_arguments(self):
        self.arguments.append(self.input_data['extra'])


class CSVParser:
    def __init__(self, filename=None):
        csv.register_dialect('semicolon-delimited', delimiter=';')
        self.filename = filename or 'cars.csv'

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


CAR_TYPE_MAP = {
    'car': PassengerCar,
    'truck': Truck,
    'spec_machine': SpecMachine
}

CAR_TYPE_DATA_EXTRACTOR_MAP = {
    'car': PassengerCarDataExtractor,
    'truck': TruckDataExtractor,
    'spec_machine': SpecMachineDataExtractor
}


class CarList:

    data_provider = CSVParser

    def __init__(self):
        self.file = sys.argv[1] if len(sys.argv) > 1 else None
        self.car_list = []
        self.get_list()

    @staticmethod
    def get_car_model_by_type(car_type):
        return CAR_TYPE_MAP[car_type]

    @staticmethod
    def get_car_data_extractor_by_type(car_type):
        return CAR_TYPE_DATA_EXTRACTOR_MAP[car_type]

    def get_list(self):
        for car_data in self.data_provider(self.file).items():
            car_model = self.get_car_model_by_type(car_data['car_type'])
            car_data_extractor = self.get_car_data_extractor_by_type(car_data['car_type'])
            self.car_list.append(
                car_model(*car_data_extractor(car_data).arguments)
            )

    def print(self):
        print(self.car_list)


def main():
    CarList().print()


if __name__ == "__main__":
    main()
