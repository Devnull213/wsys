#!/usr/bin/env python3

import subprocess, re, sys


def get_ttl(ip):
    proc = subprocess.run(['ping', '-c', '1', '-w', '2', ip], capture_output = True)
    search = re.search('ttl=\d{2,3}', proc.stdout.decode())
    return search.group()[4:]

def detect_os(ttl, ip):
    if int(ttl) <= 64 and int(ttl) >= 0:
        return f'''[*] ttl = {ttl} -> OS Linux\n[*] There\'s {64 - int(ttl)} nodes between your machine and the objective -> {ip}.'''

    elif int(ttl) <= 128 and int(ttl) >= 64:
        return f'''[*] ttl = {ttl} -> OS Windows\n[*] There\'s {128 - int(ttl)} nodes between your machine and the objective -> {ip}.'''

    else:
        return 'The OS cannot be detected.'

def main():
    if len(sys.argv) != 2:
        print('[!] Usage: wsys <IP_ADDRESS>, example -> wsys 8.8.8.8')
    else:
        ttl = get_ttl(sys.argv[1])
        print(detect_os(ttl, sys.argv[1]))


if __name__ == '__main__':

    main()


