"""
ISBN-10 or IP modifications¶
Update the decorator used for task from lab4 (choose ISBN-10 or IP) to be the class with overrided method __call__().
"""


class IPAddressError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class IPCheckDecorator:

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            error_mess = f"Incorrect IP addresses: {kwargs['ip_to_check']}"
            list_num_ip = kwargs['ip_to_check'].split(".")
            if len(list_num_ip) != 4:
                raise IPAddressError(error_mess)
            for i in list_num_ip:
                if i.isdigit():
                    if any((i[0] == "0", int(i) < 0, int(i) > 255)):
                        raise IPAddressError(error_mess)
                else:
                    raise IPAddressError(error_mess)
            return func(*args, **kwargs)
        return wrapper


@IPCheckDecorator()
def check_ip(ip_to_check):
    print(f"Correct IP addresses: {ip_to_check}")


if __name__ == "__main__":
    tuple_ip = ('1.2.3.4', '123.45.67.89', '1.2.3', '1.2.3.4.5', '123.456.78.90', '123.045.067.089')
    for j in tuple_ip:
        try:
            check_ip(ip_to_check=j)
        except IPAddressError as e:
            print(e)

