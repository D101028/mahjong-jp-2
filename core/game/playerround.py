from typing import Union

from core.player import Player
from core.game.yama import YoninYama

class PlayerRoundParam:
    def __init__(
        self, 
    ) -> None:
        pass 

class YoninPlayerRound:
    def __init__(self, player: Player, yama: YoninYama, prparam: PlayerRoundParam) -> None:
        self.player = player
        self.yama = yama
        self.prparam = prparam
    
    def run(self) -> Union['YoninPlayerRound', None]:
        """Run the round and return next round or None if it's the last player round"""
        self.player
        return 
