# save_all_via_model.py
import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from model import ContainerData

def main():
    # 1) Načti .env a ověř MONGO_URI
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    print("MONGO_URI načteno:", bool(uri))  # DEBUG výpis
    if not uri:
        raise RuntimeError("❌ Chybí MONGO_URI v .env (soubor musí být v kořeni projektu).")

    # 2) Připojení k MongoDB
    client = MongoClient(uri)
    db = client["parsing"]
    col = db["containers"]
    print("Cíl → DB=parsing, Collection=containers")  # DEBUG

    # 3) Načti vstupní JSON (a ukaž current working dir pro jistotu)
    print("Working dir:", os.getcwd())  # DEBUG
    with open("data.json", "r", encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, list):
        raise RuntimeError("❌ Očekávám, že data.json obsahuje seznam (list) kontejnerů.")

    print("Načteno záznamů z JSONu:", len(raw))  # DEBUG

    # 4) Převod všech záznamů na objekt → dokument
    docs = [ContainerData.from_raw(c).to_document() for c in raw]
    if docs:
        print("Ukázka 1. dokumentu:", docs[0])  # DEBUG

    # (volitelné) vyčistit kolekci při opakovaných bězích:
    # col.delete_many({})

    # 5) Vložení a kontrola počtů
    before = col.count_documents({})
    print("Počet dokumentů PŘED:", before)  # DEBUG

    if docs:
        res = col.insert_many(docs)
        print(f"✅ Vloženo dokumentů: {len(res.inserted_ids)}")
    else:
        print("⚠️ Seznam dokumentů je prázdný, nevkládám nic.")
        return

    after = col.count_documents({})
    print("Počet dokumentů PO:  ", after)  # DEBUG

if __name__ == "__main__":
    main()
