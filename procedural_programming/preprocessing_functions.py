import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

import joblib


# Individual pre-processing and training functions
# ================================================

def load_data(df_path):
    # Function loads data for training
    return pd.read_csv(df_path)



def divide_train_test(df, target):
    # Function divides data set in train and test
    return train_test_split(df.drop(target, axis=1), df[target], test_size=0.2, random_state=0)
    


def extract_cabin_letter(df, var):
    # captures the first letter
    return df[var].str[0] 



def add_missing_indicator(df, var):
    # function adds a binary missing value indicator
    df[var+'_NA'] = np.where(df[var].isnull(), 1, 0)
    return df


    
def impute_na(df, var, replacement="Missing"):
    # function replaces NA by value entered by user
    # or by string Missing (default behaviour)
    return df[var].fillna(replacement)



def remove_rare_labels(df, var, frequent_labels):
    # groups labels that are not in the frequent list into the umbrella
    # group Rare
    return np.where(df[var].isin(frequent_labels), df[var], 'Rare')



def encode_categorical(df, var):
    # adds ohe variables and removes original categorical variable
    return pd.concat([df.drop(var, axis=1), pd.get_dummies(df[var], prefix=var, drop_first=True)], axis=1)



def check_dummy_variables(df, dummy_list):
    # check that all missing variables where added when encoding, otherwise
    # add the ones that are missing
    for var in dummy_list:
        if var not in df:
            df[var] = 0
    return df
    

def train_scaler(df, output_path):
    # train and save scaler
    scaler = StandardScaler()
    scaler.fit(df)
    joblib.dump(scaler, output_path)
    return scaler
  
    

def scale_features(df, scaler):
    # load scaler and transform data
    scaler = joblib.load(scaler) # with joblib probably
    return scaler.transform(df)



def train_model(df, target, output_path):
    # train and save model
    # initialise the model
    lin_model = LogisticRegression(C=0.0005, random_state=0)
    
    # train the model
    lin_model.fit(df, target)
    
    # save the model
    joblib.dump(lin_model, output_path)
    
    return None



def predict(df, model):
    # load model and get predictions
    model = joblib.load(model)
    return model.predict(df)

