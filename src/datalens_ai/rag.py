from __future__ import annotations
from pathlib import Path
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LocalRAG:
    def __init__(self, knowledge_dir: str | Path):
        self.path = Path(knowledge_dir)
        self.docs=[]
        for p in sorted(self.path.glob("*.md")):
            text=p.read_text(encoding="utf-8")
            self.docs.append((p.name, text))
        self.vectorizer=TfidfVectorizer(stop_words="english") if self.docs else None
        self.matrix=self.vectorizer.fit_transform([d[1] for d in self.docs]) if self.docs else None

    def retrieve(self, query: str, k: int=3) -> list[dict]:
        if not self.docs:
            return []
        q=self.vectorizer.transform([query])
        scores=cosine_similarity(q,self.matrix)[0]
        idx=scores.argsort()[::-1][:k]
        return [{"source":self.docs[i][0],"score":float(scores[i]),"text":self.docs[i][1]} for i in idx if scores[i] > 0]
