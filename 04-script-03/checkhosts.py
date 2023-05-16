#!/usr/bin/env python3

import socket
import time
import json
import yaml
import time

hosts = {"drive.google.com": "0.0.0.0", "mail.google.com": "0.0.0.0", "google.com": "0.0.0.0"}


def load_json():
    try:
        config_json = open('./hosts.json', 'r+')
        try:
            hosts_json = json.load(config_json)
            print(f"Файл ./hosts.json загружен.")
        except json.decoder.JSONDecodeError as e:
            print(f"Неверный формат файла ./hosts.json.")
            config_json.close
            exit()
        config_json.close
    except FileNotFoundError as e:
        print(f'Файл {e.filename} не найден. Создаём.')
        config_json = open(e.filename, 'w+')
        try:
            config_yaml = open('./hosts.yaml', 'r+')
            hosts_yaml = yaml.load(config_yaml, Loader=yaml.SafeLoader)
            config_json.write(json.dumps(hosts_yaml, indent=4))
            config_json.close
            hosts_json = hosts_yaml
        except FileNotFoundError:
            config_json.write(json.dumps(hosts, indent=4))
            hosts_json = hosts
            config_json.close
        except:
                print('Ошибка.')
                exit()

    return hosts_json


def load_yaml():
    try:
        config_yaml = open('./hosts.yaml', 'r+')
        try:
            hosts_yaml = yaml.load(config_yaml, Loader=yaml.SafeLoader)
            print(f"Файл ./hosts.yaml загружен.")
        except yaml.scanner.ScannerError as e:
            print(f"Неверный формат файла ./hosts.yaml.")
            config_yaml.close
            exit()
        config_yaml.close
    except FileNotFoundError as e:
        print(f'Файл {e.filename} не найден. Создаём.')
        config_yaml = open(e.filename, 'w+')
        try:
            config_json = open('./hosts.json', 'r+')
            hosts_json = json.load(config_json)
            config_yaml.write(yaml.dump(hosts_json))
            hosts_yaml = hosts_json
            config_yaml.close
        except FileNotFoundError:
            config_yaml.write(yaml.dump(hosts))
            hosts_yaml = hosts
            config_yaml.close
        except:
                print('Ошибка.')
                exit()

    return hosts_yaml


hosts_json = load_json()
hosts_yaml = load_yaml()

if hosts_yaml != hosts_json:
    print(f"""\nНабор хостов в json и yaml отличается:\n\njson: {hosts_json}\nyaml: {hosts_yaml}\n""")
    exit()
else:

    hosts = hosts_json
    try:
        while True:
            for host in hosts:
                last_ip = hosts[host]
                new_ip = socket.gethostbyname(host)
                if new_ip != last_ip:
                    print(
                        f"""[ERROR] {host} IP mismatch: {last_ip} {new_ip}""")
                    hosts[host] = new_ip
                    write_json = open("./hosts.json", 'w+')
                    write_yaml = open("./hosts.yaml", 'w+')
                    write_json.write(json.dumps(hosts, indent=4))
                    write_yaml.write(yaml.dump(hosts))
                    write_json.close()
                    write_yaml.close()
                else:
                    print(f"""{host} - {last_ip}""")
            time.sleep(5)

    except KeyboardInterrupt:
        exit()