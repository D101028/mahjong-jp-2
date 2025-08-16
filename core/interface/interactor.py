import json
import time
from threading import Thread
from typing import Any, Literal

from .prompt import Prompt

class TerminalResponse:
    def __init__(self, response: str = "", is_ok: bool = False) -> None:
        self.response = response
        self.is_ok = is_ok

interactor_log: list[str] = []
class Interactor:
    def __init__(self, prompts: list[Prompt]) -> None:
        self.prompts: list[Prompt] = prompts

    def to_json(self) -> str:
        return json.dumps([
            prompt.to_dict() for prompt in self.prompts
        ])

    def log(self, msg: str) -> None:
        interactor_log.append(msg)

    def ask(self, msg: str) -> tuple[Thread | None, TerminalResponse]:
        self.log(msg)
        print(msg)
        if all(prompt.intent.response_type == 'no-response' for prompt in self.prompts):
            result = TerminalResponse(json.dumps([None for _ in range(len(self.prompts))]), True)
            return None, result
        result = TerminalResponse()
        def process():
            ans = input(">>>")
            result.response = ans
            result.is_ok = True
        thread = Thread(target=process)
        thread.start()
        return thread, result

    def communicate(self) -> list[Any]:
        msg = self.to_json()
        _, result = self.ask(msg)
        while True:
            time.sleep(0.1)
            if result.is_ok:
                ans = result.response
                try:
                    obj = json.loads(ans)
                except Exception as e:
                    return self.communicate()
                if not isinstance(obj, list) or len(obj) != len(self.prompts):
                    return self.communicate()
                return obj
