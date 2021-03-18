"""
Extract instances in 'jobshop1.txt' file to individuals files
to facilitate receiving data in main algorithm
"""

file1 = open('../data/jobshop1.txt', 'r')
lines = file1.readlines()

extract = []
for line in lines:
    if line[:4]==' ins':
        extract.append('$'+line[9:])
    elif (line[1:2].isdigit()) or (line[2:3].isdigit()):
        extract.append(line[1:])

tag = 0  # indicate if file pointer is open
for line in extract:
    if (line[:2]=='$ '):
        if tag==1:
            file.close()
        file_name = line[2:(len(line)-1)]
        file_name = '../data/instances/'+file_name+'.txt'
        file = open(file_name, 'w')
        tag = 1
    else:
        file.writelines(line)
