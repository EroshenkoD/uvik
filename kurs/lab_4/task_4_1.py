"""
Perfect numbers generator
Given the number, the task to return n perfect numbers.
In number theory, a perfect number is a positive integer that is equal to the sum of its positive divisors,
excluding the number itself. For instance, 6 has divisors 1, 2 and 3 (excluding itself), and 1 + 2 + 3 = 6,
so 6 is a perfect number. More about perfect numbers read on https://en.wikipedia.org/wiki/Perfect_number.
Note: Use generator for that task
Input: 3
Output: 6, 28, 496
"""
from functools import lru_cache


class IdealNumError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


@lru_cache(maxsize=128)
def gen_ideal_num():
    cur_num = 6
    while True:
        if cur_num == 8129:
            raise IdealNumError("I'm tired")
        temp_num = 0
        for i in range(1, int(cur_num // 2) + 1):
            if cur_num % i == 0:
                temp_num += i
        if temp_num == cur_num:
            yield cur_num
        cur_num += 1


if __name__ == "__main__":

    try:
        col_num = int(input("Input :"))
    except ValueError as e:
        col_num = False
        print(e)

    if col_num:
        my_gen = (gen_ideal_num())
        for _ in range(col_num):
            try:
                print(next(my_gen))
            except IdealNumError as e:
                print(e)
                break
            except StopIteration as e:
                print(e)
        print(gen_ideal_num.cache_info())
