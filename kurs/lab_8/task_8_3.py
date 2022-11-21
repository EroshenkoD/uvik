"""
Write an algorithm that will identify valid IPv4 addresses in dot-decimal format.
IPs should be considered valid if they consist of four octets, with values between 0 and 255, inclusive.

Note: Create the main class for that task and the descriptor for getting and setting ip values.

Examples of correct ip addresses: 1.2.3.4, 123.45.67.89
Examples of incorrect ip addresses: 1.2.3, 1.2.3.4.5, 123.456.78.90, 123.045.067.089
"""
from dataclasses import dataclass


class IPAddressError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


@dataclass
class IPDescriptor:
    ip: str = ""

    def __get__(self, instance, owner):
        return self.ip

    def __set__(self, instance, ip):
        if ip:
            error_mess = f"Incorrect IP addresses: {ip}"
            list_num_ip = ip.split(".")
            if len(list_num_ip) != 4:
                raise IPAddressError(error_mess)
            for i in list_num_ip:
                if i.isdigit():
                    if any((i[0] == "0", int(i) < 0, int(i) > 255)):
                        raise IPAddressError(error_mess)
                else:
                    raise IPAddressError(error_mess)
            self.ip = ip
            return self.ip


@dataclass
class IPModification:
    ip: str = IPDescriptor(ip="")


if __name__ == "__main__":
    check_ip = ('1.2.3.4', '123.45.67.89', '1.2.3', '1.2.3.4.5', '123.456.78.90', '123.045.067.089')
    temp = IPModification()
    for j in check_ip:
        try:
            temp.ip = j
        except IPAddressError as e:
            print(e)
        print(str(temp)+"\n")
