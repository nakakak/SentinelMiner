import os
import sys
import numpy as np
import pandas as pd
from joblib import load

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def preprocess_data(data, models_dir='pro', target_col=None):
    if target_col and target_col in data.columns:
        X = data.drop(target_col, axis=1)
    else:
        X = data.copy()

    for col in ['difficulty', 'attack_type', 'specific_class', 'category']:
        if col in X.columns:
            X.drop(columns=[col], inplace=True)

    categorical = X.select_dtypes(include=['object']).columns
    if len(categorical) > 0:
        X_cat = pd.get_dummies(X[categorical], drop_first=True)
        X_num = X.select_dtypes(exclude=['object']).fillna(0)
        X_processed = pd.concat([X_num, X_cat], axis=1)
    else:
        X_processed = X.fillna(0)

    preprocessor_path = resource_path(os.path.join(models_dir, 'preprocessor.joblib'))
    preprocessor = load(preprocessor_path)
    return preprocessor.transform(X_processed)

def adjust_features_for_model(X_scaled, model_info, feature_selectors=None, models_dir='pro'):
    model_type = model_info['model_type']
    model = model_info['main']

    if feature_selectors is None:
        feature_selectors = {}
        for name in ['pca_model', 'chi2_selector', 'rfe_selector']:
            path = resource_path(os.path.join(models_dir, f'{name}.joblib'))
            if os.path.exists(path):
                feature_selectors[name.split('_')[0]] = load(path)

    expected_features = getattr(model, 'n_features_in_', None)

    if model_type == 'KNN' and 'pca' not in feature_selectors and 'pca' not in model_info:
        knn_pca_path = resource_path(os.path.join(models_dir, 'knn_pca.joblib'))
        if os.path.exists(knn_pca_path):
            model_info['pca'] = load(knn_pca_path)

    if model_type == 'KNN' and 'pca' in model_info:
        return model_info['pca'].transform(X_scaled)

    if expected_features and X_scaled.shape[1] != expected_features:
        for key in ['pca', 'chi2', 'rfe']:
            if key in feature_selectors:
                X_scaled = feature_selectors[key].transform(X_scaled)
                break

        if X_scaled.shape[1] < expected_features:
            pad = np.zeros((X_scaled.shape[0], expected_features - X_scaled.shape[1]))
            X_scaled = np.hstack((X_scaled, pad))
        elif X_scaled.shape[1] > expected_features:
            X_scaled = X_scaled[:, :expected_features]

    return X_scaled

def load_label_encoder(models_dir='pro'):
    path = resource_path(os.path.join(models_dir, 'label_encoder.joblib'))
    return load(path)
