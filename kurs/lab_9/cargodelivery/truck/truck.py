from abc import ABC, abstractmethod


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


if __name__ == "__main__":
    pass
