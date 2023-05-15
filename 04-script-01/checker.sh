#!/usr/bin/env bash

#массив проверяемых хостов
hosts=("192.168.0.1" "173.194.222.113" "87.250.250.242")

num_tries=5     #число попыток
log=./log       #файл журнала
err_log=./error #файл ошибок
#Добавили внешний бесконечный цикл
while ((1==1))
do
    for host in ${hosts[@]}
    do
        echo checking $host...
        echo -n "$host" >>$log

        i=0

        while (($i < $(($num_tries))))
        do
            echo -n "$i of $num_tries:"
            curl -s --max-time 3 http://$host:80 2>&1 >/dev/null
            #в принципе, если подразумевается 5 _попыток_, то команду можно изменить на
            # "curl -s --retry $num_tries --retry-delay 0 ----retry-connrefused --max-time 3...",
            # тогда вложенный цикл с попытками будет не нужен
            if (($? != 0))
            then
                echo " ERROR" | tee -a $log
                echo $host > $err_log
                exit
            else
                echo -n " OK" | tee -a $log
            fi

            let "i += 1"
            echo ""
        done
        echo ""| tee -a $log
    done
done