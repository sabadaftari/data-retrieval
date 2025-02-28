# OAS database retrieval
OAS Database Retrieval is a Python project designed to fetch, process, and store antibody sequence data from the Observed Antibody Space (OAS) database. OAS is a comprehensive repository containing over one billion annotated sequences from more than 80 studies, covering diverse immune states, species, and individuals.

## File Structure

* **main.py:** Main entry point for the project (if applicable).
* **make_db.py:** Contains functions to process CSV files, extract metadata, and build the SQLite database.
* **my_params.yaml:** YAML configuration file defining metadata parameters and pre-entry columns.
* **parsing.py:** Utilities for parsing CSV and JSON data.
* **query.py:** Functions for querying the SQLite database.
* **utils.py:** Utility functions for data storage, file handling, and database operations.
* **requirement.txt:** Lists required Python packages.

## Usage
1. **Install Dependencies**
   ```bash
    pip install -r requirements.txt
2. **Build the Database**
   ```bash
    python main.py

3. **Query**
   ```bash
    python query.py


