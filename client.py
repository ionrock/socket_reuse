import argparse
import socket


def client():
    addr = '0.0.0.0', 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    s.sendall('eric')
    data = s.recv(1024)
    s.close()
    print(repr(data))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('times', type=int, default=3)
    args = parser.parse_args()

    for i in range(args.times):
        client()


if __name__ == '__main__':
    main()
