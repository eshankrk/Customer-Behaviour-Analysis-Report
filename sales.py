import pandas as pd
df = pd.read_csv('customer_shopping_behavior.csv')

dfh = df.head()
dfi = df.info()
dfd = df.describe(include = 'all')

imp_rev_rate = df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x:  x.fillna(x.median()))
dfns = df.isnull().sum()

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')

df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})

labels = ['Young Adult','Adult','Middle Aged','Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly':30,
    'Quarterly' : 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months':90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)

 
(df['discount_applied'] == df['promo_code_used']).all()
df = df.drop('promo_code_used', axis=1)


import urllib
from sqlalchemy import create_engine

# 1. Define your SQL Server connection details
# 'localhost' targets your local computer where SQL Server is running
SERVER_NAME = 'localhost'  
DATABASE_NAME = 'customer_shopping_behaviour' 

# 2. Create the connection string for Windows Authentication
connection_string = (
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={SERVER_NAME};'
    f'DATABASE={DATABASE_NAME};'
    f'Trusted_Connection=yes;'
)

# 3. Build the engine and upload the data
params = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# This line pushes your 'df' dataframe into SQL Server as a table named 'customer_data'
df.to_sql('customer_data', engine, if_exists='replace', index=False)

print("Data successfully loaded into SQL Server!")