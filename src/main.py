"""
LUIZ HENRIQUE DE MELO SANTOS
NATURAL COMPUTATION - 2020/2 - CLASS:TB1
TEACHER.: GISELE LOBO PAPPA
"""

## usage ##
## $ python3 main.py <instance-name> <epochs> <ants-number> <rho> <alpha> <beta> <tau>

import time
import numpy as np
from sys import argv,maxsize
from aco import *       # custom ACO utilities functions library

## algorithm parameters ##
EPOCHS = int(argv[2])   # number of iterations
ANTS = int(argv[3])     # number of ants
RHO = float(argv[4])    # evaporation rate
ALPHA = float(argv[5])  # control the influence of tau - the amount of pheromone deposited for transition - 1
BETA = float(argv[6])   # control the influence of eta - the desirability of state transition - 1
TAU = float(argv[7])    # define the initial value of pheromones in edges in graph

# check if valid input parameters were given
if len(argv)<8:
    print('ERROR: parameters were passed incorrectly')
    exit(0)
try:
    input_file = '../data/instances/'+str(argv[1])+'.txt'
    aco = ACO(input_file, ANTS, RHO, ALPHA, BETA, TAU)  # initialize ACO class
except:
    print('ERROR: it was not possible to read the input instance')
    exit(0)

makespanValues = []             # store the makespan of each epoch
minMakespanAll = maxsize        # optimum value obtained - start with maximum value possible
aco.initiateAdjacenceMatrix()   # create initial adjacente matrix

for epoch in range(EPOCHS):
    # create ant colony and build roots
    makespans = aco.buildSolutions()
    minMakespanEpoch = min(makespans)
    # check if the best makespan has been overcome and update variables
    if minMakespanEpoch < minMakespanAll: minMakespanAll=minMakespanEpoch
    # update pheromone matrix
    aco.updatePheromonesValues(makespans)  
    # store the makespan value obtained
    makespanValues.append(makespans[0])

# print results
print('> Best makespan obtained: ', str(minMakespanAll))
print('> Makespan mean: ', str(round(np.mean(makespanValues),2)))
print('> Makespan std: ', str(round(np.std(makespanValues),2)))
