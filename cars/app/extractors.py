from collections.__init__ import OrderedDict


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
