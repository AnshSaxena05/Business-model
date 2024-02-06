from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
app = Flask(__name__)

df = pd.read_csv('result.csv')

def make_chart(selected_category):
    x = df[df['Category'] == selected_category]
    a = x['Original Company Loss'].values[0]
    b = x['Company Loss after prediction'].values[0]
    c = x['Company Revenue Gain'].values[0]

    plt.bar(x=['Before', 'After', 'Gain'], height=[a,b,c])
    plt.savefig('img.jpg')

@app.route('/', methods=['GET', 'POST'])
def home():
    categories = get_categories_from_csv('result.csv')
    selected_category = None
    category_details = None

    if request.method == 'POST':
        selected_category = request.form['category']
        category_details = get_category_details('result.csv', selected_category)
        make_chart(selected_category)
        return render_template('Home.html', categories=categories, selected_category=selected_category, category_details=category_details)
    
    
    return render_template('Home.html', categories=categories)

def get_categories_from_csv(file_path):
    df = pd.read_csv(file_path)
    categories = df['Category'].tolist() if 'Category' in df.columns else []
    return categories

def get_category_details(file_path, selected_category):
    df = pd.read_csv(file_path)
    selected_row = df[df['Category'] == selected_category].squeeze()
    category_details = selected_row.to_dict() if not selected_row.empty else None
    return category_details

if __name__ == '__main__':
    app.run(debug=True)
