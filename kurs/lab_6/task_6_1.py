"""
Class topology
Choose any existing topology of objects that soround us and represent it via classes. Imlement class hierarchy that
will use different relations between objects.
Use classmethods and staticmethods.
Create UML diagram to represent the topology and relations inside of it.
Note: Create at least 3 classes
"""


class CargoDelivery:
    def __init__(self, start_point, end_point, truck, cargo):
        self.start_point = start_point
        self.end_point = end_point
        self.truck = truck
        self.cargo = cargo

    def cost_of_delivery(self):
        pass


class Cargo:
    def __init__(self, id_cargo, weight, size, list_product):
        self.id_cargo = id_cargo
        self.weight = weight
        self.size = size
        self.list_product = list_product

    def type_of_truck_for_delivery(self):
        pass


class Truck:
    def __init__(self, model, type_truck, fuel_consumption):
        self.model = model
        self.type_truck = type_truck
        self.fuel_consumption = fuel_consumption


class Product:
    def __init__(self, model, type_truck, fuel_consumption):
        self.model = model
        self.type_truck = type_truck
        self.fuel_consumption = fuel_consumption


def best_product_placement(height, width, depth):
    pass
