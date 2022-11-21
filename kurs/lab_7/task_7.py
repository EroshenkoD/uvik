"""
Class modifications
Modify your existing topology classes with dataclass or any other library for simplification.
"""
from abc import ABC, abstractmethod
from attr import attrs, attrib
from dataclasses import dataclass
from collections import namedtuple


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


@attrs
class Product:
    name = attrib()
    type_product = attrib()
    weight = attrib()
    size = attrib(default={'hight': 10, 'width': 15, 'deep': 30})

    @weight.validator
    def check_weight(self, attribute, weight):
        if weight < 0 or weight > 100:
            raise ValueError(f'Max weight 100 kg')


@dataclass
class Cargo:
    id_cargo: int
    weight: int
    size: dict
    list_product: list

    def get_type_of_truck_for_delivery(self):
        return f"This one will do for {self.id_cargo}"


CargoDelivery = namedtuple('CargoDelivery', ['start_point', 'end_point', 'packagetruck', 'packagecargo'])


if __name__ == "__main__":

    truck_fo_same_liquid = TruckFHTank('truck1')
    truck_fo_same_car = TruckFLCarTransporter('truck2')
    print(repr(truck_fo_same_liquid))
    print(str(truck_fo_same_car))

    product_1 = Product('Milk', 'liquid', 10)
    product_2 = Product('Volvo', 'car', 2)
    print(repr(product_1))
    print(str(product_2))

    cargo_1 = Cargo(1, 10, {'hight': 100, 'width': 150, 'deep': 300}, [product_1])
    cargo_2 = Cargo(2, 20, {'hight': 100, 'width': 150, 'deep': 300}, list(product_2 for _ in range(6)))
    print(repr(cargo_1))
    print(str(cargo_2))

    order_1 = CargoDelivery('Odessa', 'Kiev', truck_fo_same_liquid, cargo_1)
    order_2 = CargoDelivery('Odessa', 'Kiev', truck_fo_same_car, cargo_2)
    print(repr(order_1))
    print(str(order_2))
