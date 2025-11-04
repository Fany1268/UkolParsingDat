🧾 README.md (CZ + EN verze)

🇨🇿 Projekt: UkolParsingDat

Tento projekt vznikl jako úkol v rámci výběrového řízení na pozici junior programátora.
Cílem bylo zpracovat JSON soubor se seznamem LXC kontejnerů, vytáhnout z něj požadované údaje
a uložit je do databáze (MongoDB Atlas).

🔧 Hlavní funkce projektu

Načítá soubor data.json

Pro každý kontejner zpracuje:

jméno

status (včetně vnořeného pole state)

využití CPU a paměti

čas vytvoření (převedený na UTC timestamp)

všechny IPv4 adresy

Výsledek je uložen do kolekce containers v databázi parsing

🧩 Použité technologie

Python 3.11

MongoDB Atlas (připojení přes pymongo / motor)

async/await přístup pro efektivní práci s databází

.env pro bezpečné ukládání přístupových údajů

Dockerfile – projekt lze snadno dockerizovat a nasadit v produkci

🚀 Spuštění lokálně
# aktivace virtuálního prostředí
source .venv/Scripts/activate

# spuštění hlavního skriptu
python save_all_via_model_async.py

🐳 Spuštění v Dockeru
# build image
docker build -t ukol-parsing-dat .

# run container
docker run --env-file .env ukol-parsing-dat

📦 Struktura projektu
UkolParsingDat/
├── data.json
├── model.py
├── save_all_via_model_async.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
└── README.md

🧠 Poznámky

Projekt je psán srozumitelně a obsahuje komentáře v češtině,
aby byl vhodný i pro výukové účely a ukázku postupného vývoje.

📅 Poslední aktualizace: 4. listopadu 2025
👨‍💻 Autor: František Krátký

🇬🇧 English version

This project was created as part of a junior developer assignment.
It parses a JSON file with a list of LXC containers, extracts useful data,
and saves it into a MongoDB Atlas database.

Main features

Reads data.json

Extracts name, status, CPU & memory usage, creation time, and IP addresses

Converts timestamps to UTC

Saves data into MongoDB collection containers

Async code for better performance

Docker-ready for production deployment

Technologies

Python 3.11 · MongoDB Atlas · Motor (async driver) · python-dotenv · Docker

Run locally
python save_all_via_model_async.py

Run in Docker
docker build -t ukol-parsing-dat .
docker run --env-file .env ukol-parsing-dat


✅ Ready for production, learning, and review.

