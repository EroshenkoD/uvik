import socket


HOST = "127.0.0.1"
PORT = 65432


if __name__ == "__main__":

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        conn, addr = server_socket.accept()

        with open('server.jpg', 'wb') as img:
            img_data = conn.recv(1024)
            while img_data:
                img.write(img_data)
                img_data = conn.recv(1024)

