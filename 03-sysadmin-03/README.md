### Операционные системы. Лекция 1
1. `cd` вызывает системную ф-цию `chdir()`:
    ```
    <...cut..>
    rt_sigprocmask(SIG_BLOCK, NULL, [], 8)  = 0
    rt_sigprocmask(SIG_BLOCK, NULL, [], 8)  = 0
    stat("/tmp", {st_mode=S_IFDIR|S_ISVTX|0777, st_size=4096, ...}) = 0
    chdir("/tmp")                           = 0
    rt_sigprocmask(SIG_BLOCK, [CHLD], [], 8) = 0
    rt_sigprocmask(SIG_SETMASK, [], NULL, 8) = 0
    exit_group(0)                           = ?
    +++ exited with 0 +++
    ```


2. Выполням strace file:
    ```
    vagrant@vagrant:~$ strace -e trace=openat file /bin/bash 
    openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
    openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libmagic.so.1", O_RDONLY|O_CLOEXEC) = 3
    openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
    openat(AT_FDCWD, "/lib/x86_64-linux-gnu/liblzma.so.5", O_RDONLY|O_CLOEXEC) = 3
    openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libbz2.so.1.0", O_RDONLY|O_CLOEXEC) = 3
    openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libz.so.1", O_RDONLY|O_CLOEXEC) = 3
    openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
    openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
    openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
    openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
    openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
    openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3
    openat(AT_FDCWD, "/bin/bash", O_RDONLY|O_NONBLOCK) = 3
    ```
    Исключая библиотеки, видим, что программа ищет файлы с базой по путям `/etc/magic.mgc`, `/etc/magic` и `/usr/share/misc/magic.mgc`. В последнем файле и расположена основная база сигнатур, которой пользуется программа.  

3. Чтобы найти удалённые, но открытые файлы, выполняем команду `lsof +L1`. Выясняем из её вывода PID нужного нам процесса и FD файла, который необходимо обнулить.
После чего выполняем `: > /proc/$PID/fd/$FD` подставив соответствующие значения PID и FD.


4. Зомби-процессы ресурсов не занимают, за исключением памяти, выделенной под структуру дескриптора процесса и места в таблице процессов, размер которой ограничен.


5. Выполняем команду `strace -tt -e trace=openat opensnoop-bpfcc >trace.log 2>&1`. Чтобы не загромождать текст, фрагмент файла, содержащий вызовы open() за первую секунду, приведён [отдельно](trace.log).


6. Программа `uname` использует одноимённый системный вызов `uname()`. Согласно секции 'NOTES' `man 2 uname`,
"Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}.".


7. В списке, разделённом ";" команды выполняются последовательно, независимо от результата предыдущей. В списке, разделённом "&&", следующая команда выполнится только при условии, что предыдущая завершилась успехом.
Осмыысленных вариантов использовать `&&` при включенной опции `-e` придумать не могу.


8. Режим `set -euxo pipefail` состоит из следующих опций:
   - -e - Немедленно завершать работу, если какая-либо команда в списке завершилась ошибкой (ненулевым статусом выхода);
   - -u - При подстановке значений параметров рассматривать не установленную переменную как ошибку.
   - -x - После подстановок в каждой простой команде выдавать значение переменной PS4, 
   а затем - команду с результатами подстановок в аргументах.
   - -o pipefail - если установлен, то кодом возврата конвейера становится код возврата последней команды, завершившейся с ненулевым статусом.

   Данный набор опций позволяет в определённой степени "автоматизировать" обработку ошибок, а опция `-x` поможет при отладке. 
Однако, относительно правильности такого подхода существуют разные [мнения](http://mywiki.wooledge.org/BashFAQ/105).
Действительно, при таком подходе всегда необходимо помнить,
что ошибка с точки зрения оболочки далеко не всегда может означать ошибку сточки зрения логики работы.   

9. Выполняем `ps`:
   ```
   vagrant@vagrant:~$ ps -axo stat|cut -c-1|sort|uniq -c
        46 I
         1 R
        69 S
   ```
Видим, что больше всего у нас процессов в состоянии "interruptible sleep", что логично, т.к. система "чистая", работающих и нагруженных чем-либо служб в ней нет.