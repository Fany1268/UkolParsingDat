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
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 🆕 Ověřím, že kořen je seznam (list)
    if not isinstance(data, list):
        print("❌ Očekávám, že data.json obsahuje seznam (list) kontejnerů.")
        return

    print(f"Počet kontejnerů: {len(data)}\n")

    results = []

    # Průchod seznamem kontejnerů
    for i, container in enumerate(data, start=1):
        name = container.get("name", "neznámé_jméno")

        # Status může být nahoře, nebo uvnitř "state"
        status = container.get("status")
        if not status:
            state_block = container.get("state")
            if isinstance(state_block, dict):
                status = state_block.get("status")

        # Paměť a CPU – bezpečný přístup
        mem_usage = ((container.get("state") or {}).get("memory") or {}).get("usage")
        cpu_usage = ((container.get("state") or {}).get("cpu") or {}).get("usage")

        # Převod created_at na UTC timestamp
        created_at_str = container.get("created_at")
        if created_at_str:
            try:
                dt = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                created_at_utc = int(dt.timestamp())
            except Exception:
                created_at_utc = None
        else:
            created_at_utc = None

        # Síťová rozhraní a IP adresy
        state = container.get("state") or {}
        network = state.get("network") or {}
        ips = []
        for iface in network.values():
            for rec in (iface.get("addresses") or []):
                addr = rec.get("address")
                if addr:
                    ips.append(addr)
        ipv4 = [ip for ip in ips if ":" not in ip]

        # Objekt (slovník) pro výsledky
        container_info = {
            "name": name,
            "status": status,
            "cpu_usage": cpu_usage,
            "memory_usage": mem_usage,
            "created_at": created_at_utc,
            "ips": ipv4
        }
        results.append(container_info)

        # Výpis do konzole
        print(f"{i}. Název:     {name}")
        print(f"   Stav:       {status}")
        print(f"   Paměť:      {mem_usage} bajtů")
        print(f"   CPU:        {cpu_usage}")
        print(f"   Vytvořen:   {created_at_utc} (UTC timestamp)")
        print(f"   IPs celkem: {len(ips)}")
        print(f"   IPv4:       {ipv4}")
        print("-" * 40)

    # Ukázka objektů pro kontrolu (první a poslední)
    if results:
        print("\nUkázka objektu pro 1. kontejner:")
        print(json.dumps(results[0], indent=2, ensure_ascii=False))

        if len(results) > 1:
            print("\nUkázka objektu pro poslední kontejner:")
            print(json.dumps(results[-1], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
