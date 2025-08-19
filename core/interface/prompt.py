from typing import Any

from core.player import Player, id_players_dict
from .intent import Intent, to_intent

def to_prompt(dict1: dict[str, Any]):
    target_id = dict1.get('target-id')
    intent_dict = dict1.get('intent')
    assert target_id is not None and intent_dict is not None
    intent = to_intent(intent_dict)
    return Prompt(id_players_dict[target_id], intent)

class Prompt:
    def __init__(
            self, 
            target_player: Player, 
            intent: Intent
        ) -> None:
        self.target_player: Player = target_player
        self.intent: Intent = intent

    def to_dict(self):
        return {
            "target-id": self.target_player.ID, 
            "intent": self.intent.to_dict()
        }