import time

#1 Write a Python program with builtin function to multiply all the numbers in a list

# def summa(list):
#     for i in list:
#         yield i*n

# user = summa(list(map(int, input().split())))
# n = int(input())

# for j in user:
#     print(j, end =" ")

#2. Write a Python program with builtin function that accepts a string and calculate the number of upper case letters and lower case letters

# def calculate(str):
#     n = 0
#     m = 0
#     for i in range(len(str)):
#         if str[i].isupper() == True:
#             n +=1
#         if str[i].islower() == True:
#             m +=1
#     return("Upper:", n, "Lower:", m)
# strong = input()
# print(calculate( strong ))

#3. Write a Python program with builtin function that checks whether a passed string is palindrome or not.

# def pal(str):
#     if str == str[::-1]:
#         return("ЭТО ПАЛИНДРОМммммммммммм:>")
#     else:
#         return("Это НЕ ПАЛИНДРОМ :<")

# userput = input()
# print(pal(userput))

#4. Write a Python program that invoke square root function after specific milliseconds. 

# def sqrtlate(num, mlsc):
#     time.sleep(mlsc / 1000)
#     return num ** 0.5

# num = int(input())
# mlsc = int(input())
# print(sqrtlate(num, mlsc))

#5. Write a Python program with builtin function that returns True if all elements of the tuple are true.

# def all_true(tpl):
#     if not tpl:  
#         return False
#     for x in tpl:
#         if not x:
#             return False  
#     return True  

# v = tuple(map(int,input().split()))  
# print(v, all_true(v))