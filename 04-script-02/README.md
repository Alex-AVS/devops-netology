# Домашнее задание к занятию «Использование Python для решения типовых DevOps-задач»

### Цель задания

В результате выполнения задания вы:

* познакомитесь с синтаксисом Python;
* узнаете, для каких типов задач его можно использовать;
* воспользуетесь несколькими модулями для работы с ОС.


### Инструкция к заданию

1. Установите Python 3 любой версии.
2. Скопируйте в свой .md-файл содержимое этого файла, исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-02-py/README.md).
3. Заполните недостающие части документа решением задач — заменяйте `???`, остальное в шаблоне не меняйте, чтобы не сломать форматирование текста, подсветку синтаксиса. Вместо логов можно вставить скриншоты по желанию.
4. Для проверки домашнего задания в личном кабинете прикрепите и отправьте ссылку на решение в виде md-файла в вашем репозитории.
4. Любые вопросы по выполнению заданий задавайте в чате учебной группы или в разделе «Вопросы по заданию» в личном кабинете.

### Дополнительные материалы

1. [Полезные ссылки для модуля «Скриптовые языки и языки разметки».](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/04-script-03-yaml/additional-info)

------

## Задание 1

Есть скрипт:

```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:

| Вопрос  | Ответ                                                                                                                                                  |
| ------------- |--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Какое значение будет присвоено переменной `c`?  | Переменная не будет объявлена, т.к. возникнет ошибка TypeError: unsupported operand type(s) for +: 'int' and 'str'.<br/>Нельзя 'сложить' число и строку. |
| Как получить для переменной `c` значение 12?  | Если строкой, то c = str(a) + b, если число то c = (a + int(b)) * int(b) * int(b)                                                                                                      |
| Как получить для переменной `c` значение 3?  | c = a + int(b)                                                                                                                                                    |

------

## Задание 2

Мы устроились на работу в компанию, где раньше уже был DevOps-инженер. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. 

Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:

```python
#!/usr/bin/env python3

import os
import subprocess
import re

path = "~/netology/sysadm-homeworks"
expanded_path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
#На винде `cd` в popen() не отрабатывает, поэтому так
result_os = subprocess.run(["git", "status", "-s"], cwd=expanded_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
#Не уверен,что нужно всё. Если только непосредственно изменённные, то оставить только М и АМ соотв-но
mod_types = {"A\s": "new", "\sM": "modified", "AM": "modified new", "\sD": "deleted", "R\s": "renamed", "\?\?": "untracked"}

for result in result_os.split("\n"):
     for key in mod_types.keys():
        regexp = re.compile(r"^" + key + "\s*")
        if regexp.search(result):
            prepare_result = re.sub(regexp, '', result).split(' -> ')

            if mod_types[key] == 'renamed':
                print(f'{mod_types[key]}:\t {os.path.join(expanded_path, prepare_result[1])} <- {prepare_result[0]}')
            else:
                print(f'{mod_types[key]}:\t {os.path.join(expanded_path, prepare_result[0])}')
```

### Вывод скрипта при запуске во время тестирования:

```
C:\Users\AlexSyS\AppData\Local\Programs\Python\Python38\python.exe E:\PROJECTS\netology-devops\devops-netology\04-script-02\test.py 
deleted:	 C:\Users\AlexSyS\netology\sysadm-homeworks\01-intro-01/netology.jsonnet
deleted:	 C:\Users\AlexSyS\netology\sysadm-homeworks\01-intro-01/netology.sh
new:	 C:\Users\AlexSyS\netology\sysadm-homeworks\01-intro-01/netology_.sh
renamed:	 C:\Users\AlexSyS\netology\sysadm-homeworks\01-intro-01/netology_2.yaml <- 01-intro-01/netology.yaml
modified:	 C:\Users\AlexSyS\netology\sysadm-homeworks\04-script-03-yaml/README.md
modified:	 C:\Users\AlexSyS\netology\sysadm-homeworks\README.md
modified new:	 C:\Users\AlexSyS\netology\sysadm-homeworks\addd
untracked:	 C:\Users\AlexSyS\netology\sysadm-homeworks\ddd
untracked:	 C:\Users\AlexSyS\netology\sysadm-homeworks\netology.jsonnet

Process finished with exit code 0
```

------

## Задание 3

Доработать скрипт выше так, чтобы он не только мог проверять локальный репозиторий в текущей директории, но и умел воспринимать путь к репозиторию, который мы передаём, как входной параметр. Мы точно знаем, что начальство будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:

```python
#!/usr/bin/env python3

import os
import sys
import subprocess
import re

try:
    path = sys.argv[1]
except IndexError:
    print("Укажите путь к репозиторию.")
    exit()
    
expanded_path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))

try:
    result_os = subprocess.run(["git", "status", "-s"], cwd=expanded_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
except (FileNotFoundError, NotADirectoryError):
    print(
        f'Путь {expanded_path} не найден'
    )
    exit()

if result_os.find('fatal:') >= 0:
    print(
        f'В папке {expanded_path} репозиторий git не найден.')
    exit()

mod_types = {"A\s": "new", "\sM": "modified", "AM": "modified new", "\sD": "deleted", "R\s": "renamed", "\?\?": "untracked"}

for result in result_os.split("\n"):
     for key in mod_types.keys():
        regexp = re.compile(r"^" + key + "\s*")
        if regexp.search(result):
            prepare_result = re.sub(regexp, '', result).split(' -> ')

            if mod_types[key] == 'renamed':
                print(f'{mod_types[key]}:\t {os.path.join(expanded_path, prepare_result[1])} <- {prepare_result[0]}')
            else:
                print(f'{mod_types[key]}:\t {os.path.join(expanded_path, prepare_result[0])}')


```

### Вывод скрипта при запуске во время тестирования:

Неверный путь:
```
C:\Users\AlexSyS\AppData\Local\Programs\Python\Python38\python.exe E:\PROJECTS\netology-devops\devops-netology\04-script-02\test.py "~/netology/bubuka" 
Путь C:\Users\AlexSyS\netology\bubuka не найден

Process finished with exit code 0

```
Без репозитория:
```
C:\Users\AlexSyS\AppData\Local\Programs\Python\Python38\python.exe E:\PROJECTS\netology-devops\devops-netology\04-script-02\test.py "~/netology/" 
В папке C:\Users\AlexSyS\netology репозиторий git не найден.

Process finished with exit code 0
```
Нормальный запуск:
```
C:\Users\AlexSyS\AppData\Local\Programs\Python\Python38\python.exe E:\PROJECTS\netology-devops\devops-netology\04-script-02\test.py "~/netology/sysadm-homeworks" 
deleted:	 C:\Users\AlexSyS\netology\sysadm-homeworks\01-intro-01/netology.jsonnet
deleted:	 C:\Users\AlexSyS\netology\sysadm-homeworks\01-intro-01/netology.sh
new:	 C:\Users\AlexSyS\netology\sysadm-homeworks\01-intro-01/netology_.sh
renamed:	 C:\Users\AlexSyS\netology\sysadm-homeworks\01-intro-01/netology_2.yaml <- 01-intro-01/netology.yaml
modified:	 C:\Users\AlexSyS\netology\sysadm-homeworks\04-script-03-yaml/README.md
modified:	 C:\Users\AlexSyS\netology\sysadm-homeworks\README.md
modified new:	 C:\Users\AlexSyS\netology\sysadm-homeworks\addd
untracked:	 C:\Users\AlexSyS\netology\sysadm-homeworks\ddd
untracked:	 C:\Users\AlexSyS\netology\sysadm-homeworks\netology.jsonnet

Process finished with exit code 0
```
------

## Задание 4

Наша команда разрабатывает несколько веб-сервисов, доступных по HTTPS. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. 

Проблема в том, что отдел, занимающийся нашей инфраструктурой, очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS-имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. 

Мы хотим написать скрипт, который: 

- опрашивает веб-сервисы; 
- получает их IP; 
- выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. 

Также должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена — оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:

```python
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
```

### Вывод скрипта при запуске во время тестирования:

```
C:\Users\AlexSyS\AppData\Local\Programs\Python\Python38\python.exe E:\PROJECTS\netology-devops\devops-netology\04-script-02\checkhosts.py 
[ERROR] drive.google.com IP mismatch: 172.217.168.238 0.0.0.0
[ERROR] mail.google.com IP mismatch: 142.250.179.197 0.0.0.0
[ERROR] google.com IP mismatch: 142.250.179.206 0.0.0.0
drive.google.com - 172.217.168.238
mail.google.com - 142.250.179.197
google.com - 142.250.179.206
```

------

## Задание со звёздочкой* 

Это самостоятельное задание, его выполнение необязательно.
___

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в GitHub и пользуется Gitflow, то нам приходится каждый раз: 

* переносить архив с нашими изменениями с сервера на наш локальный компьютер;
* формировать новую ветку; 
* коммитить в неё изменения; 
* создавать pull request (PR); 
* и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. 

Мы хотим максимально автоматизировать всю цепочку действий. Для этого: 

1. Нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к GitHub, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым).
1. При желании можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. 
1. С директорией локального репозитория можно делать всё, что угодно. 
1. Также принимаем во внимание, что Merge Conflict у нас отсутствуют, и их точно не будет при push как в свою ветку, так и при слиянии в master. 

Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 

### Ваш скрипт:

```python
???
```

### Вывод скрипта при запуске во время тестирования:

```
???
```

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