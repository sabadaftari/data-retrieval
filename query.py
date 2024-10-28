import sqlite3
import pandas as pd
from utils import view_main_run_table

def query_database(db_path, table_name, filter_conditions=None, select_columns='*', limit=None):
    """
    Query the SQLite database based on given filter conditions.
    
    Parameters:
        db_path (str): Path to the SQLite database file.
        table_name (str): The table to query.
        filter_conditions (dict): Dictionary of conditions to filter by in the format {'column': 'value'}.
        select_columns (str or list): The columns to select (default is '*' for all columns).
        limit (int, optional): Maximum number of rows to return.
    
    Returns:
        pd.DataFrame: Query results as a pandas DataFrame.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # Create a cursor
    cursor = conn.cursor()

    # Prepare the base query
    if isinstance(select_columns, list):
        select_columns_str = ', '.join(select_columns)
    else:
        select_columns_str = select_columns
    
    query = f"SELECT {select_columns_str} FROM {table_name}"
    
    # Add filter conditions to the query if provided
    if filter_conditions:
        where_clauses = []
        values = []
        for col, val in filter_conditions.items():
            where_clauses.append(f"{col} = ?")
            values.append(val)
        query += " WHERE " + " AND ".join(where_clauses)

    # Add limit if specified
    if limit:
        query += f" LIMIT {limit}"

    view_main_run_table(conn,cursor)

    # Execute the query with parameters for filtering
    cursor.execute(query, tuple(values))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Get the column names from the cursor
    columns = [description[0] for description in cursor.description]
    
    # Convert results to a pandas DataFrame
    df = pd.DataFrame(results, columns=columns)
    
    # Close the connection
    conn.close()
    
    return df

if __name__ == '__main__':
    # Querying for specific 'Run' values and selecting certain columns from the Main_Run_Table
    db_path = 'multi_run_data.db'
    filter_conditions = {'Species': 'human', 'Disease': 'HCV'}
    select_columns = ['Run', 'Age', 'Disease']
    results_df = query_database(db_path, 'Main_Run_Table', filter_conditions, select_columns, limit=100)

    # Display the result
    print(results_df)
