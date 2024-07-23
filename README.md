# Project Notes

Link:
http://curatingmenus.org/data_dictionary/


## Rubric/Checklist:

1. Description of Data Cleaning Performed
  - Identify and describe all (high-level) data cleaning steps you have performed. (20 points)
  - For each high-level data cleaning step you have performed, explain its rationale. Was the step really required to support use case U1? Explain. If not, explain why those steps were still useful. (20 points)

2. Document data quality changes
  - Quantify the results of your efforts, e.g., by providing a summary table of changes: Which columns changed? How many cells (per column) have changed, etc.? (10 points)
  - Demonstrate that data quality has been improved, e.g., by devising IC-violation reports (answers to denial constraints) and showing the difference between number of IC violations reported before and after cleaning. (10 points)

3. Create a workflow model
  - A visual representation of your overall (or “outer”) workflow W1, e.g., using a tool such as YesWorkflow. At a minimum, you should identify key inputs, outputs, and steps of the workflow, along with dependencies between these. Key phases and steps of your data cleaning project may include, e.g., data profiling, data loading, data cleaning, IC violation checks, etc. Explain the design of W1 and why you’ve chosen the tools that you have in your overall workflow. (10 points)
  - A detailed (possibly visual) representation of your “inner” data cleaning workflow W2 (e.g., if you’ve used OpenRefine, you can use the OR2YW tool). (10 points)
4. Conclusions & Summary (10 points)
  - Please provide a concise summary and conclusions of your project, including lessons learned.
  - Reflect on how work was completed. You should summarize the contributions of each team member here (for teams with >= 2 members).
5. Submission of supplementary materials in a single ZIP file (10 points)
  - Workflow Model
  - OpenRefine Recipe, Other scripts, provenance files
  - Queries
  - Original (“dirty”) and Cleaned datasets, Please provide a accessible Box folder link in a plain text file: DataLinks.txt

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