# encoding:utf8
import os
from config import worker_num

# os.system('/Users/dpcraft/code/PythonWorkplace/tensorflow/bin/python3.6 ./sk_manager.py > ./log/sk_manager.log &')
for i in range(worker_num):
    print('worker %d is starting' % (i + 1))
    print('#' * 50)
    os.system('/Users/dpcraft/code/PythonWorkplace/tensorflow/bin/python3.6 ./sk_worker.py > ./log/sk_worker_%d.log &' % i)
    print('worker %d is started' % (i + 1))
    print('*' * 50)


