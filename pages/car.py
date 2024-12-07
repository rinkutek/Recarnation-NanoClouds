import pandas as pd
import numpy as np
import seaborn as sns
sns.set()
from matplotlib import pyplot as plt
import os
from pathlib import Path

# Define the base directory to access files relative to the script's location
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the dataset
df = pd.read_csv(os.path.join(BASE_DIR,'pages/data.csv'))

# Standardize column names to lowercase and replace spaces with underscores
df.columns = df.columns.str.lower().str.replace(' ','_')

# Standardize string columns to lowercase and replace spaces with underscores
string_columns = list(df.dtypes[df.dtypes == 'object'].index)
for col in string_columns :
    df[col] = df[col].str.lower().str.replace(' ','_')

# Rename 'msrp' column to 'price' for better readability
df.rename(columns = {'msrp':'price'} ,inplace =True)

# Format floats to two decimal places for better display
pd.options.display.float_format = '{:,.2f}'.format

# Add a new column for the logarithm of price (to handle skewed price data)
df['log_price'] = np.log1p(df.price)

# Set random seed for reproducibility
np.random.seed(2)

# Split data into training, validation, and testing sets
n= len(df)
n_val  =  int(0.2 * n)
n_test =  int(0.2 * n)
n_train = n - (n_val + n_test)

# Shuffle the dataset to ensure randomness
idx = np.arange(n)
np.random.shuffle(idx)
df_shuffled = df.iloc[idx]

# Create training, validation, and testing datasets
df_train = df_shuffled.iloc[:n_train].copy()
df_val = df_shuffled.iloc[n_train:n_train+n_val].copy()
df_test = df_shuffled.iloc[n_train+n_val:].copy()

# Extract target variable (log of price) for each dataset
y_train = df_train.log_price.values
y_val = df_val.log_price.values
y_test = df_test.log_price.values

# Define the numerical features used for prediction
base = ['engine_hp','engine_cylinders', 'highway_mpg', 'city_mpg', 'popularity'] # we take the numerical only here 


def prepare_X(df):
    """
    Prepares the feature matrix X from the dataframe.
    - Adds derived features like age, categorical encodings, and one-hot encodings.
    - Fills missing values with the mean of each column.
    """
    df = df.copy()
    features = base.copy()
    
    # Standardize string columns
    string_columns = list(df.dtypes[df.dtypes == 'object'].index)
    for col in string_columns :
        df[col] = df[col].str.lower().str.replace(' ','_')
    
    # Add derived feature: Age of the car
    df['age']= 2024 - df.year
    features.append('age')
    
    # One-hot encoding for number of doors
    for v in [2,3,4] :
        feature = 'num_doors_%s' % v
        df[feature] = (df['number_of_doors'] == v).astype(int)
        features.append(feature)

    # One-hot encoding for car make    
    for v in ['chevrolet', 'ford', 'volkswagen', 'toyota', 'dodge','nissan','gmc','honda','mazda','cadillac']:
        feature = 'is_make_%s' % v
        df[feature] = (df['make'] == v).astype(int)
        features.append(feature)
    
    # One-hot encoding for engine fuel type  
    for v in ['regular_unleaded', 'premium_unleaded_(required)', 
              'premium_unleaded_(recommended)', 'flex-fuel_(unleaded/e85)','diesel','electric']:
        feature = 'is_type_%s' % v
        df[feature] = (df['engine_fuel_type'] == v).astype(int)
        features.append(feature) 
    
    # One-hot encoding for transmission type
    for v in ['automatic', 'manual', 'automated_manual']:
        feature = 'is_transmission_%s' % v
        df[feature] = (df['transmission_type'] == v).astype(int)
        features.append(feature)
    
    # One-hot encoding for driven wheels    
    for v in ['front_wheel_drive', 'rear_wheel_drive', 'all_wheel_drive', 'four_wheel_drive']:
        feature = 'is_driven_wheels_%s' % v
        df[feature] = (df['driven_wheels'] == v).astype(int)
        features.append(feature)
    
    # One-hot encoding for market category
    for v in ['crossover', 'flex_fuel', 'luxury', 'luxury,performance', 'hatchback','performance','crossover,luxury','luxury,high-performance','exotic,high-performance','hatchback,performance']:
        feature = 'is_mc_%s' % v
        df[feature] = (df['market_category'] == v).astype(int)
        features.append(feature)
    
    # One-hot encoding for vehicle size
    for v in ['compact', 'midsize', 'large']:
        feature = 'is_size_%s' % v
        df[feature] = (df['vehicle_size'] == v).astype(int)
        features.append(feature)
    
    # One-hot encoding for vehicle style
    for v in ['sedan', '4dr_suv', 'coupe', 'convertible', '4dr_hatchback','crew_cab_pickup','extended_cab_pickup','wagon','2dr_hatchback','passenger_minivan']:
        feature = 'is_style_%s' % v
        df[feature] = (df['vehicle_style'] == v).astype(int)
        features.append(feature)
    
    # One-hot encoding for specific car models
    for v in ['silverado_1500','tundra','f-150','sierra_1500','beetle_convertible','corvette','tacoma','gti','frontier','beetle','accord']:
        feature = 'is_model_%s' % v
        df[feature] = (df['model'] == v).astype(int)
        features.append(feature)
    
    # Select numerical features and fill missing values
    df_num = df[features]
    df_num = df_num.fillna(df_num.mean())
    
    # Convert the dataframe to a NumPy array
    X = df_num.values
    return X


# Function to train a regularized linear regression model
def train_linear_regression_reg(X, y, r=0.0):
    """
    Trains a linear regression model with L2 regularization.
    - Adds a bias term (ones) to the feature matrix.
    - Computes weights using the closed-form solution.
    """
    ones = np.ones(X.shape[0])
    X = np.column_stack([ones, X])

    XTX = X.T.dot(X)
    reg = r * np.eye(XTX.shape[0])
    XTX = XTX + reg

    XTX_inv = np.linalg.inv(XTX)
    w = XTX_inv.dot(X.T).dot(y)
    
    return w[0], w[1:]


# Function to calculate Root Mean Squared Error (RMSE)
def rmse(y,y_pred):
    error = y_pred - y
    mse = (error **2).mean()
    return np.sqrt(mse)

# Function to compute model weights
def w_calc ():
    """
    Prepares training data and trains the model.
    - Returns the bias term (w_0) and feature weights (w).
    """
    X_train = prepare_X(df_train)
    w_0, w = train_linear_regression_reg(X_train, y_train, r=0.01)
    return w_0 , w




#### Testing :
# X_train = prepare_X(df_train)
# w_0, w = train_linear_regression_reg(X_train, y_train, r=0.01)

# y_pred = w_0 + X_train.dot(w)
# print('train', rmse(y_train, y_pred))

# X_val = prepare_X(df_val)
# y_pred = w_0 + X_val.dot(w)
# print('val', rmse(y_val, y_pred))


####  Finaly ... using the model :

# this is a testing data it is in the form:
#{'city_mpg': 18,
#  'driven_wheels': 'all_wheel_drive',
#  'engine_cylinders': 6.0,
#  'engine_fuel_type': 'regular_unleaded',
#  'engine_hp': 268.0,
#  'highway_mpg': 25,
#  'log_price': 10.345638111452145,
#  'make': 'toyota',
#  'market_category': 'crossover,performance',
#  'model': 'venza',
#  'number_of_doors': 4.0,
#  'popularity': 2031,
#  'price': 31120,
#  'transmission_type': 'automatic',
#  'vehicle_size': 'midsize',
#  'vehicle_style': 'wagon',
#  'year': 2013}

# ad = df_test.iloc[8].to_dict()

# X_train = prepare_X(df_train)
# w_0, w = train_linear_regression_reg(X_train, y_train, r=0.01)

# X_test = prepare_X(pd.DataFrame([ad]))
# y_pred = w_0 + X_test.dot(w)
# suggestion = np.expm1(y_pred)[0].astype(int)

# print("Price is : " , ad['price'])
# print("The prediction is : " , suggestion ,'$')