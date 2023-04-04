### 05. Файловые системы.
1. Sparse file - это файл, в котором последовательности нулевых байт заменены на информацию о них (размеры и смещения).
3. Не могут, т.к. жёсткие ссылки - это записи, указывающие на один и тот же элемент inode, хранящий атрибуты файла.
3. Запустили VM, убеждаемся, что наши доп. диски на месте. Они называются `/dev/sdb` и `/dev/sdc`:
    ```commandline
    root@sysadm-fs:/home/vagrant# fdisk -l
    ...
    
    Disk /dev/sda: 64 GiB, 68719476736 bytes, 134217728 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: gpt
    Disk identifier: 8E899987-900D-4DFA-ADB6-95FBCF13E9DE
    
    Device       Start       End   Sectors Size Type
    /dev/sda1     2048      4095      2048   1M BIOS boot
    /dev/sda2     4096   4198399   4194304   2G Linux filesystem
    /dev/sda3  4198400 134215679 130017280  62G Linux filesystem
    
    
    Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    
    
    Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    ```
4. Размечаем диск `sdb` c помощью fdisk:
    ```commandline
    root@sysadm-fs:/home/vagrant# fdisk /dev/sdb
    
    Welcome to fdisk (util-linux 2.34).
    Changes will remain in memory only, until you decide to write them.
    Be careful before using the write command.
    
    Device does not contain a recognized partition table.
    Created a new DOS disklabel with disk identifier 0xc4f1f7ea.
    
    Command (m for help): n
    Partition type
       p   primary (0 primary, 0 extended, 4 free)
       e   extended (container for logical partitions)
    Select (default p): p
    Partition number (1-4, default 1):
    First sector (2048-5242879, default 2048):
    Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G
    
    Created a new partition 1 of type 'Linux' and of size 2 GiB.
    
    Command (m for help): n
    Partition type
       p   primary (1 primary, 0 extended, 3 free)
       e   extended (container for logical partitions)
    Select (default p):
    
    Using default response p.
    Partition number (2-4, default 2):
    First sector (4196352-5242879, default 4196352):
    Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879):
    
    Created a new partition 2 of type 'Linux' and of size 511 MiB.
    
    Command (m for help): t
    Partition number (1,2, default 2): 1
    Hex code (type L to list all codes): fd
    
    Changed type of partition 'Linux' to 'Linux raid autodetect'.
    
    Command (m for help): t
    Partition number (1,2, default 2): 2
    Hex code (type L to list all codes): fd
    
    Changed type of partition 'Linux' to 'Linux raid autodetect'.
    
    Command (m for help): p
    Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disklabel type: dos
    Disk identifier: 0xc4f1f7ea
    
    Device     Boot   Start     End Sectors  Size Id Type
    /dev/sdb1          2048 4196351 4194304    2G fd Linux raid autodetect
    /dev/sdb2       4196352 5242879 1046528  511M fd Linux raid autodetect
    
    Command (m for help): w
    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.
    
    ```
5. Копируем разделы на диск `sdc` с помощью sfdisk:
    ```commandline
    root@sysadm-fs:/home/vagrant# sfdisk -d /dev/sdb |sfdisk /dev/sdc
    Checking that no-one is using this disk right now ... OK
    
    Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
    Disk model: VBOX HARDDISK
    Units: sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Script header accepted.
    >>> Created a new DOS disklabel with disk identifier 0xc4f1f7ea.
    /dev/sdc1: Created a new partition 1 of type 'Linux raid autodetect' and of size 2 GiB.
    /dev/sdc2: Created a new partition 2 of type 'Linux raid autodetect' and of size 511 MiB.
    /dev/sdc3: Done.
    
    New situation:
    Disklabel type: dos
    Disk identifier: 0xc4f1f7ea
    
    Device     Boot   Start     End Sectors  Size Id Type
    /dev/sdc1          2048 4196351 4194304    2G fd Linux raid autodetect
    /dev/sdc2       4196352 5242879 1046528  511M fd Linux raid autodetect
    
    The partition table has been altered.
    Calling ioctl() to re-read partition table.
    Syncing disks.
   
    ```
6. Собираем на получившихся разделах массивы `mdmdm`:

    ```commandline
    root@sysadm-fs:/home/vagrant# mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1
    mdadm: Note: this array has metadata at the start and
        may not be suitable as a boot device.  If you plan to
        store '/boot' on this device please ensure that
        your boot-loader understands md/v1.x metadata, or use
        --metadata=0.90
    Continue creating array? y
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md0 started.
    root@sysadm-fs:/home/vagrant# mdadm --create /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md1 started.
    ```
 
7.  ```commandline
    root@sysadm-fs:/home/vagrant# mdadm --create /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md1 started.
    ```
    Проверяем, что наши массивы работают:
    ```commandline
    root@sysadm-fs:/home/vagrant# cat /proc/mdstat
    Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10]
    md1 : active raid0 sdc2[1] sdb2[0]
          1042432 blocks super 1.2 512k chunks
    
    md0 : active raid1 sdc1[1] sdb1[0]
          2094080 blocks super 1.2 [2/2] [UU]
    
    unused devices: <none>
    ```
8. Создаём Physical Volume:
    ```commandline
    root@sysadm-fs:/home/vagrant# pvcreate  /dev/md0 /dev/md1
    Physical volume "/dev/md1" successfully created.
    ```
9. Создаём группу:
    ```commandline
    root@sysadm-fs:/home/vagrant# vgcreate vg_test /dev/md0 /dev/md1
    Volume group "vg_test" successfully created
    ```
10. Создаём логический том:
    ```commandline
    root@sysadm-fs:/home/vagrant# lvcreate -L 100M -n lv_test vg_test /dev/md1
      Logical volume "lv_test" created.
    ```
11. Форматируем и монтируем раздел:
    ```commandline
    root@sysadm-fs:/home/vagrant# mkfs.ext4 /dev/vg_test/lv_test
    mke2fs 1.45.5 (07-Jan-2020)
    Creating filesystem with 25600 4k blocks and 25600 inodes
    
    Allocating group tables: done
    Writing inode tables: done
    Creating journal (1024 blocks): done
    Writing superblocks and filesystem accounting information: done
    
12. ```commandline
    root@sysadm-fs:/home/vagrant# mkdir /mnt/test
    root@sysadm-fs:/home/vagrant# mount /dev/vg_test/lv_test /mnt/test
    ```
13. Копируем тестовый файл:
    ```commandline
    root@sysadm-fs:/home/vagrant# cd /mnt/test/
    root@sysadm-fs:/mnt/test# wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O test.gz
    --2023-04-04 10:54:03--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
    Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
    Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 24693115 (24M) [application/octet-stream]
    Saving to: ‘test.gz’
    
    test.gz                                                   100%[=====================================================================================================================================>]  23.55M  5.06MB/s    in 4.5s
    
    2023-04-04 10:54:08 (5.20 MB/s) - ‘test.gz’ saved [24693115/24693115]
    ```
14. Вывод lsblk:
    ```commandline
    root@sysadm-fs:/mnt/test# lsblk
    NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
    loop0                       7:0    0   62M  1 loop  /snap/core20/1611
    loop2                       7:2    0 67.8M  1 loop  /snap/lxd/22753
    loop3                       7:3    0 49.9M  1 loop  /snap/snapd/18596
    loop4                       7:4    0 63.3M  1 loop  /snap/core20/1852
    loop5                       7:5    0 91.9M  1 loop  /snap/lxd/24061
    sda                         8:0    0   64G  0 disk
    ├─sda1                      8:1    0    1M  0 part
    ├─sda2                      8:2    0    2G  0 part  /boot
    └─sda3                      8:3    0   62G  0 part
      └─ubuntu--vg-ubuntu--lv 253:0    0   31G  0 lvm   /
    sdb                         8:16   0  2.5G  0 disk
    ├─sdb1                      8:17   0    2G  0 part
    │ └─md0                     9:0    0    2G  0 raid1
    └─sdb2                      8:18   0  511M  0 part
      └─md1                     9:1    0 1018M  0 raid0
        └─vg_test-lv_test     253:1    0  100M  0 lvm   /mnt/test
    sdc                         8:32   0  2.5G  0 disk
    ├─sdc1                      8:33   0    2G  0 part
    │ └─md0                     9:0    0    2G  0 raid1
    └─sdc2                      8:34   0  511M  0 part
      └─md1                     9:1    0 1018M  0 raid0
        └─vg_test-lv_test     253:1    0  100M  0 lvm   /mnt/test
    ```
15. Тестируем файл:
    ```commandline
    root@sysadm-fs:/mnt/test# gzip -t test.gz
    root@sysadm-fs:/mnt/test# echo $?
    0
    root@sysadm-fs:/mnt/test#
    ```
16. Перемещаем тестовый раздел:
    ```commandline
    root@sysadm-fs:/mnt/test# pvmove -n lv_test /dev/md1 /dev/md0
      /dev/md1: Moved: 16.00%
      /dev/md1: Moved: 100.00%
    ```
17. Помечаем диск как "сбойный":
    ```commandline
    root@sysadm-fs:/mnt/test# mdadm /dev/md0 --fail /dev/sdb1
    mdadm: set /dev/sdb1 faulty in /dev/md0
    ```
17. Проверяем:
    ```commandline
    root@sysadm-fs:/mnt/test# cat /proc/mdstat
    Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10]
    md1 : active raid0 sdc2[1] sdb2[0]
          1042432 blocks super 1.2 512k chunks
    
    md0 : active raid1 sdc1[1] sdb1[0](F)
          2094080 blocks super 1.2 [2/1] [_U]
    
    unused devices: <none>
    ```
    dmesg:
    ```commandline
    root@sysadm-fs:/mnt/test# dmesg|tail -n 2
    [69074.255634] md/raid1:md0: Disk failure on sdb1, disabling device.
                   md/raid1:md0: Operation continuing on 1 devices.
    ```
19. Снова тестируем наш файл:
    ```commandline
    root@sysadm-fs:/mnt/test# gzip -t test.gz
    root@sysadm-fs:/mnt/test# echo $?
    0
    root@sysadm-fs:/mnt/test#
    ```
    