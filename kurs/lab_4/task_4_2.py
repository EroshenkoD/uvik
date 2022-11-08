"""IP Validation
Write an algorithm that will identify valid IPv4 addresses in dot-decimal format. IPs should be considered valid
if they consist of four octets, with values between 0 and 255, inclusive.

Note: Create the decorator that validates if the passed to inner function ip value is correct.
In case of incorrect ip format, user should see the error message.

Examples of correct ip addresses: 1.2.3.4, 123.45.67.89
Examples of incorrect ip addresses: 1.2.3, 1.2.3.4.5, 123.456.78.90, 123.045.067.089"""

from functools import wraps


input_text = input("Input: ")


def my_decorator(func):
    @wraps(func)
    def wrapper(*args):
        error_mess = f"Incorrect ip addresses: {input_text}"
        list_num_ip = input_text.split(".")
        if len(list_num_ip) != 4:
            raise ValueError(error_mess)

        for i in list_num_ip:
            if i.isdigit():
                if i[0] == "0" or int(i) < 0 or int(i) > 255:
                    raise ValueError(error_mess)
            else:
                raise ValueError(error_mess)

        func(input_text)
    return wrapper


@my_decorator
def print_ip(arg_ip):
    print(f"Correct ip addresses: {arg_ip}")


if __name__ == "__main__":

    try:
        print_ip(input_text)
    except ValueError as e:
        print(e)
