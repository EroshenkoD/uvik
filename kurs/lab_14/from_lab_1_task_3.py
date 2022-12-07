"""Check for balanced parentheses
Given an expression string, write a python program to find whether a given string has balanced parentheses or not.

Input : {[]{()}}
Output : Balanced

Input : [{}{}(]
Output : Unbalanced

Input : {][{()}}
Output : Unbalanced
"""
import time


def check_balanced(data: str) -> str:
    go_sleep()

    check_dict = {"{}": 0, "()": 0, "[]": 0}
    cur_closing = [""]
    res = ""
    for i in data:

        if i == "{":
            check_dict["{}"] += 1
            cur_closing.append("}")
        elif i == "}" and cur_closing[-1] == "}":
            check_dict["{}"] -= 1
            del cur_closing[-1]

        elif i == "(":
            check_dict["()"] += 1
            cur_closing.append(")")
        elif i == ")" and cur_closing[-1] == ")":
            check_dict["()"] -= 1
            del cur_closing[-1]

        elif i == "[":
            check_dict["[]"] += 1
            cur_closing.append("]")
        elif i == "]" and cur_closing[-1] == "]":
            check_dict["[]"] -= 1
            del cur_closing[-1]

        else:
            res = "Unbalanced"
            break

    if not res:
        for values in check_dict.values():
            if values != 0:
                res = "Unbalanced"
                break
            else:
                res = "Balanced"
    return res


def go_sleep():
    time.sleep(2)


if __name__ == "__main__":
    print(check_balanced('[{}{}(]'))
