#!/usr/bin/python

import preparationSVM


def getAccuracy(n):
    preparationSVM.doIt(n)
    # Settings
    filename = 'data.txt'
    params = '-t 0 -c 50 -b 1'
    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    lines = file_len(filename)
    border = int(lines/2)

getAccuracy(5)
