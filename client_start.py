# encoding:utf8
#  ps -ef|grep sk_|grep -v grep|cut -c 9-15|xargs kill -9
import os
from config import worker_num
import time

os.system('/home/sdnfv/dpcraft/skenv/bin/python3.4 ./sk_manager.py > ./log/sk_manager.log &')
print('manager is started')
print('*' * 50)
time.sleep(1)
for i in range(worker_num):
    print('worker %d is starting' % (i + 1))
    print('#' * 50)
    os.system('/home/sdnfv/dpcraft/skenv/bin/python3.4 ./sk_worker.py > ./log/sk_worker_%d.log &' % i)
    print('worker %d is started' % (i + 1))
    print('*' * 50)


