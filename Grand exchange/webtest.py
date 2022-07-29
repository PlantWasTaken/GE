from decimal import DivisionByZero
from itertools import count
from grapheme import length
import requests
import json
import linecache
import time as t
import sys
from prettytable import PrettyTable
from alive_progress import alive_bar

sys.setrecursionlimit(10)

i = 1
def main():
    global i
    while(i != 5):
        try:
            print(((i*100)-4)/(i))
            i = i +1
        except ZeroDivisionError:
            print("error")
            main()

    print("done")
    i = 0
main()