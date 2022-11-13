"""
Class modifications pt.2
Modify your existing topology classes with at least one abstract class.

Add magic methods to recieve description of the objects.
Override at least one comparison method.
Override at least one arithmetic method.
Override at least one copying method.
"""

from abc import ABC, abstractmethod
from attr import attrs, attrib
from dataclasses import dataclass
from collections import namedtuple


class Truck(ABC):
    def __init__(self):
        self.truck_model = "Volvo"

    def __str__(self):
        return self.__dict__

    def __repr__(self):
        return dir(self)

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

    def __cmp__(self, other):
        if not isinstance(other, Product):
            raise TypeError('Only Product')
        return self.type_product == other.type_product

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError('Only Product')
        weight = self.weight + other.weight
        size = {'hight': self.size['hight'] if self.size['hight'] > other.size['hight'] else other.size['hight'],
                'width': self.size['width'] + other.size['width'],
                'deep': self.size['hight'] if self.size['hight'] > other.size['hight'] else other.size['hight']}
        return weight, size

    def __copy__(self):
        print('Do not copy!')


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

    product_1 = Product('Milk', 'liquid', 10)
    product_2 = Product('Volvo', 'car', 2, {'hight': 100, 'width': 150, 'deep': 300})
    product_3 = Product('Beer', 'liquid', 2, {'hight': 30, 'width': 15, 'deep': 30})

    print(product_1.__cmp__(product_1))
    print(product_1.__cmp__(product_2))
    print(product_1.__cmp__(product_3))

    print(product_1.__add__(product_1))
    print(product_1.__add__(product_2))
    print(product_1.__add__(product_3))

    product_1.__copy__()

    print(TruckFLCarTransporter().__str__())
    print(TruckFLCarTransporter().__repr__())
