import argparse
import socket
import time

from multiprocessing import Process


def bind_tcp(host, port, tcp_backlog):
    # Bind to the TCP port
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    # NOTE: Linux supports socket.SO_REUSEPORT only in 3.9 and later releases.
    try:
        sock_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except Exception:
        pass

    sock_tcp.setblocking(True)
    sock_tcp.bind((host, port))
    sock_tcp.listen(tcp_backlog)

    return sock_tcp


class Hello(Process):
    def __init__(self, addr=None, fd=None):
        super(Hello, self).__init__()
        self.fd = fd
        self.addr = addr

    def get_socket(self):
        if self.fd:
            return socket.fromfd(self.fd, socket.AF_INET, socket.SOCK_STREAM)
        else:
            host, port = self.addr
            return bind_tcp(host, port, 1)

    def run(self):
        s = self.get_socket()
        while True:
            conn, (host, port) = s.accept()
            print('[%s] Connected: %s:%s' % (self.pid, host, port))
            data = conn.recv(1024)
            conn.sendall('Hello %s' % data)
            conn.close()


def server(socket_by='fd', procs=3):
    host, port = '0.0.0.0', 9999
    backlog = 1
    if socket_by == 'fd':
        s = bind_tcp(host, port, backlog)
        fd = s.fileno()
        kw = dict(fd=fd)
    else:
        kw = dict(addr=(host, port))

    pool = []
    if procs > 1:
        for i in range(0, procs):
            proc = Hello(**kw)
            proc.start()
            pool.append(proc)

    try:
        while True:
            time.sleep(1)

    except (KeyboardInterrupt, SystemExit):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('reuse_by', help='Reuse the socket by fd or address')
    parser.add_argument('--num-procs', '-p', default=3)
    args = parser.parse_args()
    server(args.reuse_by, procs=args.num_procs)


if __name__ == '__main__':
    main()
