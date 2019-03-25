import os

from .exceptions import InvalidFile


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