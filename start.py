# encoding:utf8
#  ps -ef|grep sk_|grep -v grep|cut -c 9-15|xargs kill -9
import os
from multiprocessing import Process
from multiprocessing import Manager
import numpy as np
# from config import worker_num
# from config import contaminated_node_index
import time
import sk_worker
import sk_manager
import random

# os.system('nohup /home/sdnfv/dpcraft/skenv/bin/python3.4 -u ./sk_manager.py > ./log/sk_manager.log 2>&1 &')
# print('manager is started')
# print('*' * 50)
# time.sleep(1)


# def start_worker():
#     os.system('/home/sdnfv/dpcraft/skenv/bin/python3.4 -u ./sk_worker.py > ./log/sk_worker_%d.log 2>&1' % i)


# def start_manager(name):
#     print('%s is starting' % name)
#     os.system('/home/sdnfv/dpcraft/skenv/bin/python3.4 -u ./sk_manager.py > ./log/sk_manager.log 2>&1')


# p = Process(target=start_manager, args=('manager',))

manager = Manager()
return_dict = manager.dict()

for i in range(3):
    worker_num = 50
    contaminated_num = 20
    indexList = range(1, worker_num + 1)
    contaminated_node_index = random.sample(indexList, contaminated_num)
    # contaminated_node_index = [8, 6, 5, 9, 10]
    print(indexList)
    print(contaminated_node_index)
    p = Process(target=sk_manager.manager_start, args=(worker_num, contaminated_node_index, i, return_dict))
    p.start()
    print('*' * 50)
    time.sleep(1)
    for i in range(worker_num):
        # print('worker %d is starting' % (i + 1))
        # print('#' * 50)
        Process(target=sk_worker.worker_start, args=(worker_num, contaminated_node_index)).start()
        # print('worker %d is started' % (i + 1))
        # print('*' * 50)
    p.join()
print(return_dict.values())
print(np.mean(return_dict.values()))
os._exit(0)

