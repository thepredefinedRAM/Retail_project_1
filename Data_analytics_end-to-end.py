import pandas as pd
df=pd.read_csv(r"C:\Users\LENOVO\Downloads\customer_shopping_behavior.csv")
print(df.head())
df.info()
print(df.describe(include='all'))
print(df.isnull().sum())
#dealibg with cat based median for null ratings
df['Review Rating']= df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
print(df.isnull().sum())

#now we have to convert all the col names into lower case with underscore for easy use.
df.columns= df.columns.str.lower()
#df.columns=df.columns.str.replace('  ','_')
df.columns

# create a new column age_group
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)
df[['age','age_group']].head(10)


# create new column purchase_frequency_days

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency of purchases'].map(frequency_mapping)
df[['purchase_frequency_days','frequency of purchases']].head(10)

df[['discount applied','promo code used']].head(10)

df = df.drop('promo code used', axis=1)
df.columns

from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = "root"
host = "localhost"
port = "3306"
database = "customer_behavior"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Write DataFrame to MySQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
pd.read_sql("SELECT * FROM customer LIMIT 5;", engine)