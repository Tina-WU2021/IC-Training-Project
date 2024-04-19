# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 22:15:37 2022

@author: Andy6
"""

import datetime
import json

def saverecord(name, difficulty, level, exp_total):
    time = str(datetime.datetime.now())[:-7]
    
    record= {
        'Name': name,
        'Time': time,
        'Record': {
            'Difficulty': difficulty,
            'Level': level,
            'EXP': exp_total
            }
        }

    record_json = json.dumps(record)
    f = open("record.txt", "a")
    f.write(record_json + "\n")
    f.close()
    
def readrecord(file):
    global record
    record = []
    f = open(file, "r")
    for line in f:
        data = json.loads(line)
        if len(record) > 0:
            if data['Record']['EXP'] < record[-1]['Record']['EXP']:
                record += [data]
            else:
                for i in range(0, len(record)):
                    if data['Record']['EXP'] >= record[i]['Record']['EXP']:
                        record += [record[-1]]
                        for j in range(len(record) - 2, i, -1):
                            record[j] = record[j - 1]
                        record[i] = data
                        break
        else:
            record += [data]
    f.close()    
        
    return record