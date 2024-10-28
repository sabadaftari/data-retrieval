import pandas as pd
import os
import glob
import sqlite3
import polars as pl
import json
from utils import ( 
                    store_dataframe_as_table, 
                   )

def make_db(args):
    # Get all .csv.gz files in the source folder
    gz_files = glob.glob(os.path.join('', '*.csv.gz'))


    # Connect to SQLite database (or create one if it doesn't exist)
    conn = sqlite3.connect('multi_run_data.db')
    cursor = conn.cursor()

    # Create the Main_Run_Table (parent table) which holds unique Run metadata values
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Main_Run_Table (
            Age TEXT, -- Categorical value
            Author TEXT,
            BSource TEXT, -- Categorical value
            BType TEXT, -- Categorical value
            Chain TEXT, -- Categorical value
            Disease TEXT, -- Categorical value
            Isotype TEXT, -- Categorical value
            Link TEXT, 
            Longitudinal TEXT, -- Categorical value
            Run TEXT PRIMARY KEY,
            Species TEXT, -- Categorical value
            Subject TEXT, -- Categorical value
            "Total sequences" INTEGER,
            "Unique sequences" INTEGER,
            Vaccine TEXT -- Categorical value
        )
    ''')

    # Initialize empty Polars dataframe to store the metadata (Main_Run_Table)
    Metadata_df = pl.DataFrame()
    flag = 0
    import gzip
    # Iterate over each file and process
    for csv_file_path in gz_files:
        # Step 1: Read the CSV file without a header, using the args["Pre-entry"] columns
        try:
            df_no_header = pd.read_csv(csv_file_path, skiprows=1)[args["Pre-entry"]]
        except EOFError:
            # Open the gzipped file using gzip
            print(f"The file {csv_file_path} has not fully downloaded.")

        df_header = pd.read_csv(csv_file_path)[:0]

        # Extract metadata from the first row as a JSON string
        data_str = df_header.columns.values[0]
        data_dict = json.loads(data_str)

        """
        Assuming the "Run" is a unique value, 
        We will build the querying system based on its value.

        Do all the process you want to do here
        """

        # Insert the 'Run' value into the dataframe
        df_no_header['Run'] = data_dict['Run']

        # Update the Metadata_df with the current metadata (Main_Run_Table)
        if flag == 0:
            Metadata_df = pl.DataFrame(data_dict)
            Metadata_df = Metadata_df.select(sorted(Metadata_df.columns))
            flag += 1
        else:
            temp_df = pl.DataFrame(data_dict)
            temp_df = temp_df.select(sorted(temp_df.columns))
            Metadata_df = pl.concat([Metadata_df, temp_df], how='vertical')

        # Store the CSV file's data into its own table, linking to Main_Run_Table via Run foreign key
        table_name = f'DataTable_{data_dict["Run"]}'  # Unique table name for each file
        store_dataframe_as_table(df_no_header, table_name, conn, cursor, data_dict)

        print(f"Processing of file {csv_file_path} finished.")

    # Store the metadata in the Main_Run_Table (parent table)
    Metadata_df.to_pandas().to_sql('Main_Run_Table', conn, if_exists='replace', index=False)

    # Commit and close the connection
    conn.commit()
    conn.close()

   
