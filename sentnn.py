from subprocess import Popen, PIPE
from multiprocessing import Process, Lock, Pool
from functools import partial
import time


c = "./fasttext nnSent ../trainedModels/model_31k.bin ../../CrowdPlatform/seeds_generator/visited_queries.txt"

process = Popen(c.split(), stdin=PIPE, stdout=PIPE, universal_newlines=True)
time.sleep(3)

process.stdout.readline()
mutex = Lock()
def get_relevant_queries(query):
    with mutex:
        process.stdin.write(query)
        time.sleep(0.5)
        l = []
        for i in range(0, 10, 1):
            l.append(process.stdout.readline())
        print(l)

if __name__ == '__main__':
    queries = ["dynamic programming \n", "optimization \n"]

    p = Pool(4)
    func = partial(get_relevant_queries)
    p.map(func, queries)

