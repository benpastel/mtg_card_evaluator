__author__ = 'Dustin'

import json
import random
import numpy
import matplotlib.pyplot as plt
from math import *
from itertools import groupby
import re


def p_x(X,j,x):
    count = 0
    for i in range(len(X)):
        if X[i][j] == x:
            count = count + 1
    return count / (1.0 * len(X))

def find_p_yranges(Y, yranges):
    p_yranges = []
    m = len(Y)
    for yrange in yranges:
        count = 0
        for y in Y:
            if y >= yrange[0] and y < yrange[1]:
                count = count + 1
        p_yranges.append(count / (1.0*m))
    return p_yranges

def p_xy(X,j,Y,x,yrange):
    count = 0
    for i in range(len(X)):
        if X[i][j] == x and Y[i] >= yrange[0] and Y[i] < yrange[1]:
            count = count + 1
    return count / (1.0 * len(X)**2)

def MI(X,j,yranges,Y,p_yranges):
    summ = 0
    for x in numpy.unique(X[:,j]):
        p_x_ans = p_x(X,j,x)
        if p_x_ans == 0:
            continue
        for r in range(len(yranges)):
            yrange = yranges[r]
            p_xy_ans = p_xy(X,j,Y,x,yrange)
            p_yranges_ans = p_yranges[r]
            if p_yranges_ans == 0:
                continue
            if p_xy_ans != 0:
                summ = summ + p_xy_ans*log(p_xy_ans/(p_x_ans*p_yranges_ans))
    return summ

# Returns the list of features sorted my MI, a heuristic for if it is a good feature.
# Note: This only works best for discrete valued features, and is restricted to "ngram" features
# Caution: I use abs(MI) to sort.  Not sure if this is correct
# Since y is continuous, it is discretized here
def findMIs(X,Y,keys):
    yranges = [(0,.1),(.1,.5),(.5,1),(1,10),(10,100),(100,1000),(1000,10000),(10000,100000)]
    p_yranges = find_p_yranges(Y, yranges)
    MIs = [(keys[j],MI(X,j,yranges,Y,p_yranges)) for j in range(len(X[0])) if "ngram" in keys[j]]
    sorted_MIs = sorted(MIs, key=lambda x: -abs(x[1]))
    return [ele[0] for ele in sorted_MIs]