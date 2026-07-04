#Кошелек
"""class Wallet:
    def __init__(self, balance = 1000):
        self.balance = balance

    def deposit(self,amount):
        self.balance += amount
        print(f'Ваш счет был пополнен на {amount}')

class WalletElite(Wallet):
    def deposit(self,amount):
        
        super().deposit(amount)
        bonus = (amount*0.15)
        self.balance = bonus+amount
        
class WalletMegaElite(WalletElite):
    def deposit(self):
        amount = int(input('Введите сумму для пополнения = ')) 
        super().deposit(amount)
        bonus = amount*0.2
        self.balance = bonus+amount
        print(f'Вам на баланс пришел бонус в размере:{bonus}')
        print(f'Ваш счет:{self.balance}')

wallet1 = WalletMegaElite()
wallet1.deposit()"""

#Зоопарк
"""class Animal:
    def __init__(self):
        self.animal = input('Write your animal: ')

    def make_sound(self):
        self.sound = input('what sound it makes?')

class Food(Animal):
    def __init__(self):
        super().__init__()
        self.food = input('What it eats: ')

    def make_sound(self):
         super().make_sound()
         print(f'{self.animal} makes {self.sound} and eats {self.food}')

animal = Food()
animal.make_sound()"""
"""import json
tasks = []
finished_tasks = []

def load_tasks():
    global tasks,finished_tasks
    try:
        with open("tasks.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
            tasks = data["tasks"]
            finished_tasks = data["finished_tasks"]
    except FileNotFoundError:
        tasks = []
        finished_tasks = []

def save_tasks():
    data = {
        "tasks": tasks,
        "finished_tasks": finished_tasks
    }
    with open("tasks.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def add_task():
    task = input('Какое задание вы хотите добавить? - ')
    tasks.append(task)
    save_tasks()
    print(f'Ваше задание "{task}" было добавлено!')
    return tasks 

def finished_task():
    print(f"Ваши задания:{tasks}")
    f = int(input('Введите индекс выполненого задания(индекс первого задания = 0): '))
    for ind,task in enumerate(tasks):
        if f == ind:
            print('Отлично!Занес его в список')
            finished_tasks.append(task)
            tasks.remove(task)
            save_tasks()
            return finished_tasks    

def remove_tasks():
    index = int(input('Введите индекс задания которого вы хотите удалить(индексы начинаются с 0:)'))
    for ind,task in enumerate(tasks):
        if ind == index:
            tasks.remove(task)
            return tasks



def show_tasks():
    print(f'Ваши задачи:{tasks}')
    print(f'Ваши выполненные задания: {finished_tasks}')


def main():
    load_tasks()
    print('Привет!Добро пожаловать в "Чек-лист"!')
    while True:
        fun = input('Вот ваши команды! - \n' \
        '1.Добавить в список дел задание\n' \
        '2.Показать список\n' \
        '3.Убрать задание\n' \
        '4.Добавить задание в список выполненных заданий\n' \
        '5.Завершить\n'
        'Что выберете? - ')
        if fun == '1':
            add_task()
        elif fun == '2':
            show_tasks()
        elif fun == '3':
            remove_tasks()
        elif fun == '4':
            finished_task()
        else:
            print('Рад что вы смогли составить список!До нoвых встреч!')
            break
main()"""




"""from time import sleep
import json

contacts = []

def load_data():
    global name,phone,email,contacts
    try:
        with open("contacts.json",'r',encoding='utf-8') as file:
            contacts = json.load(file)
    except FileNotFoundError:
        contacts = []
        
def save_data():
    with open("contacts.json",'w',encoding='utf-8') as file:
        json.dump(contacts,file,ensure_ascii=False,indent=2)

def main_data():
    global contacts
    name = input("Введите ваше имя: ")
    phone = input("Введите ваш номер телефона: ")
    email = input("Введите ваш электронный адрес: ")
    data = {"Name:":name, "Phone num.:":phone,"Email:":email}
    sleep(3)
    print(' ')
    ask = input("Правильно ли введена ваша информация?(да/нет):").lower()
    print(f"Name - {name}; Phone num - {phone}; Email add. - {email}")
    sleep(2)
    if ask == "да":
        print("Замечательно!Ввел данные в JSON файл")
        contacts.append(data)
        save_data()
    elif ask == "нет":
        print("Исправьте пожалуйста!")
        name = input("Введите ваше имя: ")
        phone = input("Введите ваш номер телефона: ")
        email = input("Введите ваш электронный адрес: ")
        sleep(2)
        print("Отлично!Уже все занесено!")
        contacts.append(data)
        save_data()
    return name, phone, email

def show_data():
    print(f'Секунду,сейчас покажу вам списки контактов')
    sleep(3)
    for contact in contacts:
        print(f'Вот ваши контакты- {contact["Name:"]}; {contact["Phone num.:"],}; {contact["Email:"]}')

def delete_contact():
    print(contacts)
    delete = input("Выберите контакт который хотите удалить - ")
        
    for data in contacts:
        if  delete == data["Name:"] or delete == data["Phone num.:"] or delete == data["Email:"]:
            print("Принято!Уже удалено!")
            contacts.remove(data)
            save_data()
           

def searching_data():
    for data in contacts:
        search = input("Впишите имя,или номер телефона или электр.почту человека которого хотите найти - ")
        if  search == data["Name:"] or search == data["Phone num.:"] or search == data["Email:"]:
            print("Сейчас попробую найти для вас что-нибудь!")
            sleep(3)
            print("...")
            print(f"Вроде что-то нашлось!Держите примеры- {data["Name:"]};{data["Phone num.:"]},{data["Email:"]}")
        else:
            print("К сожалению найти похожего не удалось")

def main():
    load_data()
    print("Welcome to Phone book!")
    while True:
        c = input("Команды-\n" \
        "1.Добавление номеров,имен и электронных почт\n" \
        "2.Нахождение контакта по номеру,имени или электронной почты\n" \
        "3.Удаление контакта\n" \
        "4.Показ ваших контактов\n" \
        "5.Выход\n" \
        "Что желаете выбрать? - ")

        if c == '1':
            main_data()
        elif c == '2':
            searching_data()
        elif c == '3':
            delete_contact()
        elif c == '4':
            show_data()
        elif c == '5':
            print("До свидания!")
            sleep(2)
            break
        else:
            print("Что-то я не знаю что это значит!")



main()"""

#Знакомство с SQLite

# import sqlite3

# conn = sqlite3.connect("LearningSQL.db")

# print("БД подключена!")

# cursor = conn.cursor()

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS contacts(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         phone TEXT,
#         email TEXT       
#                )
               
#                """)

# cursor.execute("""
#     INSERT INTO contacts(name,phone,email)
#     VALUES(?,?,?)""",("Yete","+18394932","yete@mail.ru"))

# cursor.execute("""
#     UPDATE contacts SET phone = '+70138483443' WHERE name = 'Yete'

#  """)
# print("Обновлено успешно!")

# cursor.execute("SELECT * FROM contacts")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
# conn.commit()
# print("Таблица установлена!")

# conn.close()

import sqlite3 

conn = sqlite3.connect("Project.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS journal(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        names TEXT
        )

 """)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        grade INTEGER)
 """)
print("Бд установлено!")

a = 0
while a <7:
    name = input("Введите ваше имя- ")

    cursor.execute("""INSERT INTO journal(names)
               VALUES(?)""",(name,))

    print("Внес в БД!")


    grade = int(input("Введите ваши оценки - "))
    student_id = cursor.lastrowid
    cursor.execute("""
        INSERT INTO grades(student_id,grade)
        VALUES(?,?)""",(student_id,grade,)
    )

    print("Внес в БД!")


    cursor.execute("SELECT * FROM journal")
    raws = cursor.fetchall()
    for raw in raws:
        print(raw)

    cursor.execute("SELECT * FROM grades")
    g = cursor.fetchall()
    for grades in g:
        print(grades)

    numbers = [grades[2] for grades in g]
    average = sum(numbers) / len(numbers)

    print(f"Средняя оценка учеников = {average}")
    conn.commit()
    a += 1

conn.close()
