from subprocess import Popen, PIPE
from multiprocessing import Process, Lock, Pool
from functools import partial
import time

def get_relevant_queries(query, process, mutex):
    print('here!')
    with mutex:
        print('here!', query)
	process.stdin.write(query)
        time.sleep(0.5)
        l = []
        for i in range(0, 10, 1):
	    print('here', i, process.stdout.readline())		
	    #l.append(process.stdout.readline())
        print(l)
	return l
