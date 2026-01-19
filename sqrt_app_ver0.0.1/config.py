import json
from dataclasses import dataclass

@dataclass
class AppConfig:
    default_language: str = "ru"
    default_precision: int = 2

def load_config(path: str) -> AppConfig:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return AppConfig(
            default_language=str(data.get("default_language", "ru")),
            default_precision=int(data.get("default_precision", 2)),
        )
    except Exception:
        return AppConfig()
