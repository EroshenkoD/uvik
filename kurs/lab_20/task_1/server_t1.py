import socket


host = ''
port = 12000


def get_solution(data):
    operation = ('+', '-', '*', '/')
    work_data = data.split(" ")
    if len(work_data) != 3:
        return f"Not valid input data {data}"
    operand = work_data[1]
    if operand not in operation:
        return f"I don't know about this operation {operand}"
    try:
        first_operand = int(work_data[0])
        second_operand = int(work_data[2])
    except ValueError as e:
        return 'I work only with numbers'

    if operand == "+":
        res = first_operand + second_operand
    elif operand == "-":
        res = first_operand - second_operand
    elif operand == "*":
        res = first_operand * second_operand
    else:
        res = first_operand / second_operand
    return str(res)


if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))

        while True:
            message, address = server_socket.recvfrom(1024)
            mess = message.decode('utf-8')
            if mess == 'exit':
                break
            mess = get_solution(mess)
            server_socket.sendto(mess.encode('utf-8'), address)

