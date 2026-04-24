import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="contract_analyzer",
        port=3306   # IMPORTANT: your XAMPP uses 3306
    )

def insert_contract(text):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO contracts (contract_text) VALUES (%s)"
    cursor.execute(query, (text,))

    conn.commit()

    contract_id = cursor.lastrowid

    conn.close()

    return contract_id

def insert_clause(contract_id, clause, risk):
    conn = get_connection()
    cursor = conn.cursor()

    query = "INSERT INTO clauses (contract_id, clause_text, risk_level) VALUES (%s, %s, %s)"
    cursor.execute(query, (contract_id, clause, risk))

    conn.commit()
    conn.close()


def get_keywords():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT keyword, risk_type FROM keywords")

    data = cursor.fetchall()

    conn.close()

    return data

import database

print(database.get_keywords())