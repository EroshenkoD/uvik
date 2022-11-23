import cargo_delivery as cd


SEPARATOR = "\n" + "/" * 100


if __name__ == "__main__":

    truck_fo_same_liquid = cd.TruckFHTank('truck_1')
    truck_fo_same_car = cd.TruckFLCarTransporter('truck_1')
    print(repr(truck_fo_same_liquid))
    print(str(truck_fo_same_car), SEPARATOR)

    product_1 = cd.Product('Milk', 'liquid', 10)
    product_2 = cd.Product('Volvo', 'car', 2, {'hight': 100, 'width': 150, 'deep': 300})
    product_3 = cd.Product('Beer', 'liquid', 2, {'hight': 30, 'width': 15, 'deep': 30})
    print(repr(product_1))
    print(str(product_2))

    print(product_1 + product_1)
    print(product_1 + product_2)
    print(product_1 + product_3)
    print(SEPARATOR)

    cargo_1 = cd.Cargo(1, 10, {'hight': 100, 'width': 150, 'deep': 300}, [product_1])
    cargo_2 = cd.Cargo(2, 20, {'hight': 100, 'width': 150, 'deep': 300}, list(product_2 for _ in range(6)))
    print(repr(cargo_1))
    print(str(cargo_2), SEPARATOR)

    order_1 = cd.CargoDelivery('Odessa', 'Kiev', truck_fo_same_liquid, cargo_1)
    order_2 = cd.CargoDelivery('Odessa', 'Kiev', truck_fo_same_car, cargo_2)
    print(repr(order_1))
    print(str(order_2), SEPARATOR)
