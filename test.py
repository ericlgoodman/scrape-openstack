dic = {'something' : 1, "something else" : 2}

for question, num_views in dic.items():
    if num_views < 2:
        del dic[question]

print dic