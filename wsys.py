#!/usr/bin/env python3

import subprocess
import re 
import argparse

def get_ttl(ip) -> int:
    '''Takes an ip address and return the vulue'''
    proc = subprocess.run(['ping', '-c', '1', '-w', '2', ip], capture_output = True)
    search = re.search('ttl=\d{2,3}', proc.stdout.decode())
    return search.group()[4:]

def detect_os(ttl, ip):
    ''' Evaluation of OS by the ttl value'''
    if int(ttl) <= 64 and int(ttl) >= 0:
        return f'''[*] ttl = {ttl} -> OS Linux\n[*] There\'s {64 - int(ttl)} nodes between your machine and the objective -> {ip}.'''

    elif int(ttl) <= 128 and int(ttl) >= 64:
        return f'''[*] ttl = {ttl} -> OS Windows\n[*] There\'s {128 - int(ttl)} nodes between your machine and the objective -> {ip}.'''

    else:
        return 'The OS cannot be detected.'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest= "ip_address", help="This argument require and should be an ip address or web domain.")
    args = parser.parse_args()

    ttl = get_ttl(args.ip_address)
    print(detect_os(ttl, args.ip_address))


if __name__ == '__main__':

    main()

