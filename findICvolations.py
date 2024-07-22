import sqlite3

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

if __name__ == "__main__":
    violations = check_constraints()
    for table, table_violations in violations.items():
        print(f"Violations in {table}:")
        for violation in table_violations:
            print(violation)