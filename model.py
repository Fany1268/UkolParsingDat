# model.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ContainerData:
    name: str
    status: str | None
    cpu_usage: int | None
    memory_usage: int | None
    created_at: int | None      # UTC timestamp
    ips: list[str]

    @staticmethod
    def _to_utc_ts(iso_str: str | None) -> int | None:
        if not iso_str:
            return None
        try:
            return int(datetime.fromisoformat(iso_str.replace("Z", "+00:00")).timestamp())
        except Exception:
            return None

    @classmethod
    def from_raw(cls, container: dict) -> "ContainerData":
        name = container.get("name", "neznámé_jméno")
        status = container.get("status") or (container.get("state") or {}).get("status")

        state = container.get("state") or {}
        cpu_usage = (state.get("cpu") or {}).get("usage")
        memory_usage = (state.get("memory") or {}).get("usage")

        network = state.get("network") or {}
        ipv4 = []
        for iface in network.values():
            for rec in (iface.get("addresses") or []):
                addr = rec.get("address")
                if addr and ":" not in addr:
                    ipv4.append(addr)

        return cls(
            name=name,
            status=status,
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            created_at=cls._to_utc_ts(container.get("created_at")),
            ips=ipv4,
        )

    def to_document(self) -> dict:
        return {
            "name": self.name,
            "status": self.status,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "created_at": self.created_at,
            "ips": self.ips,
        }
