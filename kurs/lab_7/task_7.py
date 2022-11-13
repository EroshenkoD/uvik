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

    def we_are(self):
        return self.truck_model

    @abstractmethod
    def model(self):
        raise NotImplemented

    @abstractmethod
    def type_truck(self):
        raise NotImplemented

    @abstractmethod
    def fuel_consumption(self):
        raise NotImplemented

    @abstractmethod
    def carrying(self):
        raise NotImplemented


class TruckFHTank(Truck):
    def model(self):
        print(f"I'm {super().we_are()} FH")

    def type_truck(self):
        print("For children I drive milk for adults beer")

    def fuel_consumption(self):
        print("I spend 26 liters if the driver is experienced")

    def carrying(self):
        print("I can pull 30 tons on a good road.")


class TruckFLCarTransporter(Truck):
    def model(self):
        print(f"I'm {super().we_are()} FL")

    def type_truck(self):
        print("I drive smaller cars")

    def fuel_consumption(self):
        print("I spend 22 liters")

    def carrying(self):
        print("I can pull 20 tons")


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

    def type_of_truck_for_delivery(self):
        return f"This one will do for {self.id_cargo}"


CargoDelivery = namedtuple('CargoDelivery', ['start_point', 'end_point', 'truck', 'cargo'])


if __name__ == "__main__":

    truck_fo_same_liquid = TruckFHTank()
    truck_fo_same_car = TruckFLCarTransporter()
    print(truck_fo_same_liquid.__repr__())
    print(truck_fo_same_car.__str__())

    product_1 = Product('Milk', 'liquid', 10)
    product_2 = Product('Volvo', 'car', 2)
    print(product_1.__repr__())
    print(product_2.__str__())

    cargo_1 = Cargo(1, 10, {'hight': 100, 'width': 150, 'deep': 300}, [product_1])
    cargo_2 = Cargo(2, 20, {'hight': 100, 'width': 150, 'deep': 300}, list(product_2 for _ in range(6)))
    print(cargo_1.__repr__())
    print(cargo_2.__str__())

    order_1 = CargoDelivery('Odessa', 'Kiev', truck_fo_same_liquid, cargo_1)
    order_2 = CargoDelivery('Odessa', 'Kiev', truck_fo_same_car, cargo_2)
    print(order_1.__repr__())
    print(order_2.__str__())
