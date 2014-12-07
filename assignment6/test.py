# import collections
# print(isinstance(None, collections.Hashable))
# print(list(range(0)))
# print(i for i in {})

# for i in None:
#     print (i)
a = {1:2}
a.update(({1:2},{1:3}))
# print(a)
# a[None] = 3
# print(a)
# del a[2]
# print(a)
# del a[5]
# print(3 in a)
# # print([3] in a)
#
# # print(a[2]) # KeyError: 2
# # a[[3]] = 3 # TypeError: unhashable type: 'list'
# print(a)