import numpy as np
from os import system

# BEST COMBINATION OBTAINED: python main.py la01 300 30 0.2 0.8 0.9 40

# parameters to be checked
parameters = {'epochs': np.arange(110,1000,30),
                'ant_num': np.arange(20,300,10),
                'rho': np.arange(0.4,1.0,0.02),
                'alpha': np.arange(0.4,1.0,0.02),
                'beta': np.arange(0.4,1.0,0.02),
                'tau': np.arange(20,100,2)}

# searching for epochs
print('Epochs')
for i in parameters['epochs']:
    print(str(i))
print('\n')
for i in parameters['epochs']:
    command = 'python main.py la01 '+str(i)+' 30 0.4 1 1 40'
    system(command)

# searching for ant_num
print('\nAnts number')
for i in parameters['ant_num']:
    print(str(i))
print('\n')
for i in parameters['ant_num']:
    command = 'python main.py la01 100 '+str(i)+' 0.4 1 1 40'
    system(command)

# searching for rho
print('\nRho')
for i in parameters['rho']:
    print(str(i))
print('\n')
for i in parameters['rho']:
    command = 'python main.py la01 100 30 '+str(i)+' 1 1 40'
    system(command)

# searching for alpha
print('\nalpha')
for i in parameters['alpha']:
    print(str(i))
print('\n')
for i in parameters['alpha']:
    command = 'python main.py la01 100 30 0.4 '+str(i)+' 1 40'
    system(command)

# searching for beta
print('\nbeta')
for i in parameters['beta']:
    print(str(i))
print('\n')
for i in parameters['beta']:
    command = 'python main.py la01 100 30 0.4 1 '+str(i)+' 40'
    system(command)

# searching for tau
print('\ntau')
for i in parameters['tau']:
    print(str(i))
print('\n')
for i in parameters['tau']:
    command = 'python main.py la01 100 30 0.4 1 1 '+str(i)
    system(command)
