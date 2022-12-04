"""Multiply numbers
Given two numbers. The task is to mutiply them without using the * operator.

Input : 12, 12
Output : 144

Input : 19, 0
Output : 0

Input : 1.1, 17.2
Output : 18.92

Input : -2, 4
Output : -8
"""
from typing import Union


def multiply_without_multiply(a: Union[float, int], b: Union[float, int]) -> Union[float, int]:
    res = round(((a+b)**2 - a**2 - b**2) / 2, 2)
    res_int = int(res)
    if res == res_int:
        res = res_int
    return res


if __name__ == "__main__":
    print(multiply_without_multiply(-2, 4))
