import demjson
json = open('./data.json', 'r')
json = demjson.decode(json.read())
for k,v in json.items():
    print(k)
    print(v)
    subjects = v[0]['subject']
    teacher_list = {}
    for x, y in zip(subjects, v[0]['teachers']):
        teacher_list[x] = y
    class_list = v[0]['class']
