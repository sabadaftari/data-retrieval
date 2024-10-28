import time
from functools import wraps
from ruamel.yaml import YAML

def measure_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time} seconds")
        return result
    return wrapper


@measure_execution_time
def read_hparams(URL: str) -> dict:
    """
    Read hyperparameters from a YAML file.

    Args:
    - URL (str): The URL or local file path to the YAML file containing hyperparameters.

    Returns:
    - params (dict): A dictionary containing the hyperparameters.
    """
    yaml = YAML(typ="safe", pure=True)
    yaml.default_flow_style = False

    # Read the YAML file
    with open(URL, "r") as f:
        params = yaml.load(f)

    return params

import os
import shutil

@measure_execution_time
def move_latest_file(download_folder, destination_folder):
    # Get all files in the download folder
    files = [f for f in os.listdir(download_folder) if os.path.isfile(os.path.join(download_folder, f))]
    
    # If no files found, exit the function
    if not files:
        print("No files in the download folder.")
        return
    
    # Get the latest file based on modification time
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(download_folder, f)))
    
    # Construct full file paths
    source_path = os.path.join(download_folder, latest_file)
    destination_path = os.path.join(destination_folder, latest_file)
    
    # Move the file
    shutil.move(source_path, destination_path)
    
    print(f"Moved file: {latest_file}")
    print(f"From: {source_path}")
    print(f"To: {destination_path}")


import subprocess
@measure_execution_time
def run_shell_script(script_path):
    try:
        # Use subprocess.run to execute the shell script
        result = subprocess.run(['bash', script_path], check=True, text=True, capture_output=True)
        
        # Print the output of the shell script
        print("Script output:")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        # Handle errors if the script fails
        print(f"Error occurred: {e}")
        print(f"Script error output: {e.stderr}")


# Function to create a table for each dataframe and link it to the Main_Run_Table via a foreign key
@measure_execution_time
def view_main_run_table(conn, cursor):
    # Query to select all data from Main_Run_Table
    cursor.execute('SELECT * FROM Main_Run_Table')
    
    # Fetch all the rows from the result
    rows = cursor.fetchall()
    
    # Get the column names from the cursor description
    column_names = [description[0] for description in cursor.description]
    
    # Print the column names and rows
    print(" | ".join(column_names))
    print("-" * 50)
    for row in rows:
        print(" | ".join([str(val) for val in row]))


@measure_execution_time
def insert_into_main_table_if_not_exists(metadata_dict, conn, cursor):
    """
    Inserts the Run into the Main_Run_Table if it doesn't already exist.
    
    Parameters:
        metadata_dict (dict): Metadata dictionary that contains 'Run' and other fields.
        conn: SQLite connection object.
        cursor: SQLite cursor object.
    """
    run_value = metadata_dict['Run']
    
    # Check if the Run already exists in the Main_Run_Table
    cursor.execute("SELECT 1 FROM Main_Run_Table WHERE Run = ?", (run_value,))
    exists = cursor.fetchone()
    view_main_run_table(conn, cursor)
    # If the Run does not exist, insert the metadata into the Main_Run_Table
    if not exists:
        # print("The run is not in the big table.")
        # Insert the metadata into Main_Run_Table
        cursor.execute('''
            INSERT INTO Main_Run_Table (Age, Author, BSource, BType, Chain, Disease, Isotype, Link, Longitudinal, Run, Species, Subject, "Total sequences", "Unique sequences", Vaccine)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metadata_dict['Age'], metadata_dict['Author'], metadata_dict['BSource'], metadata_dict['BType'],
            metadata_dict['Chain'], metadata_dict['Disease'], metadata_dict['Isotype'], metadata_dict['Link'],
            metadata_dict['Longitudinal'], metadata_dict['Run'], metadata_dict['Species'], metadata_dict['Subject'],
            metadata_dict["Total sequences"], metadata_dict["Unique sequences"], metadata_dict['Vaccine']
        ))

        conn.commit()  # Commit after insert

# Function to store the dataframe as a child table with foreign key to Main_Run_Table
@measure_execution_time
def store_dataframe_as_table(df, table_name, conn, cursor, metadata_dict):
    # Ensure the dataframe contains the required columns
    required_columns = ['sequence_alignment_aa', 'germline_alignment_aa', 'v_call', 'd_call', 'j_call', 'ANARCI_status', 'Run']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"DataFrame must contain the following columns: {required_columns}")
    
    # Insert into Main_Run_Table if the 'Run' does not exist
    insert_into_main_table_if_not_exists(metadata_dict, conn, cursor)

    cursor.execute('PRAGMA foreign_keys = ON;')

    # Create child table with a foreign key reference to Main_Run_Table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            sequence_alignment_aa TEXT,
            germline_alignment_aa TEXT,
            v_call TEXT,
            d_call TEXT,
            j_call TEXT,
            ANARCI_status TEXT,
            Run TEXT,
            FOREIGN KEY(Run) REFERENCES Main_Run_Table(Run) ON DELETE CASCADE
        )
    ''')
    
    # Insert the data into the child table
    df.to_sql(table_name, conn, if_exists='append', index=False)

from selenium.webdriver.common.by import By
@measure_execution_time
def pass_attributes(name, value, driver):
    if value is not None:
        driver.find_element(By.NAME, name).send_keys(value)


from selenium import webdriver
@measure_execution_time
def web_search(args):
    # The URL of the search form (This URL is for example purposes, inspect the actual form action URL)
    search_url = 'https://opig.stats.ox.ac.uk/webapps/oas/oas_unpaired/'

    # Initialize the Selenium WebDriver (Firefox in this case)
    driver = webdriver.Firefox()

    # Step 1: Open the first page with the form
    driver.get(search_url)

    # Step 2: Fill in the form with the attribute values
    [pass_attributes(key,value,driver) for key, value in args['Metadata'].items()]

    # Step 3: Submit the form
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()

    # Step 4: Wait for the next page to load and find the link with the word "here"
    try:
        # Find the hyperlink with the exact text "here." and click it
        link = driver.find_element(By.LINK_TEXT, "here.")
        link.click()
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the browser
        driver.quit()

import glob
@measure_execution_time
def DownloadandRun():
    # Moving the downloaded file
    base_URL = "/Users/sabadaftari"
    download_folder = base_URL+"/Downloads"
    destination_folder = base_URL+"/Profluent"

    move_latest_file(download_folder, destination_folder)

    # run the shell script 
    shell_file = glob.glob(os.path.join(destination_folder, '*.sh'))
    run_shell_script(shell_file[0])
