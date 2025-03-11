#1
# def sq(n):
#     h = 1
#     while h <= n:
#         yield h*h
#         h +=1
# x = sq(int(input()))
# for i in x:
#     print(i, end = ",")

#2
# def even(n):
#     num = 0
#     while num <= n:
#         yield num
#         num += 2
# result = even(int(input()))
# for i in result:
#     print(", ".join(map(str,result)))

#3
# def gbcz(n):
#     num = 0
#     while num <= n:
#         if num %3 == 0 and num %4 ==0:
#             yield num
#         num += 1
# result = gbcz(int(input()))
# for i in result:
#     print(i,end ="\t")

#4
# def square(a,n):
#     h = a
#     while h <= n:
#         yield h*h
#         h += 1
# a, n = map(int, input().split())
# x = square(a, n)
# for i in x:
#     print(i, end = "\t")

#5
# def desc(n):
#     while n >= 0:
#         yield n
#         n -= 1
# x = desc(int(input()))
# for i in x:
#     print(", ".join(map(str,x)))
