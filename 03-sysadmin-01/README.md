# Работа в терминале. Лекция 1
Для выполнения следующих пунктов, требующих работы с man bash, выполняем команду 

`man -P "less -N" bash`.
5. - максимальное число строк в журнале задаётся переменной `HISTFILESIZE`. Строка 587.
   - директива `ignoreboth` используется в переменной `HISTCONTROL` и контролирует, как сохраняются команды в истории. Её наличие означает, что команды, начинающиеся с пробела, а так же строки, дублирующие уже имеющиеся в журнале, не будут сохраняться. Является аналогом директив `ignorespace + ignoredups`.
6. Фигурные скобки `{}` используются для: 
- группировки команд (строка 196) в т.ч. при определении функций (стр. 293)
- создания массивов строк (brace expansion) (стр. 741)
- экранирования переменных от окружающего текста: `${VAR}aaa <> $VARaaa' во воторм случае подстановки не будет. (стр. 793)
- раскрытия/модификации переменных (variable expansion) - задание значений по умолчанию, строковые операции и т.д. (стр. 806)
7. Создать однократным вызовом touch 100 000 файлов можно при помощи команды 
` touch file{1..100000}`. 
Создать таким образом 300k файлов не выйдет, т.к. кончится память под аргументы команды и она завершится с ошибкой 'Argument list too long' (раскрытие массива `{1..N}` приводит к появлению N аргументов 'fileXXX').
Хотя, если посмотреть внимательнее, то можно заметить, что минимальный массив только из цифр сильно меньше лимита:
   ```
   vagrant@vagrant:/tmp/mybash$ xargs --show-limits
   Your environment variables take up 2168 bytes
   POSIX upper limit on argument length (this system): 2092936
   POSIX smallest allowable upper limit on argument length (all systems): 4096
   Maximum length of command we could actually use: 2090768
   Size of command buffer we are actually using: 131072
   Maximum parallelism (--max-procs must be no greater): 2147483647
   
   vagrant@vagrant:/tmp/mybash$ echo {1..300000} >zzz
   vagrant@vagrant:/tmp/mybash$ ls -l
   total 1944
   lrwxrwxrwx 1 vagrant vagrant       9 Mar 27 18:05 bash -> /bin/bash
   -rw-rw-r-- 1 vagrant vagrant 1988895 Mar 27 20:57 zzz
   ```
   Но даже так ошибка есть. Невозможно выделить на стеке единый кусок такого размера?


8. `[[ -d /tmp ]]` проверяет существование каталога /tmp на файловой системе. 
9. Создаём временный каталог, делаем в нём символическую ссылку на оригинальный файл bash и прописываем наш путь в начало переменной PATH:
   ```
   mkdir /tmp/mybash
   ln -s /bin/bash /tmp/mybash/
   export PATH=/tmp/mybash:$PATH 
   ```
   выполняем `type -a bash` и получаем следующий вывод:
   ```
   bash is /tmp/mybash/bash
   bash is /usr/bin/bash
   bash is /bin/bash
   ```
10. `at` исполняет команды в заданое время, а `batch` - во время низкой загрузки/простоя системы (согласно man, по умолчанию - когда load average становится < 1.5 )