from abc import ABC, abstractmethod
from dataclasses import dataclass


class Truck(ABC):

    def __init__(self):
        self.truck_model = "Volvo"

    def get_truck_model(self):
        return self.truck_model

    @abstractmethod
    def get_model(self):
        raise NotImplemented

    @abstractmethod
    def get_type_truck(self):
        raise NotImplemented

    @abstractmethod
    def get_fuel_consumption(self):
        raise NotImplemented

    @abstractmethod
    def get_carrying(self):
        raise NotImplemented


@dataclass
class TruckFHTank(Truck):
    pet_name: str

    def get_model(self):
        print(f"I'm {super().get_truck_model()} FH")

    def get_type_truck(self):
        print("For children I drive milk for adults beer")

    def get_fuel_consumption(self):
        print("I spend 26 liters if the driver is experienced")

    def get_carrying(self):
        print("I can pull 30 tons on a good road.")

    def __str__(self):
        return f"I'm {self.pet_name}"

    def __repr__(self):
        return f'TruckFHTank({self.pet_name})'


@dataclass
class TruckFLCarTransporter(Truck):
    pet_name: str

    def get_model(self):
        print(f"I'm {super().get_truck_model()} FL")

    def get_type_truck(self):
        print("I drive smaller cars")

    def get_fuel_consumption(self):
        print("I spend 22 liters")

    def get_carrying(self):
        print("I can pull 20 tons")

    def __str__(self):
        return f"I'm {self.pet_name}"

    def __repr__(self):
        return f'TruckFLCarTransporter({self.pet_name})'
