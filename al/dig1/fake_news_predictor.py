import os
import sys
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.sparse import hstack, csr_matrix

def resource_path(relative_path):
    """资源路径处理（兼容打包后的exe和开发环境）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

 模型与工具路径（打包后也能找）
MODEL_PATH = resource_path("al/dig1/fake_news_classifier.pkl")
TFIDF_TWEET_PATH = resource_path("al/dig1/tfidf_tweet_vectorizer.pkl")
TFIDF_STATEMENT_PATH = resource_path("al/dig1/tfidf_statement_vectorizer.pkl")
SCALER_PATH = resource_path("al/dig1/scaler.pkl")

def predict_fake_news(df: pd.DataFrame) -> pd.DataFrame:
    """对输入 DataFrame 执行假新闻检测预测"""
     加载模型和工具
    model = joblib.load(MODEL_PATH)
    tfidf_tweet = joblib.load(TFIDF_TWEET_PATH)
    tfidf_statement = joblib.load(TFIDF_STATEMENT_PATH)
    scaler = joblib.load(SCALER_PATH)

     填补缺失值并转换为字符串
    df["clean_tweet"] = df["clean_tweet"].fillna("").astype(str)
    df["statement"] = df["statement"].fillna("").astype(str)

     文本特征
    X_tweet = tfidf_tweet.transform(df["clean_tweet"])
    X_statement = tfidf_statement.transform(df["statement"])

     数值特征
    num_cols = [
        'followers_count', 'friends_count', 'favourites_count', 'statuses_count',
        'listed_count', 'cred', 'normalize_influence', 'BotScore',
        'capitals', 'digits', 'exclamation', 'questions',
        'Word count', 'Average word length', 'long_word_freq', 'short_word_freq'
    ]
    X_num = scaler.transform(df[num_cols])

     拼接所有特征
    X = hstack([X_tweet, X_statement, csr_matrix(X_num)])

     预测
    y_pred = model.predict(X)

     拼接预测结果
    df_result = df.copy()
    df_result["prediction"] = y_pred
    df_result["prediction_label"] = df_result["prediction"].apply(lambda x: "True" if x == 1 else "Fake")

    return df_result[["clean_tweet", "statement", "prediction_label"]]
