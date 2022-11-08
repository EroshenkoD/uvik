"""
ISBN-10 Validation
ISBN-10 identifiers are ten digits long. The first nine characters are digits 0-9. The last digit can be 0-9 or X,
to indicate a value of 10.

An ISBN-10 number is valid if the sum of the digits multiplied by their position modulo 11 equals zero.
More about ISBN on https://en.wikipedia.org/wiki/ISBN

For example:

ISBN     : 1 1 1 2 2 2 3 3 3  9
position : 1 2 3 4 5 6 7 8 9 10
This is a valid ISBN, because:

(1*1 + 1*2 + 1*3 + 2*4 + 2*5 + 2*6 + 3*7 + 3*8 + 3*9 + 9*10) % 11 = 0
Note: Create the decorator that validates if the passed to inner function isbn value is correct.
In case of incorrect isbn format, user should see the error message.

Examples of correct isbn-10 addresses: 1112223339, 1234554321, 048665088X
Examples of incorrect isbn-10 addresses: 111222333, 1112223339X, 1234512345, X123456788
"""

from functools import wraps


input_text = input("Input: ")


def my_decorator(func):
    @wraps(func)
    def wrapper(*args):
        error_mess = f"Incorrect ip addresses: {input_text}"

        if len(input_text) != 10:
            raise ValueError(error_mess)

        sum_num = 0
        index_num = 1
        for i in input_text:
            if i.isdigit():
                sum_num += (int(i) * index_num)
                index_num += 1
            elif i == "X" and index_num == 10:
                sum_num += 100
            else:
                raise ValueError(error_mess)

        if sum_num % 11:
            raise ValueError(error_mess)

        func(input_text)
    return wrapper


@my_decorator
def check_isbn(arg_isbn):
    print(f"Correct isbn-10 addresses: {arg_isbn}")


if __name__ == "__main__":

    try:
        check_isbn(input_text)
    except ValueError as e:
        print(e)

