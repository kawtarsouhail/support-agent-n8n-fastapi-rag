# main.py
import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

load_dotenv()
app = FastAPI(title="RAG FAQ")
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")   # chargé une seule fois

class Requete(BaseModel):
    question: str
    top_k: int = 3

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/search")
def search(req: Requete):
    v = str(model.encode(req.question).tolist())
    sql = """
        SELECT question, reponse, 1 - (embedding <=> %s::vector) AS score
        FROM faq
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """
    with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
        rows = conn.execute(sql, (v, v, req.top_k)).fetchall()

    passages = [
        {"question": q, "reponse": r, "score": round(s, 3)}
        for q, r, s in rows
    ]
    return {
        "passages": passages,
        "meilleur_score": passages[0]["score"] if passages else 0.0,
    }
