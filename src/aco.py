"""
LUIZ HENRIQUE DE MELO SANTOS
NATURAL COMPUTATION - 2020/2 - CLASS:TB1
TEACHER.: GISELE LOBO PAPPA
"""

import numpy as np
from math import *
from random import *

class ACO:
    """
    Main class solver to JSS Problem using Ant Colony Optimization technique
    """

    def __init__(self, input_file, _ANTS, _RHO, _ALPHA, _BETA, _TAU):
        """
        Extract the data of instance of input file and format to be used for ACO, and initialize parameters
        """
        # ACO specifications
        self.ants = _ANTS
        self.rho = _RHO
        self.alpha = _ALPHA
        self.beta = _BETA
        self.tau = _TAU
        self.instance = dict()

        # read each line of archive
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # construct the dict using jobs and machines numbers
        header = lines[0].split()
        self.instance['jobs_number'] = int(header[0])  # matrix that represent the jobs order
        self.instance['machines_number'] = int(header[1])  # matrix that represent the machines order to execute the jobs

        # create vectors of jobs and machines
        self.instance['jobs'] = [[] for _ in range(self.instance['jobs_number'])]
        self.instance['machines'] = [[] for _ in range(self.instance['jobs_number'])]
        for i in range(1,int(header[0])+1):
            line = lines[i].split()
            for j in range(int(header[1])*2):
                if (j%2!=0):
                    self.instance['jobs'][i-1].append(int(line[j]))
                else:
                    self.instance['machines'][i-1].append(int(line[j])+1)

        # define the number of possible combinations
        self.num_edges = self.instance['jobs_number']*self.instance['machines_number']


    """
        *** ACO - JSS PROBLEM ***
    """

    def initiateAdjacenceMatrix (self):
        """
        Initialize the pheromone matrix with initial tau value
        """
        self.adjacence_matrix = np.full((self.num_edges, self.num_edges), tau, dtype=float, order='C')

    def evaluateRootMakespan (self, root, jobsInMach):
        """
        Calculate the makespan of specific root selected by an ant - promotes the jobs times sun per machine

        RETURNS: the root makespan time
        """
        # matrix that contain all makespan for each machine
        makespan = np.zeros(self.instance['machines_number']).astype('int32')
        for i in range(self.num_edges):
            # recover machines ID's
            currentMachine = self.instance['machines'][root[i]][jobsInMach[i]]
            lastMachine = self.instance['machines'][root[i]][jobsInMach[i]-1]
            # sum makespans of machine
            if makespan[currentMachine-1] < makespan[lastMachine-1]:
                makespan[currentMachine-1] = makespan[lastMachine-1]+self.instance['jobs'][root[i]][jobsInMach[i]]
            else:
                makespan[currentMachine-1] += self.instance['jobs'][root[i]][jobsInMach[i]]

        # return the makespan of machine that spent more time to execute all jobs
        return max(makespan)

    def selectEdgeByProb (self, root, desirability, pheromones_vetor):
        """
        Calculate the new probabilities of edge being walked by ants and define how edge will be chosen

        RETURNS: the index of chosen edge
        """
        # calculate the probabilitie of each edge using the probabilitie function
        probabilities = np.power( pheromones_vetor , self.alpha )
        edges_probabilities = np.power( desirability , self.beta )
        edges_probabilities = np.multiply( probabilities , edges_probabilities )
        edges_probabilities = np.multiply( edges_probabilities, 1/np.sum(edges_probabilities) )

        # define the cumulative probability in each adjacent edge and select the best one
        edge_index = 0
        root_probabilities_sum = 0
        max_probility = uniform(0,1)
        for prob in edges_probabilities:
            root_probabilities_sum += prob
            if max_probility < root_probabilities_sum:
                return edge_index
            else: edge_index += 1
        return edge_index

    def defineRoot (self, ant_root, jobsNumber):
        """
        Select the next jobs to be 'traveled' by an ant - if do not have a edge to specific job, create one

        RETURNS: the indexes of best jobs to be chosen to root
        """
        desirabilities = []
        pheromones_vetor = []
        for i in range(self.instance['jobs_number']):
            if jobsNumber[i] > (self.instance['machines_number']-1):  # case if edge do not exist in root
                pheromones_vetor.append(0)  # create a empty vector
                desirabilities.append(self.tau)  # initiate the pheromone value as TAU
            else:  # case if edge exist
                pheromones_vetor.append(self.adjacence_matrix[i][jobsNumber[i]])
                desirabilities.append(self.instance['jobs'][i][jobsNumber[i]])

        # calculate probabilities in each adjacent vector and select the best edge
        return self.selectEdgeByProb(ant_root, desirabilities, pheromones_vetor)

    def buildSolutions (self):
        """
        Create a new colony of ants through the distribution of ants in the graph

        RETURNS: the makespans of each root defined
        """
        self.roots = []     # list of all roots present in colony
        makespans = []      # list of all makespans present in colony
        for i in range(self.ants):
            ant_root = []           # root of each one ant
            jobsInMachine = []         # save the number of processed jobs in each machine
            jobsNumber = self.instance['jobs_number']*[0]
            for j in range(self.num_edges):
                # select the root to be chosen by an ant
                root = self.defineRoot(ant_root, jobsNumber)
                ant_root.append(root)
                jobsInMachine.append(jobsNumber[root])
                jobsNumber[root] += 1
            
            # add finded root to colony solutions
            self.roots.append(ant_root)
            makespans.append(self.evaluateRootMakespan(ant_root, jobsInMachine))

        return makespans

    def updatePheromonesValues (self, makespans):
        """
        Update pheromones values present in all edges of graph

        RETURNS: the updated pheromones matrix
        """
        for i in range(len(self.roots)):
            jobs = []
            ants_rank = 1
            jobsNumber = [0]*self.instance['jobs_number']

            for j in range(0,(self.num_edges),2):
                # update pheromomes values
                job = self.roots[i][j]
                machine = jobsNumber[job]
                self.adjacence_matrix[job][machine] += (self.tau/(makespans[i]*ants_rank))
                # define the ants priority
                if job not in jobs:
                    jobs.append(job)
                    ants_rank += 1
                jobsNumber[job] += 1

        # apply the evaporation rate
        self.adjacence_matrix = np.multiply(self.adjacence_matrix,(1-self.rho))
