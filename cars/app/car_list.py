import sys

from .extractors import PassengerCarDataExtractor, TruckDataExtractor, SpecMachineDataExtractor
from .models import PassengerCar, Truck, SpecMachine
from .parsers import CSVParser

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
    def get_car_model_by_type(car_type: str):
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
        for car in self.car_list:
            print(car)
