# Use this script to save EM-DAT data into the postgre database

import pandas as pd
from sqlalchemy import create_engine

# Database settings
DB_NAME = 'emdat_db'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Access the data through https://www.emdat.be/
# Replace the following path
file_path = 'Emdat_database.xlsx'

sheet_name='EM-DAT Data'

df = pd.read_excel(file_path, sheet_name=sheet_name)

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

df.to_sql("emdat", engine, if_exists='replace', index=False)

print(f"Successfully imported '{file_path}' to table emdat in database '{DB_NAME}'")
