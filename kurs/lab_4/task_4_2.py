"""IP Validation
Write an algorithm that will identify valid IPv4 addresses in dot-decimal format. IPs should be considered valid
if they consist of four octets, with values between 0 and 255, inclusive.

Note: Create the decorator that validates if the passed to inner function ip value is correct.
In case of incorrect ip format, user should see the error message.

Examples of correct ip addresses: 1.2.3.4, 123.45.67.89
Examples of incorrect ip addresses: 1.2.3, 1.2.3.4.5, 123.456.78.90, 123.045.067.089"""


input_text = input("Input: ")
error_mess = "Incorrect ip addresses:"


def my_decorator(func):
    def wrapper(input_text):
        list_num_ip = input_text.split(".")
        if len(list_num_ip) != 4:
            print(error_mess)
            return func(input_text)

        for i in list_num_ip:
            if i.isdigit():
                if i[0] == "0" or int(i) < 0 or int(i) > 255:
                    print(error_mess)
                    return func(input_text)
            else:
                print(error_mess)
                return func(input_text)

        print("Correct ip addresses:")
        return func(input_text)

    return wrapper


@my_decorator
def PrintIp(arg_ip):
    print(arg_ip)


PrintIp(input_text)
