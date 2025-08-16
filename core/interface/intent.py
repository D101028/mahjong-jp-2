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
            "player-minpai-notation", 
        ], 
        content: PlayerMinpaiNotationContentType) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['no-response'], 
        purpose: Literal[
            "player-penuki-notation", 
        ], 
        content: PlayerPenukiNotationContentType) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['no-response'], 
        purpose: Literal[
            "player-ron-notation", 
        ], 
        content: PlayerRonNotationContentType) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['no-response'], 
        purpose: Literal[
            "player-tsumo-notation", 
        ], 
        content: PlayerTsumoNotationContentType) -> None:
        ...
    @overload
    def __init__(
        self, 
        response_type: Literal['no-response'], 
        purpose: Literal[
            "hyoujihai-update-notation"
        ], 
        content: HyoujihaiUpdateNotationContentType) -> None:
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
            response_type: Literal['no-response', 'standard'], 
            purpose: str, 
            content: Any
        ) -> None:
        self.response_type: Literal['no-response', 'standard'] = response_type
        self.purpose = purpose
        self.content = content

    def to_dict(self):
        return {
            "response-type": self.response_type, 
            "purpose": self.purpose, 
            "content": self.content
        }
