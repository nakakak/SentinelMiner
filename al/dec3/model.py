import os
from joblib import load


def load_model(model_name, models_dir='al/dec3'):
    model_path = os.path.join(models_dir, model_name, f"{model_name}_model.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"模型文件不存在: {model_path}")

    print(f"加载模型: {model_path}")
    model = load(model_path)
    return {'model_type': model_name, 'main': model}


def load_label_encoder(models_dir='pro'):
    path = os.path.join(models_dir, "label_encoder.joblib")
    if os.path.exists(path):
        return load(path)
    else:
        raise FileNotFoundError(f"标签编码器文件不存在: {path}")
