import spacy
import en_core_web_sm
import re
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

 加载英文 spaCy 模型（稳定兼容开发和打包）
nlp = en_core_web_sm.load()

def preprocess_text(text):
    """清洗文本，去除特殊符号和多余空格"""
    text = re.sub(r"[®©°™Ø]", "", str(text))
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def get_spacy_embeddings(texts):
    """将文本转换为 spaCy 向量表示（doc.vector）"""
    return [nlp(text).vector for text in texts]

def cluster_with_spacy(df: pd.DataFrame, n_clusters: int = 5) -> pd.DataFrame:
    """使用 spaCy 向量进行聚类"""
    texts = (df["title"] + " " + df["content"]).apply(preprocess_text)
    embeddings = get_spacy_embeddings(texts)
    model = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = model.fit_predict(embeddings)
    return df

def cluster_with_tfidf(df: pd.DataFrame, n_clusters: int = 5, top_n: int = 5):
    """使用 TF-IDF 特征聚类"""
    texts = (df["title"] + " " + df["content"]).apply(preprocess_text)
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)

    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(tfidf_matrix)
    df["cluster"] = labels

    feature_names = vectorizer.get_feature_names_out()
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]

    cluster_keywords = {}
    cluster_articles = {}

    for i in range(n_clusters):
        cluster_keywords[i] = [feature_names[ind] for ind in order_centroids[i, :top_n]]
        cluster_articles[i] = df[df["cluster"] == i]["title"].tolist()

    return cluster_keywords, cluster_articles, df
