#!/usr/bin/env pythons
from random import shuffle, choice
import demjson
import pymysql
db = pymysql.connect("localhost","root","","login" )
cursor = db.cursor()
cursor.execute("DELETE FROM `schedule` WHERE 1")

def gen_pop():
    sub_count = len(sub_list)
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
    return mat,score

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
    b_temp = subjects
    b_temp, b1  = list_spilt(b_temp, 1)
    b_temp = b1 + b_temp
    b_temp, b2  = list_spilt(b_temp, 1)
    b_temp = b2 + b_temp
    b_temp, b3  = list_spilt(b_temp, 1)
    b_temp = b3 + b_temp
    b_temp, b4  = list_spilt(b_temp, 1)
    for x, y in zip(mat, mat[1:]):
        for h, i in enumerate(x):
            for j, k in enumerate(i):
                if k == 'Practical':
                    h += 1
                    if h == 1:
                        k = k + ' ' + '|'.join(b1)
                        i[j] = k
                    elif h == 2:
                        k = k + ' ' + '|'.join(b2)
                        i[j] = k
                    elif h == 3:
                        k = k + ' ' + '|'.join(b3)
                        i[j] = k
                    elif h == 4:
                        k = k + ' ' + '|'.join(b4)
                        i[j] = k
        for h, i in enumerate(y):
            for j, k in enumerate(i):
                if k == 'Practical':
                    h += 1
                    if h == 1:
                        k = k + ' ' + '|'.join(b3)
                        i[j] = k
                    elif h == 2:
                        k = k + ' ' + '|'.join(b4)
                        i[j] = k
                    elif h == 3:
                        k = k + ' ' + '|'.join(b1)
                        i[j] = k
                    elif h == 4:
                        k = k + ' ' + '|'.join(b2)
                        i[j] = k
        return x, y


def bestRes(mat):
    highest = 0
    for i in mat:
        if i[1] > highest:
            highest = i[1]
            best = i
    best_res.append(best)

population = 100
generation = 500
divisions = 2

json = open('./data2.json', 'r').read()
json = demjson.decode(json)

for k,v in json.items():
    dept_name = k
    print(k)
    optional_sub = ''
    subjects = v[0]['subject']
    theoryProf_list, pracsProf_list, res = {}, {}, {}
    for x, y, z in zip(subjects, v[0]['theory'], v[0]['practical']):
        if '/' in x:
            optional_sub = x
        theoryProf_list[x] = y
        pracsProf_list[x] = z
    class_list = v[0]['class']

    parent_list = []
    best_res = []
    sub_list = subjects + ['Practical']
    day_count = 4

    for _ in range(population):
        Matrix = gen_pop()
        Matrix = gen_fitness(Matrix)
        parent_list.append(Matrix)

    for _ in range(generation):
        bestRes(parent_list)
        parent_list = gen_crossover(parent_list)
        parent_list = cleanGene(parent_list)
    count = 0
    final_res = []
    for i in best_res:
        if i[1] > count:
            count = i[1]
            final_res = i
    print(final_res[1])
    final_res = pracSchedule(final_res[0])
    for x, y in enumerate(final_res):
        i = 'div ' + str(x + 1)
        res[i] = y
        for a in y:
            for b, c in enumerate(a):
                if c in subjects:
                    if c == optional_sub:
                        a[b] = c + ' ' + theoryProf_list[c] + ' ' + class_list[0] + '/' + class_list[1]
                    else:
                        a[b] = c + ' ' + theoryProf_list[c] + ' ' + class_list[x]
                else:
                    pracsTeach = ''
                    for h, k in enumerate(subjects):
                        if k in c:
                            pracsTeach += ' ' +  pracsProf_list[k]
                    a[b] = c + pracsTeach + ' ' + class_list[2]

#NEED TO ADD CLASSROOM NUMBER TO THE LIST ALONG WITH THE TEACHERS NAME

    jsonRes = demjson.encode(res)
    print(res)
    cursor.execute("INSERT INTO `schedule` (`Uid`, `Dept`, `TT`) VALUES (NULL, %s, %s)", (dept_name, jsonRes))
db.commit()
db.close()
