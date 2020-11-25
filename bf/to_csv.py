import numpy as np
import pandas as pd
import re

def intepret_time(s):
    temp = re.sub(',','.',s)
    res = re.findall('[0-9.]+',temp)
    mins = float(res[0])
    secs = float(res[1])
    return mins *60  + secs

##
fr = open('results.txt')
fc = open('results.csv',mode='w')

fc.write('level,real,user,sys,succes\n')

while True:
    line = fr.readline()
    if 'level' in line:
        level = re.search('\d+',line).group()
        line = fr.readline()[:-1]
        succes = False if line == 'Terminated' else True
        if not succes:
            _ = fr.readline()
        line = fr.readline()[:-1]
        real = intepret_time(line)
        line = fr.readline()[:-1]
        user = intepret_time(line)
        line = fr.readline()[:-1]
        sys  = intepret_time(line)
        result = [str(level),str(real),str(user),str(sys),str(succes)]
        fc.write(",".join(result) + '\n')
    elif not line:
        break
##
fr.close()
fc.close()

