from typing import Literal

from core.interface import Interactor, Prompt, Intent
from core.pai import create_pai_list, Pai, FuroType
from core.player import id_players_dict

def modify_tehai(ID: int, pais: str | None = None, new_pai: str | None | Literal['skip'] = 'skip', furo_list: list[FuroType] | None = None):
    player = id_players_dict[ID]
    if pais is not None:
        player.tehai.pai_list = create_pai_list(pais)
    if new_pai != 'skip':
        player.tehai.new_pai = Pai(new_pai) if new_pai else None
    if furo_list is not None:
        player.tehai.furo_list = furo_list
    player.tehai.sort()
    print("Tehai Modified: ")
    # Send Messages
    Interactor([Prompt(player, Intent('no-response', 'player-tehai-update-notation', {
        'tehai-info': player.tehai.to_dict()
    }))]).communicate()
