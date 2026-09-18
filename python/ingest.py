# ingest.py
import os

import psycopg
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
# faq.md au format :  ## question\n réponse...
with open("faq.md", encoding="utf-8") as f:
    texte = f.read()
blocs = [b.strip() for b in texte.split("## ") if b.strip()]

with psycopg.connect(os.environ["DATABASE_URL"]) as conn:
    with conn.cursor() as cur:
        cur.execute("TRUNCATE faq RESTART IDENTITY;")
        for bloc in blocs:
            question, _, reponse = bloc.partition("\n")
            contenu = question.strip()
            vecteur = model.encode(contenu).tolist()
            cur.execute(
                "INSERT INTO faq (question, reponse, contenu, embedding)"
                " VALUES (%s, %s, %s, %s)",
                (question.strip(), reponse.strip(), contenu, str(vecteur)),
            )
    conn.commit()
print(f"{len(blocs)} chunks indexés")
