# encoding:utf8
import os
# from sk_manager import worker_num

# os.system('/Users/dpcraft/code/PythonWorkplace/tensorflow/bin/python3.6 ./sk_manager.py > ./log/sk_manager.log &')
worker_num = 3
for i in range(worker_num):
    print('worker %d is starting' % i)
    os.system('/Users/dpcraft/code/PythonWorkplace/tensorflow/bin/python3.6 ./sk_worker.py > ./log/sk_worker_%d.log &' % i)


