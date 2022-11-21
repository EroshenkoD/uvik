"""
ISBN-10 or IP modifications¶
Update the decorator used for task from lab4 (choose ISBN-10 or IP) to be the class with overrided method __call__().
"""
from dataclasses import dataclass


@dataclass
class IPModification:
    ip: str = ""

    def __call__(self, ip):
        error_mess = f"Incorrect ip addresses: {ip}"
        list_num_ip = ip.split(".")
        if len(list_num_ip) != 4:
            raise ValueError(error_mess)
        for i in list_num_ip:
            if i.isdigit():
                if any((i[0] == "0", int(i) < 0, int(i) > 255)):
                    raise ValueError(error_mess)
            else:
                raise ValueError(error_mess)
        self.ip = ip
        return self.ip


if __name__ == "__main__":
    check_ip = ('1.2.3.4', '123.45.67.89', '1.2.3', '1.2.3.4.5', '123.456.78.90', '123.045.067.089')
    temp = IPModification()
    for j in check_ip:
        try:
            temp.__call__(ip=j)
        except ValueError as e:
            print(e)
        print(temp.__str__()+"\n")
