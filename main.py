import json
from datetime import datetime

def main():
    """
    Hlavní funkce programu:
    - načte JSON se seznamem kontejnerů
    - z každého kontejneru vytáhne jméno, status, CPU, paměť, vytvoření a IP adresy
    - vytvoří přehledný výstup i objektový seznam výsledků
    """

    # Načtení JSON souboru
    # Otevřu data.json a načtu celý obsah do proměnné `data`
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Počet kontejnerů: {len(data)}\n")

    # Tady si budu ukládat výsledky jako seznam slovníků (každý kontejner = jeden dict)
    results = []

    # Průchod seznamem kontejnerů
    for i, container in enumerate(data, start=1):
        # Základní údaje
        name = container.get("name", "neznámé_jméno")

        # Status může být buď přímo nahoře, nebo uvnitř bloku "state"
        status = container.get("status")
        if not status:
            state_block = container.get("state")
            if isinstance(state_block, dict):
                status = state_block.get("status")

        # Paměť a CPU – používám bezpečné přístupy přes .get() a or {}
        mem_usage = ((container.get("state") or {}).get("memory") or {}).get("usage")
        cpu_usage = ((container.get("state") or {}).get("cpu") or {}).get("usage")

        # Převod created_at na UTC timestamp
        created_at_str = container.get("created_at")
        if created_at_str:
            try:
                # fromisoformat neumí koncovku "Z", proto ji nahradím za +00:00 (UTC)
                dt = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                created_at_utc = int(dt.timestamp())
            except Exception:
                created_at_utc = None
        else:
            created_at_utc = None

        # Síťová rozhraní a IP adresy
        # Některé kontejnery mohou mít více síťových rozhraní (např. eth0, docker0…)
        state = container.get("state") or {}
        network = state.get("network") or {}
        ips = []
        for iface in network.values():
            for rec in (iface.get("addresses") or []):
                addr = rec.get("address")
                if addr:
                    ips.append(addr)

        # Jen IPv4 adresy (bez dvojtečky)
        ipv4 = [ip for ip in ips if ":" not in ip]

        # Vytvořím slovník s přehlednými daty o kontejneru
        container_info = {
            "name": name,
            "status": status,
            "cpu_usage": cpu_usage,
            "memory_usage": mem_usage,
            "created_at": created_at_utc,
            "ips": ipv4
        }
        results.append(container_info)

        # Krátký výpis do konzole – kontrola a přehled
        print(f"{i}. Název:     {name}")
        print(f"   Stav:       {status}")
        print(f"   Paměť:      {mem_usage} bajtů")
        print(f"   CPU:        {cpu_usage}")
        print(f"   Vytvořen:   {created_at_utc} (UTC timestamp)")
        print(f"   IPs celkem: {len(ips)}")
        print(f"   IPv4:       {ipv4}")
        print("-" * 40)

    # Ukázka jednoho hotového objektu pro kontrolu (první a poslední)
    if results:
        print("\nUkázka objektu pro 1. kontejner:")
        print(json.dumps(results[0], indent=2, ensure_ascii=False))

        # Pokud existuje 17. kontejner, ukážu i ten (kvůli kontrole dat)
        if len(results) >= 17:
            print("\nUkázka objektu pro poslední kontejner:")
            print(json.dumps(results[16], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
