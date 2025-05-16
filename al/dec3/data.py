import pandas as pd
import numpy as np
from joblib import load
import os

def preprocess_data(data, preprocessor=None, models_dir='pro', target_col='label'):
    """
    完整数据预处理逻辑（处理分类列、填充缺失、标准化）
    """
    if target_col in data.columns:
        X = data.drop(columns=[target_col])
    else:
        X = data.copy()

    # 分类列独热编码
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        print(f"⚡ 检测到分类列，进行独热编码: {categorical_cols}")
        X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

     缺失值处理
    X = X.fillna(X.mean())

    if preprocessor is None:
        preprocessor = load(os.path.join(models_dir, "preprocessor.joblib"))

    X_scaled = preprocessor.transform(X)
    return X_scaled

def adjust_features_for_model(X_scaled, model_info, feature_selectors=None, models_dir='pro'):
    """
    调整特征数量，适配模型输入
    """
    expected_features = getattr(model_info['main'], 'n_features_in_', X_scaled.shape[1])
    print(f"模型期望特征数: {expected_features}，当前: {X_scaled.shape[1]}")

    if X_scaled.shape[1] < expected_features:
        padding = np.zeros((X_scaled.shape[0], expected_features - X_scaled.shape[1]))
        X_scaled = np.hstack((X_scaled, padding))
    elif X_scaled.shape[1] > expected_features:
        X_scaled = X_scaled[:, :expected_features]

    return X_scaled

def load_and_preprocess_csv(csv_path, models_dir='pro', target_col='label'):
    """
    读取CSV并完成预处理
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"成功读取CSV: {csv_path}，shape: {df.shape}")
        X_scaled = preprocess_data(df, models_dir=models_dir, target_col=target_col)
        return df, X_scaled
    except Exception as e:
        print(f"加载或预处理CSV出错: {e}")
        import traceback
        print(traceback.format_exc())
        return None, None
