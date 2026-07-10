from fastapi import FastAPI
import sqlite3

#python -m uvicorn main:app --reload
#http://localhost:8000/docs

app = FastAPI()

def get_db():
    conn = sqlite3.connect("project.db",check_same_thread= False)
    return conn

with get_db() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS finance(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        amount INTEGER,
        type TEXT
                 
                 )

 """)

@app.post("/transactions")
def add_transaction(source: str, amount: int, type: str):
    with get_db() as conn:
        conn.execute(
            "INSERT INTO finance(source,amount,type) VALUES(?,?,?)",
            (source, amount, type)
        )
    return {"message": "Транзакия добавлена!"}


@app.get("/balance")
def show_balance():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM finance WHERE type = ?",('income',))
        numbers = cursor.fetchone()
        n = numbers[0]
        


        cursor.execute("SELECT SUM(amount) FROM finance WHERE type = ?",('expense',))
        num = cursor.fetchone()
        s = num[0]

        balance = n - s
        return {"message": f"Ваш баланс  - {balance}"}
    

@app.delete("/delete/{id}")
def delete_balance(id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM finance WHERE id = ?",(id,))
        return {"message": "Транзакция была удалена!"}
        
        
@app.get("/transactions/all")
def get_transaction():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM finance")
        transaction = cursor.fetchall()
        return transaction

@app.get("/")
def home():
    return{"message": "Привет мир!"}


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}"} 