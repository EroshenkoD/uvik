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

perfect_num = (6, 28, 496, 8128, 33550336, 8589869056, 137438691328, 2305843008139952128,
               2658455991569831744654692615953842176, 191561942608236107294793378084303638130997321548169216)

try:
    col_num = int(input("Input :"))
except:
    col_num = False
    print("Data entry is error")

if col_num:
    if col_num <= 10:
        res = ""
        for i in range(col_num):
            res += f"{perfect_num[i]}, "
        print(f"Output: {res[:-2]}")
    elif col_num <= 51:
        print("I don't know so many ideal numbers, ask the guys from Great Internet Mersenne Prime Search")
    else:
        print("I don't know so many perfect numbers, but you can calculate them "
              "using the formula 2\u1D56\u207B\u00b9x(2\u1D56−1)")
