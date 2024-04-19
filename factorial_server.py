from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


HOST: str = '127.0.0.1'
PORT: int = 2345


def factorial(num: int) -> int:
    if 0 > num > 100:
        raise ValueError('Number must be greater than 0 and less than 100')
    if num == 1 or num == 0:
        return 1
    else:
        return num * factorial(num - 1)


def factorial_server() -> None:
    sock: socket = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f'Waiting for connection on {PORT} port')
    conn, addr = sock.accept()
    print(f'Connected by {addr}')
    conn.sendall(b'Please enter a number')
    number = conn.recv(1024)
    num_factorial: int = factorial(int(number))
    conn.sendall(str(num_factorial).encode())
    conn.close()
    sock.close()


if __name__ == '__main__':
    factorial_server()
