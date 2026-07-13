import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel


#http://localhost:8000/docs

app  = FastAPI()

def get_db():
    conn = sqlite3.connect("Bookorrecipes.db",check_same_thread= False)
    return conn

with get_db() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS names(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT)
     """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS recipes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER,
    ingredients TEXT)""")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS steps(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    step_id INTEGER,
    step TEXT,
    weight INTEGER)

 """)
class Recipe(BaseModel):
        name:str
        ingredients:list[str]
        step:list[str]
        weight:list[int]
@app.post("/add_recipe")
def add_recipe(recipe:Recipe):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO names(name)" \
        "VALUES(?)",(recipe.name,))
        recipe_id = cursor.lastrowid
        
        for ing in recipe.ingredients:

            cursor.execute("INSERT INTO recipes(recipe_id,ingredients) " \
            "VALUES(?,?)",(recipe_id,ing,))
       
        for st,w in zip(recipe.step,recipe.weight):
            cursor.execute("INSERT INTO steps(step_id,step,weight)" \
            "VALUES(?,?,?)",(recipe_id,st,w,))

       

        conn.commit()
        return {"message": "Рецепт добавлен!"}
    
@app.get("/Show_recipe")
def show_recipe(name:str):
    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM names WHERE name = ?",(name,))
        result = cursor.fetchone()
        recipe_id = result[0]

        cursor.execute("SELECT ingredients FROM recipes WHERE recipe_id = ?",(recipe_id,))
        ingredients = cursor.fetchall()
        cursor.execute("SELECT step,weight FROM steps WHERE step_id = ?",(recipe_id,))
        steps = cursor.fetchall()
        return {
            "name":name,

            "ingredients":ingredients,
             
             "steps":steps
        }


@app.delete("/delete_recipe")
def delete_recipe(name: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM names WHERE name = ?",(name,))
        recipe = cursor.fetchone()
        recipe_id = recipe[0]


        cursor.execute("DELETE FROM names WHERE name = ?",(name,))
        cursor.execute("DELETE FROM recipes WHERE recipe_id = ?",(recipe_id,))
        cursor.execute("DELETE FROM steps WHERE step_id = ?",(recipe_id,))


        conn.commit()
            
        return {"message": f"Рецепт блюда '{name}' было удалено!"}
    
@app.put("/update_recipe")
def update_recipe(recipe: Recipe,name:str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM names WHERE name = ?",(name,))
        result = cursor.fetchone()
        recipe_id = result[0]


        cursor.execute("DELETE FROM recipes WHERE recipe_id = ?",(recipe_id,))
        cursor.execute("DELETE FROM steps WHERE step_id = ?",(recipe_id,))


        conn.commit()


        for ing in recipe.ingredients:
            cursor.execute("INSERT INTO recipes(recipe_id,ingredients)"
            "VALUES(?,?)",(recipe_id,ing,))

        for st,w in zip(recipe.step,recipe.weight):
            cursor.execute("INSERT INTO steps(step_id,step,weight)" \
            "VALUES(?,?,?)",(recipe_id,st,w,))

        cursor.execute("UPDATE names SET name = ? WHERE name = ? ",(recipe.name,name,))

        conn.commit()

        return {"message": "Рецепт обновлен!"}

       