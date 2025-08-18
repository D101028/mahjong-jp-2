import json
from typing import Literal

with open("lang/tc.json", encoding="utf8") as fp:
    lang_data = json.load(fp)

class Config:
    DEBUGGING = True

    lang: dict[Literal["core.pai"] | Literal["core.game"], dict[str, str]] = lang_data

