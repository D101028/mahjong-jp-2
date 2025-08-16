
from core.player import Player
from .intent import Intent

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