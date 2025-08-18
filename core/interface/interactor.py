import json
import time
from threading import Thread
from typing import Any, Literal

from .prompt import Prompt
from config import Config
from core.types import *

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

    def to_console(self) -> str:
        # result = ""
        # for prompt in self.prompts:
        #     d1 = prompt.intent.to_dict()
        #     for key, value in prompt.intent.content.items():
        #         if isinstance(value, (list, tuple)) and is_same_dict_type(value[0], PaiDictType):
        #             d1['content'][key] = " ".join(value)
            
        #     result = f"{result}\n{json.dumps(d1, indent=4)}"
        result = json.dumps([
            prompt.to_dict() for prompt in self.prompts
        ], indent=2)
        return result

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
        msg = self.to_json() if not Config.DEBUGGING else self.to_console()
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
