
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.config import EMBED_MODEL, DB_PATH
import os, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

model = SentenceTransformer(EMBED_MODEL)


def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS vectors (
        id INTEGER PRIMARY KEY,
        text TEXT,
        embedding BLOB
        )
    """)
    conn.commit()
    conn.close()


def embed(text: str):
    return model.encode(text)

def store(text: str):
    emb = embed(text).astype(np.float32).tobytes()
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO vectors (text, embedding) VALUES (?, ?)", (text, emb))
    conn.commit()
    conn.close()

def search(query: str, k=4):
    q_emb = embed(query)
    conn = connect()
    c = conn.cursor()
    rows = c.execute("SELECT text, embedding FROM vectors").fetchall()
    scored = []
    for text, emb in rows:
        emb = np.frombuffer(emb, dtype=np.float32)
        score = np.dot(q_emb, emb) / (np.linalg.norm(q_emb) * np.linalg.norm(emb))
        scored.append((score, text))
    conn.close()
    return [t for _, t in sorted(scored, reverse=True)[:k]]