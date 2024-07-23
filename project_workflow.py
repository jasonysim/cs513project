import os
import sqlite3
import pandas as pd
import numpy as np

def check_constraints():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    queries = {
        "Dish": [
            # id must be unique
            "SELECT * FROM Dish GROUP BY id HAVING COUNT(*) > 1;",
            # name must be unique for a given id
            "SELECT * FROM Dish GROUP BY id HAVING COUNT(DISTINCT name) > 1;",
            # menus_appeared must be greater than or equal to 0
            "SELECT * FROM Dish WHERE menus_appeared < 0;",
            # first_appeared must be less than or equal to last_appeared
            "SELECT * FROM Dish WHERE first_appeared > last_appeared;",
            # lowest_price in Dish must be a float greater than or equal to 0
            "SELECT * FROM Dish WHERE lowest_price < 0;",
            # highest_price in Dish must be a float greater than or equal to 0
            "SELECT * FROM Dish WHERE highest_price < 0;",
            # lowest_price in Dish must be less than or equal to highest_price
            "SELECT * FROM Dish WHERE lowest_price > highest_price;",
        ],
        "Menu": [
            # id in Menu must be unique
            "SELECT * FROM Menu GROUP BY id HAVING COUNT(*) > 1;",
        ],
        "MenuItem": [
            # id in MenuItem must be unique
            "SELECT * FROM MenuItem GROUP BY id HAVING COUNT(*) > 1;",
            # price in MenuItem must be a float greater than or equal to 0
            "SELECT * FROM MenuItem WHERE price < 0;",
            # high_price in MenuItem must be a float greater than or equal to 0
            "SELECT * FROM MenuItem WHERE high_price < 0;",
            # menu_id in MenuItem must be a valid foreign key
            "SELECT * FROM MenuItem WHERE menu_page_id NOT IN (SELECT id FROM MenuPage);",
            # dish_id in MenuItem must be a valid foreign key
            "SELECT * FROM MenuItem WHERE dish_id NOT IN (SELECT id FROM Dish);",
            # updated_at must be greater than or equal to created_at
            "SELECT count(*) FROM MenuItem WHERE updated_at < created_at;",
        ],
        "MenuPage": [
            # id in MenuPage must be unique
            "SELECT * FROM MenuPage GROUP BY id HAVING COUNT(*) > 1;",
            # menu_id in MenuPage must be a valid foreign key
            "SELECT * FROM MenuPage WHERE menu_id NOT IN (SELECT id FROM Menu);",
            # page_number in MenuPage must be greater than or equal to 1
            "SELECT * FROM MenuPage WHERE page_number < 1;",
        ]
    }

    violations = {}

    for table, table_queries in queries.items():
        violations[table] = []
        for query in table_queries:
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                violations[table].append({query: result})

    conn.close()
    return violations

def compare_dataframes(original_df, updated_df):
    if original_df.shape != updated_df.shape:
        raise ValueError("The input dataframes must have the same shape.")
    
    diff_df = pd.DataFrame(np.nan, index=original_df.index, columns=original_df.columns)
    
    for column in original_df.columns:
        diff_mask = original_df[column] != updated_df[column]
        diff_df.loc[diff_mask, column] = updated_df.loc[diff_mask, column]

    diff_df = diff_df.dropna(how='all')

    return diff_df



dish_columns = ['id', 'name', 'description', 'menus_appeared', 'times_appeared', 'first_appeared', 'last_appeared', 'lowest_price', 'highest_price']
menu_columns = ['id', 'name', 'sponsor', 'event', 'venue', 'place', 'physical_description', 'occasion', 'notes', 'call_number', 'keywords', 'language', 'date', 'location', 'location_type', 'currency', 'currency_symbol', 'status', 'page_count', 'dish_count']
menuitem_columns = ['id', 'menu_page_id', 'price', 'high_price', 'dish_id', 'created_at', 'updated_at', 'xpos', 'ypos']
menupage_columns = ['id', 'menu_id', 'page_number', 'image_id', 'full_height', 'full_width', 'uuid']

def csv2db():

    conn = sqlite3.connect('database.db')
    
    csv_directory = 'NYPL-menus'    
    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            csv_path = os.path.join(csv_directory, filename)
            df = pd.read_csv(csv_path)
            
            table_name = os.path.splitext(filename)[0]            
            df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    conn.close()

def usecase_query():

    conn = sqlite3.connect('database.db')
    
    # Menus that contain all top 5 dishes by menus_appeared in Dish table
    query = """
    SELECT DISTINCT m.*
    FROM Menu m
    JOIN MenuPage mp ON m.id = mp.menu_id
    JOIN MenuItem mi ON mp.id = mi.menu_page_id
    JOIN Dish d ON mi.dish_id = d.id
    WHERE d.id IN (
        SELECT id
        FROM Dish
        ORDER BY menus_appeared DESC
        LIMIT 5
    ) AND m.status = 'complete'
    GROUP BY m.id
    HAVING COUNT(DISTINCT d.id) = 5;
    """
    result_df = pd.read_sql_query(query, conn)
    result_df.columns = menu_columns
    conn.close()
    return result_df