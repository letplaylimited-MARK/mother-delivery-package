import re
from collections import Counter

TFIDF_WEIGHTS = {"開發": 0.8, "系統": 0.6, "醫療": 0.9, "合規": 0.85, "審查": 0.7,
                 "設計": 0.6, "分析": 0.7, "測試": 0.5, "部署": 0.6, "優化": 0.7}

def extract_tfidf_keywords(text, vocab_size=100):
    words = re.findall(r'[\w]+', text)
    counter = Counter(words)
    total = sum(counter.values())
    keywords = {}
    for word, count in counter.most_common(min(vocab_size, len(counter))):
        tf = count / total if total > 0 else 0
        idf = TFIDF_WEIGHTS.get(word, 0.3)
        keywords[word] = round(tf * idf, 4)
    return keywords

def ensemble_score(f1=0, f2=0, f3=0, f4=0, f5=0, f6=0):
    w = [0.25, 0.30, 0.20, 0.10, 0.10, 0.05]
    return w[0]*f1 + w[1]*f2 + w[2]*f3 + w[3]*f4 + w[4]*f5 + w[5]*f6
