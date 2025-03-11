import re

with open("row (1).txt", encoding="utf-8") as f:
    text = f.read()

#1
# pattern = r"аб*"
# x = re.findall(pattern, text)
# print(x)c
#2
# pattern = r"ас{2,3}"
# x = re.findall(pattern, text)
# print(x)
#3
# pattern = r"[а-я]+-[а-я]+"
# x = re.findall(pattern, text)
# print(x)
#4
# pattern = r"[А-Я][а-я]+"
# x = re.findall(pattern, text)
# print(x)
# #5
# pattern = r"К.*а"
# x = re.findall(pattern, text)
# print(x)
# #6
# pattern = r"[ .,]"
# x = re.sub(pattern, ":", text)
# print(x[:100])
# #7
# txt = "son_pon_anton"
# def camel(s):
#     words = s.split("_")
#     return words[0] + "".join(word.capitalize() for word in words[1:])
# print(camel(txt))
#8
# txt ="ПриветМирКакДела"
# pattern = r"(?=[А-Я])"
# x = re.split(pattern, txt)
# x = [word for word in x if word]
# print(x)
# #9
# txt = "БольшойМаленькийБиг"
# pattern = r"(?<=[а-я])([А-Я])"
# x = re.sub(pattern, r" \1", txt)
# print(x)
# #10
# txt = "АррррвИовГоо"
# pattern = r"([а-я])([А-Я])"
# x = re.sub(pattern, r"\1_\2", txt).lower()
# print(x)