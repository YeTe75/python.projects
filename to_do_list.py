import psycopg2 
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
load_dotenv(dotenv_path="c:/Users/user/Desktop/Projects/projects/Python projects/.env")
DB_PASSWORD = os.getenv("DB_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
print("SECRET_KEY:", os.getenv("SECRET_KEY"))
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated = "auto")
app = FastAPI()
#dotenv_path="c:/Users/user/Desktop/Projects/projects/Python projects/.env"


def get_db():
    
    conn = psycopg2.connect(
    host = "localhost",
    database = "mydb",
    user = "postgres",
    password = os.getenv("DB_PASSWORD")

)
    return conn

def create_token(user_name:str):
    expire = datetime.utcnow() + timedelta(hours=24)
    data = {"sub": user_name, "exp": int(expire.timestamp())}
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id SERIAL PRIMARY KEY,
    user_name TEXT,
    email TEXT)


 """)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id SERIAL PRIMARY KEY,
        name_of_task TEXT,
        user_id INTEGER,
        date TEXT,
        priority TEXT,
        status TEXT) """)
    

@app.post("/login") 
def login(user_name:str,password:str):
    
    with get_db() as con:
        cursor = con.cursor()
        cursor.execute("SELECT password FROM users WHERE user_name = %s",(user_name,))
        result  = cursor.fetchone()
        hashed_password = result[0]
        check_password = pwd_context.verify(password,hashed_password)
        if check_password == True:
           token = create_token(user_name)
           return {"message":"Добро пожаловать","token":token}
        else:
            return {'message': "Неверный пароль!"}
            
@app.post("/register")
def register(user_name: str, email:str,password: str):
    hashed_password = pwd_context.hash(password)
    with get_db() as conn:

        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(user_name,email,password) VALUES(%s,%s,%s)", (user_name,email,hashed_password,))

        conn.commit()
        return {"message": "Юзер зарегистрирован!"}
    

@app.post("/add_task")
def add_task(user_name: str,name_of_task: str, date:str, priority:str, status:str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE user_name = %s",(user_name,))
        result = cursor.fetchone()
        user_id = result[0]
        cursor.execute("INSERT INTO tasks(name_of_task,user_id,date,priority,status) VALUES(%s, %s, %s, %s, %s)",(name_of_task,user_id,date,priority,status,))

        conn.commit()
        return {"message": "Задание добавлено!"}


@app.get("/show_tasks/{user_name}")
def show_tasks(user_name:str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE user_name = %s",(user_name,))
        result = cursor.fetchone()
        user_id = result[0]

        cursor.execute("SELECT * FROM tasks WHERE user_id = %s",(user_id,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return rows

@app.get("/show_tasks/{user_name}/{status}")
def filt_task(user_name:str, status:str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE user_name = %s",(user_name,))
        result = cursor.fetchone()
         
         
         
        cursor.execute("SELECT * FROM tasks WHERE status = %s",(status,))
        tasks = cursor.fetchall()

        return {"message":f"Ваша таблица по статусу: {status}"}, result, tasks




@app.delete("/delete_tasks/{user_name}")
def delete_tasks(user_name:str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE user_name = %s",(user_name,))
        user = cursor.fetchone()
        user_id = user[0]

        cursor.execute("DELETE FROM users WHERE user_name = %s ",(user_name,))
        cursor.execute("DELETE FROM tasks WHERE user_id = %s",(user_id,))
        return {"message": f"Данные пользователя {user_name} были удалены."}


    
print("файл запустился!")