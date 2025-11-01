import json
from datetime import datetime

def main():
    # Načtu celý JSON soubor do proměnné `data`
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Jen kontrola, kolik je tam kontejnerů
    print(f"Počet kontejnerů: {len(data)}\n")

    # Procházím kontejnery jeden po druhém, `i` je pořadové číslo od 1
    for i, container in enumerate(data, start=1):
        # Vezmu jméno (když chybí, napíšu "neznámé_jméno")
        name = container.get("name", "neznámé_jméno")

        # Zjistím stav: buď je přímo nahoře, nebo je uvnitř "state"
        status = container.get("status")
        if not status:
            state_block = container.get("state")
            if isinstance(state_block, dict):
                status = state_block.get("status")

        # Paměť a CPU beru bezpečně přes `or {}` (když něco chybí, použiju prázdný slovník)
        mem_usage = ((container.get("state") or {}).get("memory") or {}).get("usage")
        cpu_usage = ((container.get("state") or {}).get("cpu") or {}).get("usage")

        # created_at převedu na UTC timestamp (sekundy od 1.1.1970)
        created_at_str = container.get("created_at")
        if created_at_str:
            try:
                # fromisoformat neumí "Z", proto ji nahradím za +00:00 (UTC)
                dt = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
                created_at_utc = int(dt.timestamp())
            except Exception:
                created_at_utc = None
        else:
            created_at_utc = None

        # IP adresy: projdu síťová rozhraní a posbírám všechny adresy (state.network.*.addresses[].address)
        state = container.get("state") or {}
        network = state.get("network") or {}
        ips = []
        for iface in network.values():
            for rec in (iface.get("addresses") or []):
                addr = rec.get("address")
                if addr:
                    ips.append(addr)

        # Jen IPv4 (bez dvojtečky)
        ipv4 = [ip for ip in ips if ":" not in ip]

        # Přehledný výpis výsledků pro jeden kontejner
        print(f"{i}. Název:     {name}")
        print(f"   Stav:       {status}")
        print(f"   Paměť:      {mem_usage} bajtů")
        print(f"   CPU:        {cpu_usage}")
        print(f"   Vytvořen:   {created_at_utc} (UTC timestamp)")
        print(f"   IPs celkem: {len(ips)}")
        print(f"   IPv4:       {ipv4}")
        print("-" * 40)

if __name__ == "__main__":
    main()
