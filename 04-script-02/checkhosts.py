# /usr/bin/env python3

import socket
import time

hosts = {"drive.google.com": "0.0.0.0", "mail.google.com": "0.0.0.0", "google.com": "0.0.0.0"}

while True:
    for host in hosts.keys():
        last_ip = hosts[host]
        new_ip = socket.gethostbyname(host)
        if last_ip != new_ip:
            print(f"[ERROR] {host} IP mismatch: {new_ip} {last_ip}")
            hosts[host] = new_ip
        else:
            print(f"{host} - {new_ip}")
    time.sleep(5)
