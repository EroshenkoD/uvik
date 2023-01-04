import time
import socket


addr = ("127.0.0.1", 12000)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(1.0)

        while True:
            message = input("Enter expression for our calculator separated by a space or enter 'exit': ")
            start = time.time()
            client_socket.sendto(message.encode('utf-8'), addr)
            if message == 'exit':
                print("Thanks for using our calculator")
                break
            try:
                data, server = client_socket.recvfrom(1024)
                data = data.decode('utf-8')
                end = time.time()
                elapsed = end - start
                print(f"You'r expression: {message}\nOur solution: {data}\nSolution time: {elapsed}")
            except socket.timeout:
                print('REQUEST TIMED OUT')
                break
            except ConnectionResetError:
                print("Calculator out of reach")
                break
