"""
John keeps a backup of his old personal phone book as a text file. On each line of the file he can find
the phone number (formated as +X-abc-def-ghij where X stands for one or two digits),
the corresponding name between < and > and the address.

Unfortunately everything is mixed, things are not always in the same order; parts of lines are cluttered with
non-alpha-numeric characters (except inside phone number and name).

Examples of John's phone book lines:

"/+1-541-754-3010 156 Alphand_St. <J Steeve>\n"

" 133, Green, Rd. <E Kustur> NY-56423 ;+1-541-914-3010!\n"

"<Anastasia> +48-421-674-8974 Via Quirinal Roma\n"
Could you help John with a program that, given the lines of his phone book and a phone number num returns
a string for this number : "Phone => num, Name => name, Address => adress"

Input: "/+1-541-754-3010 156 Alphand_St. <J Steeve>\n 133, Green, Rd. <E Kustur> NY-56423 ;+1-541-914-3010!\n",
"1-541-754-3010"
Output: Phone => 1-541-754-3010, Name => J Steeve, Address => 156 Alphand St.
Note: It can happen that there are many people for a phone number num, then return : "Error => Too many people: num"

or it can happen that the number num is not in the phone book, in that case return: "Error => Not found: num"
"""
import re
from functools import lru_cache


def read_file(file_name):
    with open(file_name) as file:
        for row in file:
            yield row


class GetPersonDataError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


@lru_cache(maxsize=128)
def get_person_data(text_row):
    res = ""

    phone_numb = re.search(r'[+]\d{,2}[-]\d{3}[-]\d{3}[-]\d{4}', text_row)
    if phone_numb:
        res += f'Phone => {phone_numb.group(0)[1:]}, '
        text_row = text_row.replace(phone_numb.group(0), "")
    else:
        raise GetPersonDataError("Error => Not found: num")

    name_list = re.findall(r'[<][^<>]{0,}[>]', text_row)
    if len(name_list) == 1:
        res += f'Name => {name_list[0][1:-1:]}, '
        text_row = text_row.replace(name_list[0], "")
    else:
        raise GetPersonDataError("Error => Too many people: num")

    address = re.sub(r'[^a-zA-Z,\d, \.,-]', " ", text_row)
    address = address.split(" ")
    address = [i for i in address if i != ""]
    address = " ".join(address)
    res += f'Address => {address}'

    return res


if __name__ == "__main__":

    gen_text = read_file('5_2.txt')

    while True:
        try:
            text_to_decoder = next(gen_text)
            print(get_person_data(text_to_decoder))
        except StopIteration:
            break
        except GetPersonDataError as e:
            print(e)
    print(get_person_data.cache_info())
