import sqlite3

conn = sqlite3.connect("Finance.db")

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS finance( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT,
    amount INTEGER,
    type TEXT)""")



def add_income():
    q = "доход"
    income = int(input("Введите ваш доход = "))
    type_of = input("Введите вид дохода(работа,инвестиции,выплата арендовщика и тд.) - ")
    cursor.execute("INSERT INTO finance(source,amount,type)" 
    "VALUES(?,?,?)",(type_of,income,q,))
    conn.commit()

def add_expenses():
    q = 'расход'
    expenses = int(input("Введите ваши затраты = "))
    type_of = input("Введите вид расхода(магазин,ресторан,пожертвование и тд.) - ")
    cursor.execute("INSERT INTO finance(source,amount,type)" \
    "VALUES(?,?,?)",(type_of,expenses,q,))
    conn.commit()


def show_balance():
    q = input("Что вы хотите посмотреть?(доход или расход) - ").lower()
    if q == "доход":
        cursor.execute("SELECT * FROM finance WHERE type = ? ",(q,))
        income = cursor.fetchall()
        for row in income:
            print(f"Название: {row[1]}, количество: {row[2]}")

    elif q == "расход":
        cursor.execute("SELECT * FROM finance WHERE type = ?",(q,))
        expenses = cursor.fetchall()
        for rowe in expenses:
              print(f"Название: {rowe[1]}, количество: {rowe[2]}")


def show_average_expenses():
    q = 'расход'
    cursor.execute("SELECT amount FROM finance WHERE type = ?",(q,))
    ex = cursor.fetchall()
    numbers = [row[0] for row in ex ]
    average = sum(numbers) / len(numbers)
    print(f"Ваши средние расходы = {average}")

def delete_trans():
    try:
        trans = int(input("Введите id транзакции(помните - id начианется с 0) = "))
        cursor.execute("SELECT * FROM finance")
        name = cursor.fetchall()
        for names in name:
            if trans == names[0]:
                cursor.execute("DELETE FROM finance WHERE id = ?",(trans,))
                conn.commit()
                print(f"Транзакция была удалена!")
    except ValueError:
        print("Id должно быть цифрой!")


def main():
    print("ДОБРО ПОЖАЛОВАТЬ В 'РЕГУЛЯРОВЩИК ФИНАНСОВ'!!!")
    
    while True:
        choice = input("Что желаете сделать?: \n" \
    "1.Добавить доходы и расходы?\n" \
    "2.Показать полный список\n" \
    "3.Показать средние затраты\n" \
    "4.Удалить транзакцию\n" \
    "5.Завершить\n" \
    "Ваш выбор - ")
        
        if choice == '1':
            c = input("1.Внести\n" \
            "2.Снять\n" \
            "Ваш выбор - ")
            if c == '1':
                add_income()
            elif c == '2':
                add_expenses()
            else:
                print("Напишите 1 или 2")
           
        elif choice == '2':
            show_balance()
        elif choice == '3':
            show_average_expenses()
        elif choice == '4':
            delete_trans()
        elif choice == '5':
            print("До свидания!")
            break
        else:
            print("Что-то я не знаю такой команды!")

main()
conn.close()