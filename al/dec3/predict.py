from al.dec3.model import load_model, load_label_encoder
from al.dec3.data import load_and_preprocess_csv, adjust_features_for_model

def predict_by_csv(csv_path, model_name, models_dir='al/dec3', pre_dir='pro'):
    """
    用指定模型进行CSV预测
    """
    df, X_scaled = load_and_preprocess_csv(csv_path, models_dir=pre_dir)
    if df is None or X_scaled is None:
        return None

    model_info = load_model(model_name, models_dir)
    X_ready = adjust_features_for_model(X_scaled, model_info, models_dir=pre_dir)

    model = model_info['main']
    predictions = model.predict(X_ready)

    encoder = load_label_encoder(models_dir=pre_dir)
    labels = encoder.inverse_transform(predictions)

    return labels
