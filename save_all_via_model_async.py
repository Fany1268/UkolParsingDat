# save_all_via_model_async.py
import asyncio
import json
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient  # async Mongo klient
import aiofiles  # async čtení souboru
from model import ContainerData

async def main():
    # 1) načtení .env
    load_dotenv()
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise RuntimeError("❌ Chybí MONGO_URI v .env")

    # 2) async připojení k MongoDB Atlas
    client = AsyncIOMotorClient(uri)
    db = client["parsing"]
    col = db["containers"]

    # 3) async načtení data.json
    async with aiofiles.open("data.json", "r", encoding="utf-8") as f:
        text = await f.read()
    raw = json.loads(text)
    if not isinstance(raw, list):
        raise RuntimeError("❌ Očekávám list kontejnerů v data.json")

    # 4) převod přes dataclass → dokumenty
    docs = [ContainerData.from_raw(c).to_document() for c in raw]

    # (volitelné) vyčistit kolekci před vložením:
    # await col.delete_many({})

    # 5) async insert
    if docs:
        res = await col.insert_many(docs)
        print(f"✅ [ASYNC] Uloženo dokumentů: {len(res.inserted_ids)}")
    else:
        print("⚠️ [ASYNC] Nic k uložení.")

if __name__ == "__main__":
    asyncio.run(main())
