import sqlite3 

conn = sqlite3.connect("Journal.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
               )
 """)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS grades(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    grade INTEGER
               
               )

 """)

def add_students():
    name = input("Введите имя ученика: ")
    cursor.execute("SELECT id FROM students WHERE name = ?",(name,))
    result = cursor.fetchone()
    if result:
        print(f"{name} уже имеется в бд!")
        return result[0]
    else:
        print(f'{name} нет в БД,добавляю!')
        cursor.execute("""
       INSERT INTO students(name)
       VALUES(?)""",(name,))
        conn.commit()
        return cursor.lastrowid

def add_grades(student_id):
    grade = int(input("Введите вашу оценку: "))
    cursor.execute("""
    INSERT INTO grades(student_id,grade)
    VALUES(?,?)""",(student_id,grade,))
    conn.commit()

def show_full_journal():
    name = input("Введите имя - ")
    cursor.execute("SELECT id FROM students WHERE name = ?",(name,))
    names = cursor.fetchone()
    student_id = names[0]
    

    cursor.execute("SELECT grade FROM grades WHERE student_id = ?",(student_id,))
    grades = cursor.fetchall()
    print(f"Оценки {name}:")
    for grade in grades:
        print(grade[0])

def show_average():
    global grade
    name = input("Введите имя - ")
    average_of = input("1.Показать среднюю оценку ученика\n" \
    "2.Показать среднюю оценку класса\n" \
    "Что выберет? - ")
    if average_of == '1':
        cursor.execute("SELECT id FROM students WHERE name = ?",(name,))
        grades = cursor.fetchone()
        student_id = grades[0]
        cursor.execute("SELECT grade FROM grades WHERE student_id =?",(student_id,))
        all_grades = cursor.fetchall()
        numbers = [g[0] for g in all_grades]
        average = sum(numbers)/len(numbers)
        print(f"Средняя оценка ученика {name} = {average}")
        
    elif average_of == '2':
        cursor.execute("SELECT grade FROM grades" )
        gr = cursor.fetchall()
        numb = [g[0]for g in gr]
        num = sum(numb) / len(numb)
        print(f"Средняя оценка класса = {num}")

def delete_from_journal():
    global student_id,name
    delete =  input("Введите имя ученика,которого хотите удалить - ")
    cursor.execute("SELECT * FROM students")
    names = cursor.fetchall()
    for name in names:
        print(name)
        if delete == name[1]:
            student_id = name[0]
            cursor.execute("""
            DELETE FROM students WHERE name = ?""",(delete,))
            cursor.execute("""DELETE FROM grades WHERE student_id = ?  """,(student_id,))
            conn.commit()
            print(f"{delete} был удален")
def main():
    print("WELCOME TO SCHOOL JOURNAL")
    while True:
        choice = input("Что желаете сделать? -\n" \
        "1.Добавить Имя и Фамилию ученика,а также его оценки\n" \
        "2.Показать полный журнал\n" \
        "3.Удалить данные ученика\n"
        "4.Показать среднюю оценку\n" \
        "5.Закончить\n" \
        "Что предпочитаете? - ")


        if choice == '1':
            student_id = add_students()
            add_grades(student_id)
        elif choice == '2':
            show_full_journal()
        elif choice == '3':
            delete_from_journal()
        elif choice == '4':
            show_average()
        elif choice == '5':
            print("До свидания!")
            break 
        else:
            print("Что-то я не знаю такой команды!")

main()
conn.close()