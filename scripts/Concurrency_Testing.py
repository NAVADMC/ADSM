# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=4>

# From python library [concurrent.futures](https://docs.python.org/3.3/library/concurrent.futures.html)

# <codecell>

import subprocess
subprocess.call(['sqlite3.exe', '--help'])

# <codecell>

import os
os.startfile('sqlite3.exe')

# <codecell>

command = 'sqlite3.exe --help'
os.system(command)

# <codecell>

import subprocess
import sys
command = ['sqlite3.exe', '--help']
child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
for x in range(10000):
    out = child.stdout.read(1)
    if out == '' and child.poll() != None:
        break
    if out:
        print(out)
#         sys.stdout.flush()

# <codecell>

proc = subprocess.Popen('sqlite3.exe --help', shell=True, stdout=subprocess.PIPE)
try:
    outs, errs = proc.communicate(timeout=15)
except TimeoutExpired:
    proc.kill()
    outs, errs = proc.communicate()
print(outs, errs)

# <headingcell level=1>

# This actually works:

# <codecell>

subprocess.check_output(['ipconfig'])

# <headingcell level=2>

# TODO: check try subprocess.communicate()

# <codecell>


# <codecell>

import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://newline.us/']

# Retrieve a single page and report the url and contents
def load_url(url, timeout):
    conn = urllib.request.urlopen(url, timeout=timeout)
    return conn.readall()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))

# <markdowncell>

# Works because Threads are interactive.

# <codecell>


# <codecell>

import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

main()

# <markdowncell>

# Doesn't work because multiprocessing library is not interactive.

# <codecell>


# <codecell>

from IPython.parallel import Client
rc = Client()

# <markdowncell>

# Doesn't work because I haven't set up security.

# <codecell>


