import cargodelivery as cd


SEPARATOR = "\n" + "/" * 100


if __name__ == "__main__":

    truck_fo_same_liquid = cd.TruckFHTank()
    truck_fo_same_car = cd.TruckFLCarTransporter()
    print(truck_fo_same_liquid.__repr__())
    print(truck_fo_same_car.__str__(), SEPARATOR)

    product_1 = cd.Product('Milk', 'liquid', 10)
    product_2 = cd.Product('Volvo', 'car', 2, {'hight': 100, 'width': 150, 'deep': 300})
    product_3 = cd.Product('Beer', 'liquid', 2, {'hight': 30, 'width': 15, 'deep': 30})
    print(product_1.__repr__())
    print(product_2.__str__())
    print(product_1.__cmp__(product_1))
    print(product_1.__cmp__(product_2))
    print(product_1.__cmp__(product_3))
    print(product_1.__add__(product_1))
    print(product_1.__add__(product_2))
    print(product_1.__add__(product_3))
    product_1.__copy__()
    print(SEPARATOR)

    cargo_1 = cd.Cargo(1, 10, {'hight': 100, 'width': 150, 'deep': 300}, [product_1])
    cargo_2 = cd.Cargo(2, 20, {'hight': 100, 'width': 150, 'deep': 300}, list(product_2 for _ in range(6)))
    print(cargo_1.__repr__())
    print(cargo_2.__str__(), SEPARATOR)

    order_1 = cd.CargoDelivery('Odessa', 'Kiev', truck_fo_same_liquid, cargo_1)
    order_2 = cd.CargoDelivery('Odessa', 'Kiev', truck_fo_same_car, cargo_2)
    print(order_1.__repr__())
    print(order_2.__str__(), SEPARATOR)
