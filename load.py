import pandas as pd
from sqlalchemy import create_engine

# Define the PostgreSQL connection parameters
db_params = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database',
    'port': 'your_port',
}
engine = create_engine(f'postgresql+psycopg2://{db_params["user"]}:{db_params["password"]}@{db_params["host"]}:{db_params["port"]}/{db_params["database"]}')

csv_file_path = 'path/to/transformed_data.csv'

csv_df = pd.read_csv(csv_file_path)

target_table = 'your_target_table'

# Write the DataFrame to the PostgreSQL database
csv_df.to_sql(target_table, engine, index=False, if_exists='replace')

print(f'Data from {csv_file_path} successfully loaded into {target_table} in PostgreSQL.')
