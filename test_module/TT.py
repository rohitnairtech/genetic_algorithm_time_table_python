#!/usr/bin/env pythons
from random import shuffle, choice
from xlwt import Workbook

def gen_pop():
    sub_count = len(sub_list)
    day_count = len(day_list)
    Matrix = [[[0 for x in range(sub_count)] for x in range(day_count)] for x in range(divisions)]

    for x in range(day_count):
        shuffle(sub_list)
        for u in range(sub_count):
            Matrix[0][x][u] = sub_list[u]
    for x in range(1,2):
        c = x - 1
        for y in range(day_count):
            flag = ''
            while True:
                shuffle(sub_list)
                for i in range(sub_count):
                    if Matrix[c][y][i] == sub_list[i]:
                        flag = 'same'
                        break
                if flag != 'same':
                    for u in range(sub_count):
                        Matrix[x][y][u] = sub_list[u]
                    break
                else:
                    flag = ''

    return Matrix

def gen_fitness(mat):
    score = 0
    for x, y in zip(mat, mat[1:]):
        for a, b in zip(x, y):
            for h, k in zip(a, b[1:]):
                if h != k:
                    score += 1
    for i in mat:
        for x, y in zip(i, i[1:]):
            for a, b in zip(x, y):
                if a != b:
                    score += 1
    if score > 44:
        """print('\nThe optimal result is:\n')"""
        pracSchedule(mat)
        exit()
    else:
        #print(mat, score)
        return mat,score

def list_spilt(mat, splice):
    return mat[:splice], mat[splice:]

def gen_crossover(mat):
    #print('\nCreating Crossover points and Mutating the population \n')
    par_len = len(mat)
    split_point = [2,3]
    for _ in range(par_len):
        par1 = choice(mat)
        par2 = choice(mat)
        while par1 == par2:
            par2 = choice(mat)
        mat.remove(par1)
        mat.remove(par2)
        par1 = par1[0]
        par2 = par2[0]
        splice = choice(split_point)
        offspring1 = []
        offspring2 = []
        for i, j in zip(par1,par2):
            a, b = list_spilt(i, splice)
            h, k = list_spilt(j, splice)
            child1 = a + k
            child2 = h + b
            offspring1.append(child1)
            offspring2.append(child2)
        #print('\nGenerating fitness score for the newly formed child\n')
        offspring1 = gen_fitness(offspring1)
        offspring2 = gen_fitness(offspring2)
        mat.append(offspring1)
        mat.append(offspring2)
    return mat

def cleanGene(mat):
    for c, i in enumerate(mat):
        if i[1] < 25:
            del mat[c]
    return mat

def pracSchedule(mat):
    b1 = ['BDA', 'CSAM', 'SQTA', 'Robo']
    b2, b_temp = list_spilt(b1, 1)
    b2 = b_temp + b2
    b3, b_temp = list_spilt(b2, 1)
    b3 = b_temp + b3
    b4, b_temp = list_spilt(b3, 1)
    b4 = b_temp + b4
    for x, y in zip(mat, mat[1:]):
        for h, i in enumerate(x):
            for j, k in enumerate(i):
                if k == 'Practical':
                    h += 1
                    if h == 1:
                        k = k + ' ' + '|'.join(b1)
                        i[j] = k
                    if h == 2:
                        k = k + ' ' + '|'.join(b2)
                        i[j] = k
                    if h == 3:
                        k = k + ' ' + '|'.join(b3)
                        i[j] = k
                    if h == 4:
                        k = k + ' ' + '|'.join(b4)
                        i[j] = k
        for h, i in enumerate(y):
            for j, k in enumerate(i):
                if k == 'Practical':
                    h += 1
                    if h == 1:
                        k = k + ' ' + '|'.join(b3)
                        i[j] = k
                    if h == 2:
                        k = k + ' ' + '|'.join(b4)
                        i[j] = k
                    if h == 3:
                        k = k + ' ' + '|'.join(b1)
                        i[j] = k
                    if h == 4:
                        k = k + ' ' + '|'.join(b2)
                        i[j] = k
        exportExcel([x, y])


#Make this less hard-coded
def exportExcel(mat):
    results = mat
    day_list = ['Mon','Tue', 'Wed', 'Thu', 'Fri']
    sub_count = len(sub_list) + 1
    wb = Workbook()
    sheet1 = wb.add_sheet('Div 1')
    sheet2 = wb.add_sheet('Div 2')
    width = 256 * 30
    for c, day in enumerate(day_list):
        sheet1.write(0,c, day)
        sheet2.write(0,c, day)
        c += 1
        sheet1.col(c).width = width
        sheet2.col(c).width = width
    for i in range(sub_count):
        i += 1
        sheet1.write(i,0,'Project')
        sheet2.write(i,0,'Project')
    for x,y in zip(results, results[1:]):
        for c, i in enumerate(x):
            i.insert(3,'Break')
            c+=1
            sheet1.col(c).width = width
            for r, h in enumerate(i):
                r+=1
                sheet1.write(r,c,h)
        for c, i in enumerate(y):
            i.insert(3,'Break')
            c+=1
            for r ,h in enumerate(i):
                r+=1
                sheet2.write(r,c,h)
    fname = 'BEIT.xls'
    wb.save(fname)
    print('Exported to '+fname)


population = 100
generation = 500
parent_list = []
sub_list = ['SNMR', 'CSAM', 'STQA/Rob', 'BDA', 'Practical']
day_list = ['Tue', 'Wed', 'Thu', 'Fri']
divisions = 2
#print('\nInitial population of solutions loaded\n')
for _ in range(population):
    Matrix = gen_pop()
    Matrix = gen_fitness(Matrix)
    parent_list.append(Matrix)

for _ in range(generation):
    parent_list = gen_crossover(parent_list)
    parent_list = cleanGene(parent_list)
