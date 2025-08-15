import json
from typing import Any, Literal, overload

from core.types import *

class Intent:
    @overload
    def __init__(
        self, 
        response_type: Literal['no-response'], 
        purpose: Literal[
            "player-tehai-update-notation"
        ], 
        content: PlayerTehaiUpdateNotationContentType) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['no-response'], 
        purpose: Literal[
            "player-datsuhai-notation", 
        ], 
        content: PlayerDatsuhaiNotationContentType) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['no-response'], 
        purpose: Literal[
            "river-update-notation", 
        ], 
        content: RiverUpdateNotationContentType) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['no-response'], 
        purpose: Literal[
            "hyoujihai-update-notation"
        ], 
        content: dict[str, Any]) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['standard'], 
        purpose: Literal[
            "ask-to-datsuhai"
        ], 
        content: AskToDatsuhaiContentType) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['standard'], 
        purpose: Literal[
            "ask-to-datsuhai-or-other-choices"
        ], 
        content: AskToDatsuhaiOrOtherChoicesContentType) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['standard'], 
        purpose: Literal[
            "ask-to-choices"
        ], 
        content: AskToChoicesContentType) -> None:
        ...

    def __init__(
            self, 
            response_type: Literal["standard", "no-response"], 
            purpose: Literal[
                "player-tehai-update-notation", 
                "player-datsuhai-notation", 
                "river-update-notation", 
                "hyoujihai-update-notation", 
                "ask-to-datsuhai", 
                "ask-to-datsuhai-or-other-choices", 
                "ask-to-choices"
            ], 
            content: Any
        ) -> None:
        self.response_type = response_type
        self.purpose = purpose
        self.content = content if isinstance(content, str) else json.dumps(content)

    def to_dict(self):
        return {
            "response-type": self.response_type, 
            "purpose": self.purpose, 
            "content": self.content
        }
