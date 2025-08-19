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

class DebugInput:
    responses: list[str] = []
    
    @classmethod
    def push(cls, *contents: str) -> None:
        cls.responses += contents
    
    @classmethod
    def pull(cls) -> str:
        if not cls.responses:
            raise Exception("Response not found")
        return cls.responses.pop(0)

interactor_log: list[str] = []
response_log: list[str] = []

class Interactor:
    def __init__(self, prompts: list[Prompt]) -> None:
        self.prompts: list[Prompt] = prompts

    def to_json(self) -> str:
        return json.dumps([
            prompt.to_dict() for prompt in self.prompts
        ])

    def to_console(self) -> str:
        result = "\n---\n".join([str(prompt) for prompt in self.prompts])
        return f"======\n{result}"

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

    def debug_communicate(self) -> list[Any]:
        print(self.to_console())
        if all(prompt.intent.response_type == 'no-response' for prompt in self.prompts):
            ans = json.dumps([None for _ in range(len(self.prompts))])
        else:
            ans = DebugInput.pull()
            print(f"Responses: {ans}")
        try:
            obj = json.loads(ans)
        except Exception as e:
            raise Exception(f"Unknown ans: {ans}")
        if not isinstance(obj, list) or len(obj) != len(self.prompts):
            raise Exception(f"Unknown ans: {ans}")
        return obj

    def communicate(self) -> list[Any]:
        if Config.DEBUGGING:
            return self.debug_communicate()
        msg = self.to_json()
        _, result = self.ask(msg)
        while True:
            if result.is_ok:
                ans = result.response
                response_log.append(ans)
                try:
                    obj = json.loads(ans)
                except Exception as e:
                    _, result = self.ask("again")
                    continue
                if not isinstance(obj, list) or len(obj) != len(self.prompts):
                    _, result = self.ask("again")
                    continue
                return obj
            time.sleep(0.1)
