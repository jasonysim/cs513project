import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import sqlite3
import pandas as pd
import numpy as np

def csv2db(csv_directory:str,db_path:str,db_name:str='database',outdir:str=None):
    if db_path is None:
        db_path = os.getcwd()
    conn = sqlite3.connect(f'{db_path}/{db_name}.db')
    for filename in os.listdir(csv_directory):
        if filename.endswith('.csv'):
            csv_path = os.path.join(csv_directory, filename)
            df = pd.read_csv(csv_path)
            table_name = os.path.splitext(filename)[0]            
            df.to_sql(table_name, conn, if_exists='replace', index=False)

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
    menu_columns = ['id', 'name', 'sponsor', 'event', 'venue', 'place', 'physical_description', 'occasion', 'notes', 'call_number', 'keywords', 'language', 'date', 'location', 'location_type', 'currency', 'currency_symbol', 'status', 'page_count', 'dish_count']
    result_df = pd.read_sql_query(query, conn)
    result_df.columns = menu_columns
    conn.close()
    return result_df

def compare_dataframes(original_df, updated_df):
    if original_df.shape != updated_df.shape:
        raise ValueError("The input dataframes must have the same shape.")
    diff_df = pd.DataFrame(np.nan, index=original_df.index, columns=original_df.columns)
    for column in original_df.columns:
        diff_mask = original_df[column] != updated_df[column]
        diff_df.loc[diff_mask, column] = updated_df.loc[diff_mask, column]
    return diff_df

def summarize_diff(diff_df):
    # count the number of non-NaN values in the diff_df
    number_changes = diff_df.count()
    perc_changes = round(number_changes / len(diff_df),4)
    diff_summary = pd.DataFrame({'number_changes': number_changes, 'perc_changes': perc_changes})

    # sort the diff_summary by number_changes
    diff_summary = diff_summary.sort_values(by='number_changes', ascending=True)

    diff_summary.loc['all_records'] = 0
    diff_summary.loc['all_records','number_changes'] = (diff_df.sum(axis=1)>0).sum()
    diff_summary.loc['all_records','perc_changes'] = round(diff_summary.loc['all_records','number_changes'] / len(diff_df),4)
    return diff_summary

def visualize_diff(original_df, updated_df):

    diff_summary = summarize_diff(compare_dataframes(original_df, updated_df))

    fig, ax = plt.subplots(figsize=(10, 5))

    width = 0.1
    diff_summary.number_changes.plot(kind='barh', ax=ax, position=1, width=width, color='blue')

    # second y axis for percentage changes
    ax2 = ax.twiny()
    ax2.set_xlim(0, 1)
    diff_summary.perc_changes.plot(kind='barh', ax=ax2, position=0, width=width, color='red')

    # rotate x axis labels
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)    

    # add legend    
    red_patch = mpatches.Patch(color='red', label='Percentage Changes')
    blue_patch = mpatches.Patch(color='blue', label='Number of Changes')
    ax.legend(handles=[blue_patch, red_patch], loc='lower right')

    ax.set_xlabel('Number of Changes')
    ax2.set_xlabel('Percentange Change')

    # set tight layout for fig
    fig.tight_layout()

    # save fig
    fig.savefig('diff_summary.png')