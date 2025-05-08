
import os
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

# Base directory for locating data
BASE_DIR = Path(__file__).resolve().parent.parent

# Load dataset
df = pd.read_csv(os.path.join(BASE_DIR, 'pages/used_cars.csv'))

# Drop missing essentials
df = df.dropna(subset=['model_year', 'milage', 'price'])

# Clean and convert
df['milage'] = df['milage'].str.replace(' mi.', '', regex=False).str.replace(',', '').astype(int)
df['model_year'] = df['model_year'].astype(int)
df['price'] = df['price'].str.replace('$', '', regex=False).str.replace(',', '').astype(int)

# Feature: car age
df['age'] = 2024 - df['model_year']
# df['milage'] = df['milage'] / df['age'].replace(0, 1)  # avoid division by zero


# Define target and features
y = np.log1p(df['price'])
X = df[['brand', 'model', 'fuel_type', 'engine', 'transmission', 'ext_col', 'int_col', 'accident', 'clean_title', 'milage', 'age']]

# Column types
categorical_cols = X.select_dtypes(include='object').columns.tolist()
numerical_cols = X.select_dtypes(include='number').columns.tolist()

# Preprocessing
numeric_transformer = Pipeline([('imputer', SimpleImputer(strategy='mean'))])
categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numerical_cols),
    ('cat', categorical_transformer, categorical_cols)
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost pipeline
model = make_pipeline(
    preprocessor,
    XGBRegressor(n_estimators=800, max_depth=9, learning_rate=0.15, random_state=42)
    #XGBRegressor(n_estimators=800,max_depth=10,learning_rate=0.15,subsample=0.8,colsample_bytree=0.8,reg_lambda=1.0,reg_alpha=0.5,random_state=0)

)

# Train the 
print("Training model...")
model.fit(X_train, y_train)

# Evaluate (optional)
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)
print(f"RMSE: {rmse:.3f}")
print(f"R² Score: {r2:.3%}")
