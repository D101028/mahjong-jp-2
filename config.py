import json
from typing import Literal

with open("lang/tc.json", encoding="utf8") as fp:
    lang_data = json.load(fp)

class Config:
    lang: dict[Literal["core"] | Literal["game"], dict[str, str]] = lang_data

