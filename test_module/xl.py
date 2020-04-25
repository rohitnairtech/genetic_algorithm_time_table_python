from xlwt import Workbook

sub_list = ['SNMR', 'Java', 'STQA/Rob', 'BDA', 'Practical']
results = [['Java', 'STQA/Rob', 'Practical', 'BDA', 'SNMR'], ['BDA', 'Practical', 'SNMR', 'Java', 'STQA/Rob'], ['STQA/Rob', 'BDA', 'Practical', 'SNMR', 'Java'], ['Practical', 'STQA/Rob', 'BDA', 'Java', 'SNMR']], [['Practical', 'SNMR', 'BDA', 'Java', 'STQA/Rob'], ['STQA/Rob', 'BDA', 'Practical', 'SNMR', 'Java'], ['Practical', 'SNMR', 'Java', 'STQA/Rob', 'BDA'], ['SNMR', 'Java', 'STQA/Rob', 'BDA', 'Practical']]
day_list = ['Mon','Tue', 'Wed', 'Thu', 'Fri']
c = 0
wb = Workbook()
sheet1 = wb.add_sheet('Div 1')
sheet2 = wb.add_sheet('Div 2')
for day in day_list:
    sheet1.write(0,c, day)
    sheet2.write(0,c, day)
    c += 1

for i in range(len(sub_list)):
    i += 1
    sheet1.write(i,0,'Project')
    sheet2.write(i,0,'Project')
print(results)

for x,y in zip(results, results[1:]):
    c, r = 0,0
    for i in x:
        c+=1
        for h in i:
            r+=1
            sheet1.write(r,c,h)
        r=0
    c = 0
    for i in y:
        c+=1
        for h in i:
            r+=1
            sheet2.write(r,c,h)
        r = 0
#Insert these data into the excel file
wb.save('Engg_IT_4.xls')
