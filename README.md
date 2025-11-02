# UkolParsingDat

## 🇨🇿 Popis projektu
Tento projekt vznikl jako úkol v rámci výběrového řízení na pozici **junior programátora**.  
Cílem je zpracovat JSON soubor se seznamem LXC kontejnerů, vytáhnout z něj požadované údaje  
a připravit data k dalšímu zpracování (např. pro uložení do databáze).

### Aktuální stav:
- Skript `main.py` načítá JSON soubor `data.json`
- Pro každý kontejner vypisuje:
  - jméno
  - status
  - CPU a paměť
  - čas vytvoření (převedený na UTC timestamp)
  - všechny IPv4 adresy
- Výstup je zároveň ukládán do seznamu slovníků (`results`)
- Kód obsahuje české komentáře pro srozumitelnost a výuku

### Další krok:
- Normalizace dat do objektů (OOP přístup)
- Uložení do MongoDB (cloud Atlas)

---

## Project overview
This project was created as part of a **junior developer** technical assignment.  
The goal is to parse a JSON file containing a list of LXC containers, extract the required data,  
and prepare it for further use (e.g., database storage).

### Current progress:
- Script `main.py` reads `data.json`
- Extracts and displays:
  - container name
  - status
  - CPU & memory usage
  - creation time (converted to UTC timestamp)
  - IPv4 addresses
- Data is stored in a list of dictionaries (`results`)
- Code includes detailed comments for better readability and learning

### Next steps:
- Normalize data into Python objects
- Store them in MongoDB Atlas

---

📅 **Poslední update:** 2. listopadu 2025  
👨‍💻 **Autor:** František Krátký
