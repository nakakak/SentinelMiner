import spacy
import en_core_web_sm
import pandas as pd
import re

 加载英文NER模型
nlp = en_core_web_sm.load()

 清洗文本函数
def clean_text(text):
    if pd.isna(text):
        return ""
    text = re.sub(r"[®©°™Ø]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

 提取时间+事件摘要
def extract_date_and_event(text):
    doc = nlp(text)
    date = None
    for ent in doc.ents:
        if ent.label_ == "DATE":
            date = ent.text
            break
    keywords = [token.text for token in doc if token.pos_ in ["VERB", "NOUN"]][:4]
    return date, " ".join(keywords)

 主处理函数
def extract_timeline_from_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "title" in df.columns:
        df["title"] = df["title"].apply(clean_text)
    if "content" in df.columns:
        df["content"] = df["content"].apply(clean_text)

    df = df[df["content"].str.strip().astype(bool)]
    df = df.reset_index(drop=True)

    timeline = []
    for _, row in df.iterrows():
        date, summary = extract_date_and_event(row["content"])
        if date and summary:
            timeline.append((date, summary))

    timeline_df = pd.DataFrame(timeline, columns=["date", "event"])
    timeline_df = timeline_df.sort_values("date")
    return timeline_df
