import os
import time
import threading
import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

map_file_prefix = './output/con/map'
reduce_file_prefix = './output/con/reduce'
GL_max_len = 250000
GL_max_file = 512


def map_write_file(idx):
    file_name = '{}_{}.txt'.format(map_file_prefix, idx)
    with open(file_name, 'w') as file:
        for i in range(GL_max_len):
            file.write('part_{}_line_{}\n'.format(idx, i))
        file.close()


def takeSleep(idx, name):
    file_name = '{}_{}.txt'.format(map_file_prefix, idx)
    with open(file_name, 'w') as file:
        for i in range(GL_max_len):
            file.write('part_{}_line_{}\n'.format(idx, i))
        file.close()

# Print iterations progress


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


def reduce_file():
    file_name = '{}.txt'.format(reduce_file_prefix)
    with open(file_name, 'w')as out_file:
        for i in range(GL_max_file):
            in_file_name = '{}_{}.txt'.format(map_file_prefix, i)
            with open(in_file_name, 'r') as in_file:
                in_str = in_file.read()
                out_file.write(in_str)
                in_file.close()
            os.unlink(in_file_name)

        out_file.close()


def raw_func():
    file_name = '{}.txt'.format(reduce_file_prefix)
    with open(file_name, 'w') as out_file:
        for i in range(GL_max_file):
            printProgressBar(i+1, GL_max_file, prefix='Raw',
                             suffix='Raw finished', length=40, decimals=2)
            for j in range(GL_max_len):
                out_file.write('part_{}_line_{}\n'.format(i, j))
        out_file.close()
    # print()
    return


def flow_func():
    for i in range(GL_max_file):
        printProgressBar(i+1, GL_max_file, prefix='Flow',
                         suffix='Flow finished', length=40)
        map_write_file(i)
    # print()
    reduce_file()


def concurrency_func():
    threads = []
    for i in range(GL_max_file):
        printProgressBar(i+1, GL_max_file, prefix='Flow',
                         suffix='Flow finished', length=40)
        t = threading.Thread(target=takeSleep, args=(str(i), 'zzz'))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    reduce_file()
    # print()
    return


def test_average_time(f):
    start_time = time.time()
    count = 5
    for _ in range(count):
        f()
    end_time = time.time()
    average_time = (end_time-start_time)/count
    print('{} use time = {} s\n'.format(f.__name__, average_time))


print('lab test result =>')
test_average_time(raw_func)
test_average_time(flow_func)
test_average_time(concurrency_func)


# print('主程序开始运行...')
# threads=[]
# for i in range(0, 50):
#     t=threading.Thread(target=takeSleep, args=(str(i), 'zhangphil'))
#     threads.append(t)
#     t.start()

# print('主程序运行中...')

# # 等待所有线程任务结束。
# for t in threads:
#     t.join()

# print("所有线程任务完成")
