import pandas as pd
from pymongo import MongoClient
import mysql.connector
from sqlalchemy import create_engine

def etl_process():
    use_database_q = """
                     USE sales_predict_n;
                     """
                  
    select_q = """
               SELECT SNO, discounted_price, actual_price, discount_percentage, rating, rating_count FROM numeric_table
               """
    
    mysql_connection =mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bravo@5103#"
    )
    mysql_coursor=mysql_connection.cursor()
    mysql_coursor.execute(use_database_q)
    mysql_coursor.execute(select_q)
    
    result_set = mysql_coursor.fetchall()

    columns = ["SNO", "discounted_price", "actual_price", "discount_percentage", "rating", "rating_count"]
    mysql_df = pd.DataFrame(result_set, columns=columns)


    # Extract from MongoDB
    mongo_client = MongoClient('mongodb://localhost:27017/')
    mongo_db = mongo_client['textdataset']
    mongo_collection = mongo_db['text']
    mongo_cursor = mongo_collection.find({}, {'SNO': 1,'product_id': 1, 'product_name': 1, 'category': 1, 'about_product': 1,
                                              'user_id': 1, 'user_name': 1, 'review_id': 1, 'review_title': 1,
                                              'review_content': 1, 'img_link': 1, 'product_link': 1})
    mongo_df = pd.DataFrame(list(mongo_cursor))
    
    mysql_df['discounted_price'] = mysql_df['discounted_price'].replace('[\₹,]', '', regex=True).astype(float)
    mysql_df['actual_price'] = mysql_df['actual_price'].replace('[\₹,]', '', regex=True).astype(float)
    mysql_df['rating'] = pd.to_numeric(mysql_df['rating'], errors='coerce').fillna(0.0).astype(float)
    mysql_df['discount_percentage'] = mysql_df['discount_percentage'].astype(float)
    mysql_df['rating_count'] = mysql_df['rating_count'].astype(str).str.replace(',', '').astype(float)

    print(mysql_df.info())
    print(mongo_df.info())
    
    # Merge dataframes if there is a common column
    merged_df = pd.merge(mysql_df, mongo_df, how='inner', left_on='SNO', right_on='SNO')

    # Additional transformation steps can be added here

    # Save the transformed data to a CSV file
    merged_df.to_csv('transformed_data.csv', index=False)
    

# Run the ETL process
etl_process()
