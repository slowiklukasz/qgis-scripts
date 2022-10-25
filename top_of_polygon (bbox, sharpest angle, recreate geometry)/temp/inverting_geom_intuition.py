lst = ["a", "b", "c", "d", "e", "f", "a"]
strt = 2
strt_v = lst[strt]

lst_1 = lst[:strt]
lst_1.append(strt_v) # closing polygon
lst_2 = lst[strt:-1]

re_lst = lst_2 + lst_1
print(lst_2)
print(lst_1)
print(re_lst)

