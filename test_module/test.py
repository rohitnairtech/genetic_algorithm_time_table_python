#!/usr/bin/env pythons
from random import shuffle, choice
def gen_pop(sub, day):
    sub_list = sub
    day_list = day
    sub_count = len(sub_list)
    day_count = len(day_list)
    Matrix = [[[0 for x in range(sub_count)] for x in range(day_count)] for x in range(2)]
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
            for h, k in zip(a, b):
                if h == 'Practicals' and (k == 'SNMR' or k == 'STQA/Rob'):
                    score += 1
            for h, k in zip(a, a[1:]):
                if h == 'Practicals' and (k == 'SNMR' or k == 'SQTA/Rob'):
                    score += 1
            for h, k in zip(b, b[1:]):
                if h == 'Practicals' and (k == 'SNMR' or k == 'SQTA/Rob'):
                    score += 1
    for i in mat:
        for x, y in zip(i, i[1:]):
            for h, k in zip(x, y):
                if h != k:
                    score += 1
    return mat, score

def list_spilt(mat, splice):
    return mat[:splice], mat[splice:]

def gen_crossover(mat):
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
        offspring1 = gen_fitness(offspring1)
        offspring2 = gen_fitness(offspring2)
        mat.append(offspring1)
        mat.append(offspring2)
    return mat

def cleanGene(mat):
    count = 0
    for i in mat:
        if i[1] < 15:
            del mat[count]
        count += 1
    return mat

def bestRes(mat):
    highest = 0
    for i in mat:
        if i[1] > highest:
            highest = i[1]
            best = i
    best_res.append(best)

population = 100
generation = 1000
parent_list = []
best_res = []
final_soln = []
for _ in range(population):
    Matrix = gen_pop(['SNMR', 'STQA/Rob', 'BDA', 'CSAM', 'Practicals'], ['Tue', 'Wed', 'Thu', 'Fri'])
    Matrix = gen_fitness(Matrix)
    parent_list.append(Matrix)


for i in range(generation):
    #print('New Generation: ' + str(i+1))
    bestRes(parent_list)
    parent_list = gen_crossover(parent_list)
    parent_list = cleanGene(parent_list)
count = 0
for i in best_res:
    if i[1] > count:
        count = i[1]
        final_soln = i
print(final_soln)
