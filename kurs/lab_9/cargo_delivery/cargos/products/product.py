from attr import attrs, attrib


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


