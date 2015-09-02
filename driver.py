import argparse
import time
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('reuse_method')
    args = parser.parse_args()

    servers = subprocess.Popen([
        'python', '/code/server.py', args.reuse_method
    ])
    time.sleep(2)
    print('Started servers')
    subprocess.call('ps afx', shell=True)

    client = subprocess.Popen(['python', '/code/client.py', '10'])
    client.wait()
    servers.kill()


if __name__ == '__main__':
    main()
