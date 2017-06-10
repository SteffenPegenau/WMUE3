#!/usr/bin/python
from svmutil import *
import sys
import time
#from time import process_time




# Settings
filename = '../Aufg02/data.txt'
params = '-t 0 -c 50 -b 1'


# Shuffle
#import random
#lines = open(filename).readlines()
#random.shuffle(lines)
#open(filename, 'w').writelines(lines)

# Get number of samples
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

lines = file_len(filename)
border = int(lines/2)
print('Found ' + str(lines) + ' lines => take first ' + str(border) +  ' as training data')

# Timer to measure the time of training and testing
if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

y, x = svm_read_problem(filename)

# TRAIN
t0 = default_timer()
m = svm_train(y[:border], x[:border], params)
timeTraing = default_timer() - t0

# TEST
t0 = default_timer()
p_label, p_acc, p_val = svm_predict(y[border:], x[border:], m)
timeTesting= default_timer() - t0

print('Training time: ' + str(timeTraing) + 's')
print('Testing time: ' + str(timeTesting) + 's')

i = 0
tp = 0 # true positives (a course is recognized)
fn = 0 # false negatives (a course is not recognized)
fp = 0 # false positives (a non-course is recognized as a course)
tn = 0 # true negatives (a non-course is recognized)


offset = int(lines - border - 1)
ySize = len(y)
#print('Offset:' + str(offset) + '\tSize of y=' + str(ySize))
for pred in p_label:
    #print(str(offset) + ' + ' + str(i) + ' = ' + str(offset+i) + ' / ' + str(ySize))
    act = y[offset + i] #p_val[i][0]
    print('i=' + str(i) + '\tpred=' + str(pred) + '\tval=' + str(p_val[i]) + '\tact=' + str(act))
    #print(str(i)+';'+str(pred)+';'+str(act))
    if act > 0 and pred > 0: tp += 1
    if act > 0 and pred < 0: fn += 1
    if act < 0 and pred > 0: fp += 1
    if act < 0 and pred < 0: tn += 1
    i += 1
print('label size=' + str(len(p_label)) + '\tvalue size=' + str(len(p_val)))
print('|\t\t|\tpred +1\t|\tpred -1\t|')
print('|\t act +1\t|\t' + str(tp) + '\t|\t ' + str(fn) + '\t|')
print('|\t act -1\t|\t' + str(fp) + '\t|\t ' + str(tn) + '\t|')

accuracy = float((tp + tn)) / (lines - border)
print('Calc accuracy: ' + str(accuracy))
#print(p_label)
#print(p_val)
