import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
pd.set_option('display.max_rows', None)
df=pd.read_csv("transformed_data.csv")

"""
The below code is used to remove the extra rows of data for each category.This done by
Calculatig the overall review count for each category and eleminate the row which contains < 1% of total review count for
that category.
"""
category_sum = df.groupby('category')['rating_count'].sum()

def filter_by_1percent(row):
    category = row['category']
    count = row['rating_count']
    category_total = category_sum[category]
    return count >= 0.01 * category_total

df_filtered = df[df.apply(filter_by_1percent, axis=1)]

unique_categories = df_filtered['category'].unique()
"""
Lists to store company loss, min_discount, max_rating, original_company_loss, and company_revenue_gain for each category
Then runs the model to predict these values and store each value in respective dataframe.
Then combine all the dataframes into 1 dataframe.
Meanwhile create a pickle file for model as well.
"""
company_loss_per_category = []
min_discount_per_category = []
max_rating_per_category = []
original_company_loss_per_category = []
company_revenue_gain_per_category = []

model = RandomForestRegressor(random_state=42)

for category in unique_categories:
    # Filter data for the current category
    category_data = df_filtered[df_filtered['category'] == category]
    
    if len(category_data) < 2:
        
        initial_discount = category_data['discount_percentage'].iloc[0]
        category_c_loss = ((category_data['actual_price'] - category_data['discounted_price']) * (initial_discount)).sum()
        company_loss_per_category.append({'Category': category, 'Company Loss after prediction': category_c_loss})
        min_discount_per_category.append({'Category': category, 'Min Discount for Max Rating': initial_discount})
        max_rating_per_category.append({'Category': category, 'Max Rating': category_data['rating'].max()})
        original_company_loss_per_category.append({'Category': category, 'Original Company Loss': category_c_loss})
        company_revenue_gain_per_category.append({'Category': category, 'Company Revenue Gain': 0})
        # No gain for single data point
        continue
    
    X = category_data[['discounted_price', 'actual_price', 'rating', 'rating_count']]
    y = category_data['discount_percentage']
    
    # model = RandomForestRegressor(random_state=42)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model.fit(X_train, y_train)
    
    predictions = model.predict(X)
    
    min_discount = min(predictions)
    
    category_c_loss = ((category_data['actual_price'] - category_data['discounted_price']) * (min_discount)).sum()
    
    # Store company loss, min_discount, and max_rating for the category
    company_loss_per_category.append({'Category': category, 'Company Loss after prediction': category_c_loss})
    min_discount_per_category.append({'Category': category, 'Min Discount for Max Rating': min_discount})
    max_rating_per_category.append({'Category': category, 'Max Rating': category_data['rating'].max()})
    
    # Calculate original company loss using the original discount
    original_c_loss = ((category_data['actual_price'] - category_data['discounted_price']) * (category_data['discount_percentage'])).sum()
    original_company_loss_per_category.append({'Category': category, 'Original Company Loss': original_c_loss})
    
    # Calculate company revenue gain by subtracting Original Company Loss from Company Loss
    revenue_gain = original_c_loss - category_c_loss
    company_revenue_gain_per_category.append({'Category': category, 'Company Revenue Gain': revenue_gain})

with open("model.pkl",'wb') as file:
    pickle.dump(model,file=file)

company_loss_df = pd.DataFrame(company_loss_per_category)
min_discount_df = pd.DataFrame(min_discount_per_category)
max_rating_df = pd.DataFrame(max_rating_per_category)
original_company_loss_df = pd.DataFrame(original_company_loss_per_category)
company_revenue_gain_df = pd.DataFrame(company_revenue_gain_per_category)

result_df = pd.merge(company_loss_df, min_discount_df, on='Category')
result_df = pd.merge(result_df, max_rating_df, on='Category')
result_df = pd.merge(result_df, original_company_loss_df, on='Category')
result_df = pd.merge(result_df, company_revenue_gain_df, on='Category')

result_df.to_csv("result.csv", index=False)

