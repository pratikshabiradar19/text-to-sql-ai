import sqlite3
import pandas as pd
from dotenv import load_dotenv
import os
import google.generativeai as genai

import streamlit as st

load_dotenv()

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

DB_SCHEMA = """
Database: E-Commerce Store
Tables:
1. customers - customer_id, name, city, email
2. products - product_id, product_name, category, price
3. orders - order_id, customer_id, product_id, quantity, order_date, total_amount
Relationships:
- orders.customer_id connects to customers.customer_id
- orders.product_id connects to products.product_id
"""

def clean_sql(sql):
    sql = sql.replace("```sql", "").replace("```", "").strip()
    lines = sql.split('\n')
    clean_lines = []
    found_start = False
    for line in lines:
        stripped = line.strip().upper()
        if stripped.startswith('SELECT') or stripped.startswith('WITH'):
            found_start = True
        if found_start:
            clean_lines.append(line)
    if clean_lines:
        sql = '\n'.join(clean_lines).strip()
    return sql

def generate_sql(user_question):
   models_to_try = [
    "models/gemini-2.0-flash",
    "models/gemini-flash-latest",
]
    prompt = f"""You are an expert SQL assistant working with SQLite.
Here is the database schema:
{DB_SCHEMA}
Convert this question to a valid SQLite SQL query:
"{user_question}"
Rules:
- Return ONLY the raw SQL query
- No explanations
- No markdown
- No backticks
- Start directly with SELECT or WITH
- Use exact column and table names from schema
- Use JOIN when combining tables
- Use ORDER BY and LIMIT for top or bottom results"""

    last_error = None
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            sql = response.text.strip()
            sql = clean_sql(sql)
            print(f"Used model: {model_name}")
            return sql
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            last_error = e
            continue
    raise Exception(f"All models failed. Last error: {last_error}")

def run_query(sql_query):
    try:
        conn = sqlite3.connect("ecommerce.db")
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df, None
    except Exception as e:
        return None, str(e)

def ask(user_question):
    try:
        sql = generate_sql(user_question)
        df, error = run_query(sql)
        return sql, df, error
    except Exception as e:
        return "Could not generate SQL", None, str(e)