import psycopg2
from psycopg2 import sql, OperationalError
###################################################################################################
def create_db(db_name):
    try:
        connection = psycopg2.connect(
            dbname='postgres', 
            user='postgres',
            password='211288',
            host='127.0.0.1',
            port='5432'
        )
        connection.autocommit = True 
        cursor = connection.cursor()

        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))

        print(f"Database '{db_name}' created successfully.")
        
    except OperationalError as e:
        if "database already exists" in str(e):
            print(f"Database '{db_name}' already exists.")
        else:
            print(f"Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
###################################################################################################
def connect_db(db_name):
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user='postgres',
            password='211288',
            host='127.0.0.1',
            port='5432'
        )
        print(f"Connected to database '{db_name}' successfully.")
        
    except OperationalError:
        print(f"Failed to connect to database '{db_name}'. Attempting to create it...")
        create_db(db_name)
###################################################################################################
def action1(cursor):
    try:
        print("Введите название: ", end='')
        title = input()
        print("Введите цену: ", end='')
        price = int(input())
        cursor.execute("INSERT INTO catalog(title, pricekg) VALUES(%s, %s)", (title, price))
    except ValueError as e:
        print(f"Ошибка: {e}")
###################################################################################################
def action2(cursor):
    try:
        print("1. Редактировать название \n2. Редактировать цену")
        print("Выберите действие: ")
        cursor.execute("SELECT id FROM catalog")
        result = [row[0] for row in cursor.fetchall()]
        print(result)

        action = int(input())
        if (not (action in [1, 2])):
            print("Выход на главное меню")
            return
        print("Введите ID: ", end='')
        id = int(input())
        if(id in result):
            if (action == 1):
                print("Введите новое название: ", end='')
                title = input()
                cursor.execute("UPDATE catalog SET title = %s WHERE id = %s", (title, id))
            elif(action == 2):
                print("Введите новую цену: ", end='')
                price = int(input())
                cursor.execute("UPDATE catalog SET pricekg = %s WHERE id = %s", (price, id))
        else:
            print(f"Ошибка: В каталоге не существует товара с ID = {id}.")
    except ValueError as e:
        print(f"Ошибка: {e}")
###################################################################################################
def action3(cursor):
    try:
        action4(cursor)
        print("Введите ID: ", end='')
        id = int(input())
        cursor.execute("SELECT id FROM catalog")
        result = [row[0] for row in cursor.fetchall()]
        if(id in result):
            cursor.execute("DELETE FROM catalog WHERE id = %s", (id,))
        else:
            print(f"Ошибка: В каталоге не существует товара с ID = {id}.")
    except ValueError as e:
        print(f"Ошибка: {e}")
###################################################################################################
def action4(cursor):
    cursor.execute("SELECT * FROM catalog")
    rows = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    print("\t\t".join(colnames)) 

    for row in rows:
        print("\t\t".join(map(str, row))) 

###################################################################################################
def action5(cursor):
    action4(cursor)
    try:
        metal_id = int(input("Введите ID металла: "))
        quantity = float(input("Введите количество кг: "))
        
        if quantity <= 0:
            print("Количество должно быть положительным числом.")
            return

        cursor.execute("SELECT title, pricekg FROM catalog WHERE id = %s;", (metal_id,))
        result = cursor.fetchone()

        if result:
            title, price_per_kg = result
            total_price = price_per_kg * quantity
            print(f"Вы выбрали: {title}")
            print(f"Цена за {quantity} кг: {total_price:.2f} руб.")
        else:
            print("Металл с таким ID не найден.")
    
    except ValueError:
        print("Пожалуйста, введите корректные данные.")

###################################################################################################
def game_loop(cursor):
    while(1):
        print("1. Добавить позицию")
        print("2. Редактировать позицию")
        print("3. Удалить позицию")
        print("4. Список цен")
        print("5. расчитать стоимость")
        print("6. закрыть программу")

        print("Что вы хотите сделать?   ", end='')
        try:
            action = int(input())
            print("##########################################")
            if(action == 1):
                action1(cursor)
            elif(action == 2):
                action2(cursor)
            elif(action == 3):
                action3(cursor)
            elif(action == 4):
                action4(cursor)
            elif(action == 5):
                action5(cursor) 
            elif(action == 6):
                break
            else:
                print("Пожалуйста, введите корректные данные.")
            print("##########################################")
        except ValueError:
            print("Пожалуйста, введите корректные данные.")
###################################################################################################
def main():
    db_name = "Prices"
    connect_db(db_name)
    connection = psycopg2.connect(
        dbname=db_name,
        user='postgres',
        password='211288',
        host='127.0.0.1',
        port='5432'
    )
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS catalog (id SERIAL PRIMARY KEY, pricekg INT, title VARCHAR(64));")
    cursor.execute("UPDATE catalog SET id = (SELECT COUNT(*) FROM catalog AS c WHERE c.id <= catalog.id);")
    game_loop(cursor)
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
###################################################################################################
if __name__ == "__main__":
    main()