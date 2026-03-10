import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.preprocessing import normalize, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression
import joblib

def load_raman_mapping(file_path):
    df = pd.read_csv(file_path, sep='\s+', header=0)
    df.columns = ['X', 'Y', 'Wave', 'Intensity']
    spectra = df.pivot_table(
        index=['X', 'Y'], 
        columns='Wave', 
        values='Intensity'
    )
    X_raw = spectra.values
    wavenumbers = spectra.columns.values
    return X_raw, wavenumbers

def parsing_data_pred(dir_path):
    '''dir_path путь до папки с данными без других подпапок внутри!'''
    data_list = []
    for dir_1 in os.listdir(f'{dir_path}'):
        print(f'{dir_1}')
        center, cells = None, None
        for i in dir_1.split('_'):
            if 'center' in i:
                center = i
            if 'cortex' in i or 'striatum' in i or 'cerebellum' in i:
                cells = i
        X_raw, wavenumbers = load_raman_mapping(f'{dir_path}/{dir_1}')
        metadata_df = pd.DataFrame({
            'center': [center] * X_raw.shape[0],
            'cells': [cells] * X_raw.shape[0]
        })
        file_data = pd.concat([pd.DataFrame(X_raw), metadata_df], axis=1)
        data_list.append(file_data)
    return pd.concat(data_list, ignore_index=True)

data_pred = parsing_data_pred('data_pred')
df = data_pred

ohe = OneHotEncoder(sparse_output=False, drop='first')
cat_encoded = ohe.fit_transform(df[['center', 'cells']])

df = pd.concat([df.drop(['center', 'cells'], axis=1), pd.DataFrame(cat_encoded, columns=['center', 'cell1', 'cell2'])], axis=1)

X = df

scaler = joblib.load('models/scaler.joblib')
X_scaled = scaler.transform(X.drop(['center', 'cell1', 'cell2'], axis=1))

X_normalized = normalize(X_scaled, norm='l2')

pca = joblib.load('models/pca.joblib')
X_pca = pca.transform(X_normalized)

X = pd.concat([pd.DataFrame(X_pca), X[['center', 'cell1', 'cell2']]], axis=1)

names_columns = [str(i) for i in range(X.shape[1] - 3)]
names_columns.extend(['center', 'cell1', 'cell2'])

X = pd.DataFrame(X.values, columns=names_columns)

rf_loaded = joblib.load('models/rf_model.joblib')
lgb_loaded = joblib.load('models/lgb_model.joblib')
xgb_loaded = joblib.load('models/xgb_model.joblib')

stacking = StackingClassifier([
    ('rf', rf_loaded),
    ('lgb', lgb_loaded),
    ('xgb', xgb_loaded)
], final_estimator=LogisticRegression(random_state=42), cv=2, n_jobs=-1)

stack_pred = stacking.predict(X)

pd.DataFrame(stack_pred).to_csv('predict.csv')
