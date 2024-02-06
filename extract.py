import pandas as pd
from sqlalchemy import create_engine

def load_to_postgresql():
    
    transformed_data = pd.read_csv('path/to/transformed_data.csv')

    # Load data into PostgreSQL
    postgresql_connection_string = "postgresql://username:password@localhost:5432/your_postgresql_database"
    postgresql_engine = create_engine(postgresql_connection_string)
    transformed_data.to_sql('numeric_table_transformed', postgresql_engine, index=False, if_exists='replace')

load_to_postgresql()
