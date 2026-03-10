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

def zscore_mask_only(X_numpy):
    X_safe = X_numpy.astype(np.float64).copy()
    X_safe = np.nan_to_num(X_safe)
    z_scores = np.abs(stats.zscore(X_safe, axis=1))
    max_z = np.max(z_scores, axis=1)
    threshold = np.percentile(max_z, 95)
    keep_mask = max_z < threshold
    kept_pct = keep_mask.mean() * 100
    print(f"Threshold={threshold:.2f}")
    return keep_mask

def parsing_data(dir_path):
    data_list = []
    for dir_1 in os.listdir(dir_path):
        for dir_2 in os.listdir(f'{dir_path}/{dir_1}'):
            for dir_3 in os.listdir(f'{dir_path}/{dir_1}/{dir_2}'):
                print(f'{dir_3}')
                center, cells = None, None
                for i in dir_3.split('_'):
                    if 'center' in i:
                        center = i
                    if 'cortex' in i or 'striatum' in i or 'cerebellum' in i:
                        cells = i
                X_raw, wavenumbers = load_raman_mapping(f'{dir_path}/{dir_1}/{dir_2}/{dir_3}')
                metadata_df = pd.DataFrame({
                    'center': [center] * X_raw.shape[0],
                    'cells': [cells] * X_raw.shape[0], 
                    'cat': [dir_1] * X_raw.shape[0]
                })
                file_data = pd.concat([pd.DataFrame(X_raw), metadata_df], axis=1)
                data_list.append(file_data)
    return pd.concat(data_list, ignore_index=True)

data = parsing_data('data')
df = data

label_encoder_cat = LabelEncoder()
df['cat'] = label_encoder_cat.fit_transform(data['cat'])

ohe = OneHotEncoder(sparse_output=False, drop='first')
cat_encoded = ohe.fit_transform(df[['center', 'cells']])

df = pd.concat([df.drop(['center', 'cells'], axis=1), pd.DataFrame(cat_encoded, columns=['center', 'cell1', 'cell2'])], axis=1)

X, y = df.drop('cat', axis=1), df['cat']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X.drop(['center', 'cell1', 'cell2'], axis=1))

X_normalized = normalize(X_scaled, norm='l2')

pca = PCA(n_components=37)
X_pca = pca.fit_transform(X_normalized)

keep_mask = zscore_mask_only(X_pca)

X = pd.concat([pd.DataFrame(X_pca), X[['center', 'cell1', 'cell2']]], axis=1)

names_columns = [str(i) for i in range(X.shape[1] - 3)]
names_columns.extend(['center', 'cell1', 'cell2'])

X = pd.DataFrame(X.values, columns=names_columns)[keep_mask]
y = y[keep_mask]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print(f'Train: {X_train.shape[0]}')
print(f'Test:  {X_test.shape[0]}')

rf_model = RandomForestClassifier(
    n_estimators=4000,
    max_depth=16,
    min_samples_split=10,
    min_samples_leaf=5,
    random_state=42,
    max_features='sqrt',
    class_weight='balanced',
    n_jobs=-1,
    verbose=0
)

lgb_model = LGBMClassifier(
    n_estimators=4000,
    learning_rate=0.01,
    max_depth=12,
    num_leaves=100,
    subsample=0.9,
    colsample_bytree=0.9,
    reg_alpha=0.1,
    reg_lambda=0.1,
    random_state=42,
    class_weight='balanced',
    verbose=-1,
    n_jobs=-1,
    device='gpu'
)

xgb_model = xgb.XGBClassifier(
    n_estimators=4000,
    max_depth=12,
    learning_rate=0.01,
    subsample=0.9,
    colsample_bytree=0.9,
    reg_alpha=0.2,
    reg_lambda=1.0,
    min_child_weight=5,
    random_state=42,
    n_jobs=-1,
    tree_method='gpu_hist'
)

rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_proba = rf_model.predict_proba(X_test)

print(f"RF Accuracy: {accuracy_score(y_test, rf_pred):.3f}")
print(classification_report(y_test, rf_pred, target_names=['сontrol','endo','exo']))

lgb_model.fit(X_train, y_train)
lgb_pred = lgb_model.predict(X_test)
lgb_proba = lgb_model.predict_proba(X_test)

print(f"LGB Accuracy: {accuracy_score(y_test, lgb_pred):.3f}")
print(classification_report(y_test, lgb_pred, target_names=['сontrol','endo','exo']))

xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)
xgb_proba = xgb_model.predict_proba(X_test)

print(f"XGB Accuracy: {accuracy_score(y_test, xgb_pred):.3f}")
print(classification_report(y_test, xgb_pred, target_names=['сontrol','endo','exo']))

joblib.dump(rf_model, 'models/rf_model.joblib')
joblib.dump(lgb_model, 'models/lgb_model.joblib')
joblib.dump(xgb_model, 'models/xgb_model.joblib')
