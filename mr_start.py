# encoding:utf8
#  ps -ef|grep start.py|grep -v grep|cut -c 9-15|xargs kill -9
import os
from multiprocessing import Process
from multiprocessing import Manager
import numpy as np
# from config import worker_num
# from config import contaminated_node_index
import time
import mr_sk_worker
import mr_sk_manager
import random
import matplotlib.pyplot as plt


# 节点数
worker_num_range = 4
# 污染节点
x = range(worker_num_range)
y_dict = {1: [], 2: [], 3: [], 4: [], 5: [], 10:[]}
for circle_no in range(2, 3):
    for xi in x:
        manager = Manager()
        # 备份污染后分布式训练正确率：
        return_dict_3 = manager.dict()
        # contaminated_num = xi
        for i in range(10):
            worker_num = 4
            contaminated_num = xi
            indexList = range(1, worker_num + 1)
            contaminated_node_index = random.sample(indexList, contaminated_num)
            # contaminated_node_index = [8, 6, 5, 9, 10]
            print('*' * 50)
            print('circle=', circle_no)
            print('containated_no_num=', xi)
            print(contaminated_node_index)
            p = Process(target=mr_sk_manager.manager_start, args=(worker_num, contaminated_node_index, i,
                                                                  return_dict_3, circle_no))
            p.start()
            time.sleep(0.5)
            workers = []
            # 启动worker
            for j in range(worker_num):
                # print('worker %d is starting' % (i + 1))
                # print('#' * 50)
                p1 = Process(target=mr_sk_worker.worker_start, args=(worker_num, contaminated_node_index))
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

        y_dict[circle_no].append(np.mean(return_dict_3.values()))
        # print('分布式训练平均正确率:')
        # print(np.mean(return_dict_1.values()))
        # print('单节点节点污染后分布式训练平均正确率：')
        # print(np.mean(return_dict_2.values()))
        # print('备份污染后分布式训练平均正确率：')
        # print(np.mean(return_dict_3.values()))
    print(y_dict[circle_no])

print(y_dict)
# l1 = plt.plot(x, y_dict[6], 'm--', label='6')
# l2 = plt.plot(x, y_dict[7], 'r--', label='7')
# l3 = plt.plot(x, y_dict[8], 'g--', label='8')
# l4 = plt.plot(x, y_dict[9], 'b--', label='9')
l5 = plt.plot(x, y_dict[2], 'c--', label='10')
# plt.plot(x, y_dict[6], 'mx-', x, y_dict[7], 'ro-', x, y_dict[8], 'g+-', x, y_dict[9], 'b^-', x, y_dict[10], 'c*-',)
plt.plot(x, y_dict[2], 'c*-',)
plt.title('The Result in Three Conditions')
plt.xlabel('Number of contaminated nodes')
plt.ylabel('score')
plt.legend()
plt.show()
os._exit(0)


# manager = Manager()
# # 分布式训练正确率：
# return_dict_1 = manager.dict()
# # 单节点节点污染后分布式训练正确率：
# return_dict_2 = manager.dict()
# # 备份污染后分布式训练正确率：
# return_dict_3 = manager.dict()
# for i in range(10):
#     worker_num = 50
#     contaminated_num = 10
#     indexList = range(1, worker_num + 1)
#     contaminated_node_index = random.sample(indexList, contaminated_num)
#     # contaminated_node_index = [8, 6, 5, 9, 10]
#     print(indexList)
#     print(contaminated_node_index)
#     p = Process(target=sk_manager.manager_start, args=(worker_num, contaminated_node_index, i,
#                                                        return_dict_1, return_dict_2, return_dict_3))
#     p.start()
#     print('*' * 50)
#     time.sleep(1)
#     for j in range(worker_num):
#         # print('worker %d is starting' % (i + 1))
#         # print('#' * 50)
#         Process(target=sk_worker.worker_start, args=(worker_num, contaminated_node_index)).start()
#         # print('worker %d is started' % (i + 1))
#         # print('*' * 50)
#     p.join()
# os._exit(0)

