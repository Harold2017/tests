#!/usr/bin/env python
# -*- coding:utf-8 _*-  
"""
@author:Harold
@license: MIT Licence
@file: extract_data_from_csv.py
@time: 2021/05/26
"""

import numpy as np
import argparse
import os
import re


def file_exists(x):
    if not os.path.exists(x):
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x

def dir_exists(x):
    dir = os.path.dirname(x)
    if not os.path.exists(dir):
        raise argparse.ArgumentTypeError("{0} does not exist".format(dir))
    return x

def skip_valid(x):
    x = int(x)
    if x < 0:
        raise argparse.ArgumentError("input rows number {0} invalid".format(x))
    return x

def cols_valid(x):
    x = int(x)
    if x < 1 and x != -1:
        raise argparse.ArgumentError("input rows number {0} invalid".format(x))
    return x

def to_float(value):
    try:
        return float(re.sub('[^.\-\d]', '', value))
    except ValueError:
        return float('nan')  # or None if you wish


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract data from csv and store into txt')
    parser.add_argument('-f', '--file', dest='filepath', required=True, nargs=1, 
                        type=file_exists,
                        help='filepath')
    parser.add_argument('-s', '--skip', dest='skip', required=True, default=0, nargs=1,
                        type=skip_valid,
                        help='skip headers')
    parser.add_argument('-c', '--cols', dest='cols', required=True, default=-1, nargs=1,
                        type=cols_valid,
                        help='cols number (default -1 means all cols)')
    parser.add_argument('-o', '--out', dest='outfilepath', required=True, nargs=1, 
                        type=dir_exists,
                        help='output filepath')
    parser.add_argument('-v', '--convert', dest='convert', action='store_true',
                        help='convert to 3d array')
    args = parser.parse_args()

    file = os.path.abspath(args.filepath[0])
    cols = args.cols[0]
    if cols == -1:
        data = np.genfromtxt(file, delimiter=',', skip_header=args.skip[0], dtype = 'str', encoding=None)
        _, cols = data.shape
    data = np.genfromtxt(file, delimiter=',', skip_header=args.skip[0], usecols=tuple(range(cols)), dtype=None, converters={ i : to_float for i in range(cols) }, encoding=None)

    # if need convert to 3d array
    if cols > 3 and args.convert:
        r, c = data.shape
        n_data = np.empty([r*c, 3], dtype=float)
        i = 0
        j = 0
        for x, y in zip(np.nditer(data), range(r*c)):
            j += 1
            if j == c - 1:
                i += 1
                j = 0
            n_data[y] = [i, j, x]
        np.savetxt(os.path.abspath(args.outfilepath[0]), n_data, delimiter=' ', fmt='%.6f')    
    else:        
        np.savetxt(os.path.abspath(args.outfilepath[0]), data, delimiter=' ', fmt='%.6f')
