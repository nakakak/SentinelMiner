import os
import sys
import glob
import numpy as np
import pandas as pd
from joblib import load
import traceback

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

 修正的全局路径
BASE_DIR = resource_path("al/dec3")
PRO_DIR = resource_path("pro")

def load_preprocessor():
    return load(os.path.join(PRO_DIR, 'preprocessor.joblib'))

def load_label_encoder():
    return load(os.path.join(PRO_DIR, 'label_encoder.joblib'))

def load_feature_selectors():
    feature_selectors = {}
    for name in ['pca_model', 'chi2_selector', 'rfe_selector', 'knn_pca']:
        path = os.path.join(PRO_DIR, f"{name}.joblib")
        if os.path.exists(path):
            feature_selectors[name.replace("_model", "").replace("_selector", "")] = load(path)
    return feature_selectors

def load_model(model_key):
    model_path = os.path.join(BASE_DIR, model_key, f"{model_key}_model.joblib")
    model = load(model_path)
    info = {'model_type': model_key, 'main': model}
    if model_key == 'KNN':
        knn_pca_path = os.path.join(PRO_DIR, 'knn_pca.joblib')
        if os.path.exists(knn_pca_path):
            info['pca'] = load(knn_pca_path)
    return info

def preprocess_data(df, preprocessor):
    X = df.copy()
    drop_cols = ['label', 'difficulty', 'attack_type', 'specific_class', 'category']
    for col in drop_cols:
        if col in X.columns:
            X = X.drop(columns=[col])
    cat_cols = X.select_dtypes(include=['object']).columns
    if len(cat_cols) > 0:
        X = pd.get_dummies(X, columns=cat_cols, drop_first=True)
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
    return preprocessor.transform(X)

def adjust_features(X_scaled, model_info, selectors):
    model = model_info['main']
    expected = getattr(model, 'n_features_in_', X_scaled.shape[1])
    if model_info['model_type'] == 'KNN' and 'pca' in model_info:
        X_scaled = model_info['pca'].transform(X_scaled)
    if expected != X_scaled.shape[1]:
        if 'pca' in selectors:
            X_scaled = selectors['pca'].transform(X_scaled)
        if X_scaled.shape[1] < expected:
            pad = np.random.randn(X_scaled.shape[0], expected - X_scaled.shape[1])
            X_scaled = np.hstack((X_scaled, pad))
        elif X_scaled.shape[1] > expected:
            X_scaled = X_scaled[:, :expected]
    return X_scaled

def predict_labels(X, model_info, label_encoder):
    preds = model_info['main'].predict(X)
    try:
        return label_encoder.inverse_transform(preds)
    except Exception:
        return preds

def full_predict(csv_path, model_key):
    try:
        df = pd.read_csv(csv_path)
        pre = load_preprocessor()
        le = load_label_encoder()
        selectors = load_feature_selectors()
        model_info = load_model(model_key)
        X = preprocess_data(df, pre)
        X = adjust_features(X, model_info, selectors)
        return predict_labels(X, model_info, le)
    except Exception as e:
        print(f"[预测失败]: {e}")
        print(traceback.format_exc())
        return None
