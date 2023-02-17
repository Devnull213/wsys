#!/usr/bin/env python3
""" Module that provides information about the OS by the ttl information"""
import argparse
import re
import subprocess


def get_ttl(ip_or_domain: str) -> tuple:
    """
    Returns the ttl value from the ping command aplied to a given ip address or domain

        Parameters: 
            ip_or_domain (string): Ip address or web domain

        Returns:
            integer ttl value
    """
    proc = subprocess.run(
        ["ping", "-c", "1", "-w", "2", ip_or_domain], capture_output=True, check=True
    )
    try:
        search = re.search("ttl=[0-9]{2,3}", proc.stdout.decode())
        return (int(search.group()[4:]), ip_or_domain)
    except ValueError as exc:
        raise ValueError(exc) from exc


def detect_os(ttl: int, ip_or_domain: str) -> str:
    """
    Evaluate the OS by the ttl value

        Parameters:
            ttl (int): ttl value from a ping command
            ip_or_domain: Ip address or web domain

        Returns: 
            String with the detected OS
    """
    if ttl <= 64:
        return f"""
        [*] ttl = {ttl} -> OS Linux
        [*] There\'s {64 - ttl} nodes between your machine and the objective -> {ip_or_domain}."""

    if 128 >= ttl >= 64:
        return f"""
        [*] ttl = {ttl} -> OS Windows
        [*] There\'s {128 - ttl} nodes between your machine and the objective -> {ip_or_domain}."""

    return "The OS cannot be detected."


def main() -> None:
    """Main execution function"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        dest="ip_address",
        help="This argument require and should be an ip address or web domain.",
    )
    args = parser.parse_args()

    ttl, ip_address = get_ttl(args.ip_address)
    print(detect_os(ttl, ip_address))


if __name__ == "__main__":

    main()
