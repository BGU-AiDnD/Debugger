from multiprocessing import Pool, Manager
from subprocess import Popen
import time
import csv
import sys


def run_process(cmd_args):
    proc = Popen(cmd_args)
    proc.communicate()


def main(num_processes, cmd_lines_path):
    p = Pool(int(num_processes))
    with open(cmd_lines_path) as f:
        p.map(run_process, csv.reader(f))

if __name__ == '__main__':
    main(*sys.argv[1:])

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