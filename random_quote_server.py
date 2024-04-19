from random import choice
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR


HOST: str = '127.0.0.1'
PORT: int = 1234


def random_quote() -> str:
    quotes: list = [
        "The greatest glory in living lies not in never falling, but in rising every time we fall.",
        "The way to get started is to quit talking and begin doing.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "If you set your goals ridiculously high and it's a failure, "
        "you will fail above everyone else's success.",
        "You may say I'm a dreamer, but I'm not the only one. "
        "I hope someday you'll join us. And the world will live as one.",
        "You must be the change you wish to see in the world.",
        "Well done is better than well said.",
        "It is during our darkest moments that we must focus to see the light.",
        "Be yourself; everyone else is already taken.",
        "Only a life lived for others is a life worthwhile.",
        "Hello World!"
    ]

    return choice(quotes) + '\n'


def random_quote_server() -> None:
    sock: socket = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f'Waiting for connection on {PORT} port')
    conn, addr = sock.accept()
    print(f'Connected by {addr}')
    quote: str = random_quote()
    conn.sendall(quote.encode())
    conn.close()
    sock.close()


if __name__ == '__main__':
    random_quote_server()
