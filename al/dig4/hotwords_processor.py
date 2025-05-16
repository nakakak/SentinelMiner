import os
import pandas as pd
import re
from collections import Counter
import spacy
import en_core_web_sm   ✅ 直接导入模型模块

 ✅ 直接使用加载好的模型
nlp = en_core_web_sm.load()

def extract_hotwords_from_dataframe(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    对传入的新闻 DataFrame 执行清洗、分词、去停用词、热词统计。
    返回前 top_n 个词频的词汇及其计数。
    """
     删除无用列（如果存在）
    df = df.drop(columns=[
        "Unnamed: 3", "Unnamed: 4", "Unnamed: 5", "Unnamed: 6",
        "Unnamed: 7", "Unnamed: 8", "Unnamed: 9",
        "Unnamed: 10", "Unnamed: 11", "Unnamed: 12", "url"
    ], errors="ignore")

     清洗函数
    def clean_text(text):
        if pd.isna(text):
            return ""
        text = re.sub(r"[®©°™Ø]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

     应用清洗
    df["content"] = df["content"].apply(clean_text)

     删除空内容
    df = df[df["content"].str.strip().astype(bool)]

     重置索引
    df = df.reset_index(drop=True)
    df = df.head(10)

     分词 + 去停用词 + 只保留纯字母词
    all_text = " ".join(df["content"].dropna())
    doc = nlp(all_text.lower())
    tokens = [token.text for token in doc if token.is_alpha and not token.is_stop]

     统计词频
    word_freq = Counter(tokens)
    return pd.DataFrame(word_freq.most_common(top_n), columns=["word", "count"])
