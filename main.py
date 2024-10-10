from uuid import uuid4
import mysql.connector
from faker import Faker
import random
from time import sleep

disable_second_replic = False

while True:
    master = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="manyusers",
    )

    slave1 = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="manyusers",
        port=3307
    )

    slave2 = None
    if not disable_second_replic:
        slave2 = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="manyusers",
            port=3308
        )

    fake = Faker()
    master_cursor = master.cursor()
    slave1_cursor = slave1.cursor()
    slave2_cursor = None
    if not disable_second_replic:
        slave2_cursor = slave2.cursor()

    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}+{str(uuid4())[:8]}@example.com"
    birth_date = fake.date_of_birth(minimum_age=18, maximum_age=80)
    gender = random.choice(['M', 'F', 'O'])
    sql = "INSERT INTO users (first_name, last_name, email, birth_date, gender) VALUES (%s, %s, %s, %s, %s)"
    master_cursor.execute(sql, (first_name, last_name, email, birth_date, gender))
    master.commit()
    sleep(2)
    master_cursor.execute("SELECT COUNT(*) FROM users")
    slave1_cursor.execute("SELECT COUNT(*) FROM users")
    second_result = 0
    if not disable_second_replic:
        slave2_cursor.execute("SELECT COUNT(*) FROM users")
        second_result = slave2_cursor.fetchone()[0]
    print(f"Master {master_cursor.fetchone()[0]}, Slave1 {slave1_cursor.fetchone()[0]}, Slave2 {second_result}")

    master_cursor.close()
    slave1_cursor.close()
    if not disable_second_replic:
        slave2_cursor.close()
        slave2.close()
    master.close()
    slave1.close()



