# Project Notes

Link:
http://curatingmenus.org/data_dictionary/

## Integrity Constraints and Requirements

### Dish
- `dish_id` in `Dish` must be unique
- each `dish_id` in `Dish` must have a unique `name`
- `name` in `Dish` must be unique
- `menus_appeared` in `Dish` must be an integer greater than or equal to 0
- `menus_appeared` in `Dish` must be less than or equal to the number of menus that contain the dish
- `first_appeared` in `Dish` must be a date
- `last_appeared` in `Dish` must be a date
- `first_appeared` in `Dish` must be less than or equal to `last_appeared`
- `lowest_price` in `Dish` must be a float greater than or equal to 0
- `highest_price` in `Dish` must be a float greater than or equal to 0
- `lowest_price` in `Dish` must be less than or equal to `highest_price`

### Menu
- `id` in `Menu` must be unique
- `sponsor` in `Menu` must be a string
- `event` in `Menu` must be a string
- `venue` in `Menu` must be a string
- `place` in `Menu` must be a string
- `physical_description` in `Menu` must be a string
- `occasion` in `Menu` must be a string
- `notes` in `Menu` must be a string
- `call_number` in `Menu` must be a string
- `location` in `Menu` must be a string
- `currency` in `Menu` must be a string
- `status` in `Menu` must be a string
- `page_count` in `Menu` must be equal to the number of pages in the menu
- `dish_count` in `Menu` must be equal to the number of dishes in the menu
- `date` in `Menu` contains no data unfortunately

### MenuItem
- `id` in `MenuItem` must be unique
- `menu_page_id` in `MenuItem` must be a valid `MenuPage` id
- `price` in `MenuItem` must be a float greater than or equal to 0
- `high_price` in `MenuItem` must be a float greater than or equal to 0
- `high_price` must be consistent with the prices in `Dish`
- `dish_id` in `MenuItem` must be a valid `Dish` id
- `created_at` in `MenuItem` must be a date
- `updated_at` in `MenuItem` must be a date
- `updated_at` must be greater than or equal to `created_at`

### MenuPage
- `id` in `MenuPage` must be unique
- `menu_id` in `MenuPage` must be a valid `Menu` id
- `page_number` in `MenuPage` must be an integer greater than or equal to 1

## File: 2sql.py

### Functions

#### `csv2db()`
- **Purpose**: Imports CSV files from the `NYPL-menus` directory into a SQLite database.
- **Key Points**:
  - Connects to `database.db`.
  - Iterates over CSV files in the `NYPL-menus` directory.
  - Reads each CSV file into a DataFrame and writes it to the database.

#### `usecase_query()`
- **Purpose**: Executes a query to find menus that contain all top 5 dishes by `menus_appeared` in the `Dish` table.
- **Key Points**:
  - Connects to `database.db`.
  - Joins `Menu`, `MenuPage`, `MenuItem`, and `Dish` tables.
  - Filters for top 5 dishes and menus with status 'complete'.
  - Groups by menu ID and ensures each menu contains all 5 dishes.