from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

HOST: str = '127.0.0.1'
PORT: int = 1357


def calculate(num1: int, num2: int) -> str:
    return (f'{num1} + {num2} = {num1 + num2}\n'
            f'{num1} - {num2} = {num1 - num2}\n'
            f'{num1} * {num2} = {num1 * num2}\n'
            f'{num1} / {num2} = {num1 / num2: .2f}\n')


def calculation_server() -> None:
    sock: socket = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f'Waiting for connection on {PORT} port')
    conn, addr = sock.accept()
    print(f'Connected by {addr}')
    conn.sendall(b'Please enter first number\n')
    first_num = conn.recv(1024)
    conn.sendall(b'Enter second number\n')
    second_num = conn.recv(1024)
    result: str = calculate(int(first_num), int(second_num))
    conn.sendall(result.encode())
    conn.close()
    sock.close()


if __name__ == '__main__':
    calculation_server()
