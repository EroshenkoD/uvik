from dataclasses import dataclass


@dataclass
class Cargo:
    id_cargo: int
    weight: int
    size: dict
    list_product: list

    def type_of_truck_for_delivery(self):
        return f"This one will do for {self.id_cargo}"


if __name__ == "__main__":
    pass
