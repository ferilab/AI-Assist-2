
import os, sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(BASE_DIR, "backend"))
print("read embeddings from: ", os.path.join(BASE_DIR, "backend"))

from embeddings import init_db, store


init_db()


DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
for file in os.listdir(DATA_DIR):
    with open(os.path.join(DATA_DIR, file)) as f:
        store(f.read())