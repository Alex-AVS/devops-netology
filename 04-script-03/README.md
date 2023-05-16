# Домашнее задание к занятию «Языки разметки JSON и YAML»

### Цель задания

В результате выполнения задания вы:

* познакомитесь с синтаксисами JSON и YAML;
* узнаете, как преобразовать один формат в другой при помощи пары строк.

### Чеклист готовности к домашнему заданию

1. Установлена библиотека PyYAML для Python 3.

### Инструкция к заданию 

1. Скопируйте в свой .md-файл содержимое этого файла, исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-03-yaml/README.md).
3. Заполните недостающие части документа решением задач — заменяйте `???`, остальное в шаблоне не меняйте, чтобы не сломать форматирование текста, подсветку синтаксиса. Вместо логов можно вставить скриншоты по желанию.
4. Любые вопросы по выполнению заданий задавайте в чате учебной группы или в разделе «Вопросы по заданию» в личном кабинете.

### Дополнительные материалы

1. [Полезные ссылки для модуля «Скриптовые языки и языки разметки».](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/04-script-03-yaml/additional-info)

------

## Задание 1

Мы выгрузили JSON, который получили через API-запрос к нашему сервису:

```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
  Нужно найти и исправить все ошибки, которые допускает наш сервис.

### Ваш скрипт:
Синтаксически так, только 7175 - это не IP и первый элемент не имеет смысла.
```
     { "info" : "Sample JSON output from our service\t", 
        "elements" :[
            { 
                "name" : "first",
                "type" : "server",
                "ip" : 7175 
            },
            { 
                "name" : "second",
                "type" : "proxy",
                "ip" : "71.78.22.43"
            }
        ]
    }
```

---

## Задание 2

В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML-файлов, описывающих наши сервисы. 

Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. 

Формат записи YAML по одному сервису: `- имя сервиса: его IP`. 

Если в момент исполнения скрипта меняется IP у сервиса — он должен так же поменяться в YAML и JSON-файле.

### Ваш скрипт:

```python
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
```

### Вывод скрипта при запуске во время тестирования:

```
C:\Users\AlexSyS\AppData\Local\Programs\Python\Python38\python.exe E:\PROJECTS\netology-devops\devops-netology\04-script-03\checkhosts.py 
Файл ./hosts.json не найден. Создаём.
Файл ./hosts.yaml не найден. Создаём.
[ERROR] drive.google.com IP mismatch: 0.0.0.0 172.217.168.238
[ERROR] mail.google.com IP mismatch: 0.0.0.0 142.250.179.197
[ERROR] google.com IP mismatch: 0.0.0.0 142.250.179.206
drive.google.com - 172.217.168.238
mail.google.com - 142.250.179.197
google.com - 142.250.179.206

Process finished with exit code 0

```

### JSON-файл(ы), который(е) записал ваш скрипт:

```json
{
    "drive.google.com": "172.217.168.238",
    "mail.google.com": "142.250.179.197",
    "google.com": "142.250.179.206"
}
```

### YAML-файл(ы), который(е) записал ваш скрипт:

```yaml
drive.google.com: 172.217.168.238
google.com: 142.250.179.206
mail.google.com: 142.250.179.197

```

---

## Задание со звёздочкой* 

Это самостоятельное задание, его выполнение необязательно.
____

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:

   * принимать на вход имя файла;
   * проверять формат исходного файла. Если файл не JSON или YAML — скрипт должен остановить свою работу;
   * распознавать, какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны;
   * перекодировать данные из исходного формата во второй доступный —  из JSON в YAML, из YAML в JSON;
   * при обнаружении ошибки в исходном файле указать в стандартном выводе строку с ошибкой синтаксиса и её номер;
   * полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов.

### Ваш скрипт:

```python
???
```

### Пример работы скрипта:

???

----

### Правила приёма домашнего задания

В личном кабинете отправлена ссылка на .md-файл в вашем репозитории.

-----

### Критерии оценки

Зачёт:

* выполнены все задания;
* ответы даны в развёрнутой форме;
* приложены соответствующие скриншоты и файлы проекта;
* в выполненных заданиях нет противоречий и нарушения логики.

На доработку:

* задание выполнено частично или не выполнено вообще;
* в логике выполнения заданий есть противоречия и существенные недостатки.  
 
Обязательными являются задачи без звёздочки. Их выполнение необходимо для получения зачёта и диплома о профессиональной переподготовке.

Задачи со звёздочкой (*) являются дополнительными или задачами повышенной сложности. Они необязательные, но их выполнение поможет лучше разобраться в теме.