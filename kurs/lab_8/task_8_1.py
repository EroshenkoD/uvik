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
from copy import copy


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


@attrs(eq=False)
class Product:
    name = attrib()
    type_product = attrib()
    weight = attrib()
    size = attrib(default={'hight': 10, 'width': 15, 'deep': 30})

    @weight.validator
    def check_weight(self, attribute, weight):
        if weight < 0 or weight > 100:
            raise ValueError(f'Max weight 100 kg')

    def __eq__(self, other):
        print("It's __eq__")
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


@dataclass
class Cargo:
    id_cargo: int
    weight: int
    size: dict
    list_product: list

    def __eq__(self, other):
        print("It's __eq__")
        if not isinstance(other, Cargo):
            raise TypeError('Only Cargo')
        return self.weight == other.weight

    def __copy__(self):
        new_copy = Cargo(self.id_cargo + 1, self.weight, self.size, self.list_product)
        return new_copy

    def get_type_of_truck_for_delivery(self):
        return f"This one will do for {self.id_cargo}"


CargoDelivery = namedtuple('CargoDelivery', ['start_point', 'end_point', 'truck', 'cargo'])


if __name__ == "__main__":
    SEPARATOR = "\n" + "/" * 100

    product_1 = Product('Milk', 'liquid', 10)
    product_2 = Product('Volvo', 'car', 2, {'hight': 100, 'width': 150, 'deep': 300})
    product_3 = Product('Beer', 'liquid', 2, {'hight': 30, 'width': 15, 'deep': 30})

    print(f'Print 1 {product_1 == product_1}')
    print(f'Print 2 {product_1 == product_2}')
    print(f'Print 3 {product_1 == product_3}')
    print(f'Print 4 {product_1.type_product == product_3.type_product}')

    print(product_1 + product_1)
    print(product_1 + product_2)
    print(product_1 + product_3, SEPARATOR)

    print(str(TruckFLCarTransporter('truck1')))
    print(repr(TruckFLCarTransporter('truck2')), SEPARATOR)

    cargo_1 = Cargo(1, 10, {'hight': 100, 'width': 150, 'deep': 300}, [product_1])
    cargo_2 = Cargo(2, 10, {'hight': 100, 'width': 150, 'deep': 300}, list(product_2 for _ in range(6)))
    print(cargo_1 == cargo_2)
    print(cargo_1 is cargo_2, SEPARATOR)

    cargo_3 = copy(cargo_1)
    print(type(cargo_3))
    print(type(cargo_1))
    print(cargo_1 == cargo_3)
    print(cargo_1 is cargo_3)




