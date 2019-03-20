# encoding:utf8
#  ps -ef|grep start.py|grep -v grep|cut -c 9-15|xargs kill -9
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
import matplotlib.pyplot as plt


# x = range(51)
x = range(10, 21)
y_1 = []
y_2 = []
y_3 = []

for xi in x:
    manager = Manager()
    # 分布式训练正确率：
    return_dict_1 = manager.dict()
    # 单节点节点污染后分布式训练正确率：
    return_dict_2 = manager.dict()
    # 备份污染后分布式训练正确率：
    return_dict_3 = manager.dict()
    # contaminated_num = xi
    for i in range(2):
        worker_num = 50
        contaminated_num = xi
        indexList = range(1, worker_num + 1)
        contaminated_node_index = random.sample(indexList, contaminated_num)
        # contaminated_node_index = [8, 6, 5, 9, 10]
        print(indexList)
        print(contaminated_node_index)
        p = Process(target=sk_manager.manager_start, args=(worker_num, contaminated_node_index, i,
                                                           return_dict_1, return_dict_2, return_dict_3))
        p.start()
        print('*' * 50)
        time.sleep(1)
        workers = []
        for j in range(worker_num):
            # print('worker %d is starting' % (i + 1))
            # print('#' * 50)
            p1 = Process(target=sk_worker.worker_start, args=(worker_num, contaminated_node_index))
            p1.start()
            workers.append(p1)

            # print('worker %d is started' % (i + 1))
            # print('*' * 50)
        for proc in workers:
            proc.join()
        p.join()
    # print(return_dict_1.values())
    # print(return_dict_2.values())
    # print(return_dict_3.values())
    y_1.append(np.mean(return_dict_1.values()))
    y_2.append(np.mean(return_dict_2.values()))
    y_3.append(np.mean(return_dict_3.values()))
    # print('分布式训练平均正确率:')
    # print(np.mean(return_dict_1.values()))
    # print('单节点节点污染后分布式训练平均正确率：')
    # print(np.mean(return_dict_2.values()))
    # print('备份污染后分布式训练平均正确率：')
    # print(np.mean(return_dict_3.values()))

print('分布式训练正确率：', y_1)
print('单节点节点污染后分布式训练正确率：', y_2)
print('备份污染后分布式训练正确率：', y_3)

l1 = plt.plot(x, y_1, 'r--', label='Distributed pollution free')
l2 = plt.plot(x, y_2, 'g--', label='Distributed no backup')
l3 = plt.plot(x, y_3, 'b--', label='Distributed backup')
plt.plot(x, y_1, 'ro-', x, y_2, 'g+-', x, y_3, 'b^-')
plt.title('The Result in Three Conditions')
plt.xlabel('Number of contaminated nodes')
plt.ylabel('score')
plt.legend()
plt.show()
os._exit(0)






