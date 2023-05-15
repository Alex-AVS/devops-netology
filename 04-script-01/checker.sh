#!/usr/bin/env bash

#массив проверяемых хостов 
hosts=("192.168.67.1" "173.194.222.113" "87.250.250.242")

num_tries=5	#число попыток
log=./log.log	#файл журнала
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
	#в принципе, команду можно ихменить на "curl -s --retry $num_tries --retry-delay 0 ----retry-connrefused --max-time 3...", тогда вложенный цикл будет не нужен
	if (($? != 0))
	then
	    echo -n " ERROR" | tee -a $log
	    echo $host > ./error
	    break 3
	else 
	    echo -n " OK" | tee -a $log
	fi
	
	let "i += 1"
	echo ""
    done
    echo ""| tee -a $log
done
done