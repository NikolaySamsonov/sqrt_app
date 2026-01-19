import json
import os
from typing import Dict

class LocalizationManager:
    def __init__(self, locales_dir: str, default_lang: str = "ru"):
        self.locales_dir = locales_dir
        self._data: Dict[str, Dict[str, str]] = {}
        self.lang = default_lang
        self._load_all()

    def _load_all(self):
        for fn in os.listdir(self.locales_dir):
            if fn.lower().endswith(".json"):
                lang = os.path.splitext(fn)[0]
                path = os.path.join(self.locales_dir, fn)
                with open(path, "r", encoding="utf-8") as f:
                    self._data[lang] = json.load(f)

        if self.lang not in self._data and self._data:
            self.lang = sorted(self._data.keys())[0]

    def available_languages(self):
        return sorted(self._data.keys())

    def set_language(self, lang: str):
        if lang in self._data:
            self.lang = lang

    def t(self, key: str) -> str:
        return self._data.get(self.lang, {}).get(key, key)
