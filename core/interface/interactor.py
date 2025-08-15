import json
import time
from threading import Thread
from typing import Any, Literal

from .prompt import Prompt

interactor_log: list[str] = []
class Interactor:
    def __init__(self, prompts: list[Prompt]) -> None:
        self.prompts: list[Prompt] = prompts

    def to_json(self) -> str:
        return json.dumps([
            prompt.to_json() for prompt in self.prompts
        ])

    def log(self, msg: str) -> None:
        interactor_log.append(msg)

    def ask(self, msg: str) -> tuple[Thread, dict[Literal["response"], str | None]]:
        self.log(msg)
        print(msg)
        result: dict[Literal["response"], str | None] = {"response": None}
        def process():
            ans = input()
            result["response"] = ans
        thread = Thread(target=process)
        thread.start()
        return thread, result

    def communicate(self) -> list[Any]:
        msg = self.to_json()
        _, result = self.ask(msg)
        while True:
            time.sleep(0.1)
            ans = result["response"]
            if ans is not None:
                try:
                    obj = json.loads(ans)
                except Exception as e:
                    return self.communicate()
                if not isinstance(obj, list) or len(obj) != len(self.prompts):
                    return self.communicate()
                return obj
