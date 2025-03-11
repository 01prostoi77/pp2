# import os

# path = r"C:\Users\Farkhat\Desktop\PP2\labworks\lab6"

# print("Папки:", [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
# print("Файлы:", [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
# print("Все:", os.listdir(path))

# import os

# path = r"C:\Users\Farkhat\Desktop\PP2\labworks\lab6"
# print("Существует:", os.path.exists(path))
# print("Читаемый:", os.access(path, os.R_OK))
# print("Записываемый:", os.access(path, os.W_OK))
# print("Исполняемый:", os.access(path, os.X_OK))

# import os

# path = r"C:\Users\Farkhat\Desktop\PP2\labworks\lab6"
# if os.path.exists(path):
#     print("Файл:", os.path.basename(path))
#     print("Папка:", os.path.dirname(path))
# else:
#     print("Путь dont exist")


# file_path = input()
# print("Stroki:", sum(1 for _ in open(file_path)))

# data = ["yabloko", "banana", "cherry"]
# with open("fff.txt", 'w') as f:
#     f.writelines(f"{item}\n" for item in data)
# print("Список записан в fff.txt")

# import string

# for letter in string.ascii_uppercase:
#     open(f"{letter}.txt", 'w').write(f"{letter}.txt\n")
# print("Созданы файлы A.txt - Z.txt")

# src = input("Источник: ")
# dst = input("Куда: ")
# open(dst, 'w').write(open(src).read())
# print("Файл скопирован")


# import os

# file_path = input()
# if os.path.exists(file_path) and os.access(file_path, os.W_OK):
#     os.remove(file_path)
#     print("File удален")
# else:
#     print("Удаление error")




