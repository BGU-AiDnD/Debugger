from multiprocessing import Pool
from subprocess import Popen
import csv
import sys
import os


def run_process(cmd_args):
    print "Running", cmd_args
    proc = Popen(cmd_args)
    proc.communicate()


def main(num_processes, cmd_lines_path):
    p = Pool(int(num_processes))
    with open(cmd_lines_path) as f:
        p.map(run_process, csv.reader(f))


def run_configurations(dir_path, num_processes):
    p = Pool(int(num_processes))
    p.map(run_process, map(lambda x: [sys.executable, "wrapper.py", x, "learn"], map(lambda x: os.path.join(dir_path, x), os.listdir(dir_path))))


if __name__ == '__main__':
    run_configurations(r"C:\Users\amirelm\Documents\GitHub\repository_mining\repository_data\configurations", 10)
    # main(*sys.argv[1:])

""" Running example:
python test_process.py 3 process.csv

process.csv:
python,-c,import time;time.sleep(10);print 100
python,-c,import time;time.sleep(10);print 100
python,-c,import time;time.sleep(10);print 100
python,-c,import time;time.sleep(10);print 100
python,-c,import time;time.sleep(10);print 100
python,-c,import time;time.sleep(10);print 100
python,-c,import time;time.sleep(10);print 100
python,-c,import time;time.sleep(10);print 100
python,-c,import time;time.sleep(10);print 100
python,-c,import time;time.sleep(10);print 100
"""