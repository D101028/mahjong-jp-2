from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game.yama import YamaType

from core.ext import tokens, support
from core.pai import Pai, Tehai, is_agari
from core.types import *

class River:
    def __init__(self) -> None:
        self.pai_list: list[Pai] = []
        self.riichi_hai_pos: int | None = None

    def datsuhai(self, pai: Pai, is_riichi: bool = False) -> None:
        self.pai_list.append(pai)
        if is_riichi:
            self.riichi_hai_pos = len(self.pai_list) - 1
    
    def to_dict(self) -> RiverDictType:
        return {
            "pai-list": [pai.to_dict() for pai in self.pai_list], 
            "riichi-hai-pos": self.riichi_hai_pos
        }

players_dict: dict[int, 'Player'] = {}

class Player:
    def __init__(self, ID: int, name: str, tensuu: int, menfon: int) -> None:
        if menfon not in support.fonwei_tuple:
            raise ValueError(f"Unknown menfon: {menfon}")

        self.ID = ID # 0,1,2,(3)
        self.name = name
        self.tensuu: int = tensuu
        self.menfon: int = menfon # tokens.ton, tokens.nan, tokens.shaa, (tokens.pei)
        self.tehai: Tehai = Tehai([])
        self.river: River = River()

        self.riichi_junme: int | None = None # 打出立直牌後的巡目
        self.player_junme: int = 0
        self.break_junme: bool = False

        self.doujin_furiten_pais: set[Pai] = set() # 保存會同巡振聽的牌，玩家打出牌後清空
        self.riichi_furiten_pais: set[Pai] = set() # 保存會立直振聽的牌
        self.datsu_furiten_pais: set[Pai] = set()  # 保存所有打出過的牌

        players_dict[menfon] = self

    def __hash__(self) -> int:
        return self.ID.__hash__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        else:
            return self.ID == other.ID

    def draw(self, yama: 'YamaType') -> None:
        """從 yama 摸牌"""
        if self.tehai.new_pai is not None:
            raise Exception("there already exists a pai in the tehai")
        p = yama.draw()
        self.tehai.new_pai = p

    def datsuhai(self, pos: int | None = None, is_riichi: bool = False) -> Pai:
        """從 tehai 打牌"""
        self.player_junme += 1
        self.break_junme = False
        if is_riichi:
            self.riichi_junme = self.player_junme
        if pos is None:
            # 摸切
            if self.tehai.new_pai is None:
                raise Exception("Could not found new_pai in tehai")
            p = self.tehai.new_pai
            self.river.datsuhai(p, is_riichi)
            self.tehai.new_pai = None
            return p
        if pos >= len(self.tehai.pai_list) or pos < -len(self.tehai.pai_list):
            raise IndexError(f"Out of length of tehai.pai_list. Length: {len(self.tehai.pai_list)}, Given: {pos}")
        
        pai = self.tehai.pai_list.pop(pos)
        if self.tehai.new_pai is not None:
            self.tehai.pai_list.append(self.tehai.new_pai)
            self.tehai.new_pai = None
        self.river.datsuhai(pai, is_riichi)
        return pai

    def previous(self) -> 'Player':
        """上家"""
        player: Player | None
        if players_dict.get(support.fonwei_tuple[-1]) is None:
            # Sanin
            if self.menfon == support.fonwei_tuple[0]:
                player = players_dict.get(support.fonwei_tuple[-2])
            else:
                player = players_dict.get(support.fonwei_tuple[support.fonwei_tuple.index(self.menfon) - 1])
        else:
            # Yonin
            if self.menfon == support.fonwei_tuple[0]:
                player = players_dict.get(support.fonwei_tuple[-1])
            else:
                player = players_dict.get(support.fonwei_tuple[support.fonwei_tuple.index(self.menfon) - 1])
        if player is None:
            raise Exception("Could not get some players from players_dict")
        return player

    def next(self) -> 'Player':
        """下家"""
        player: Player | None
        if players_dict.get(support.fonwei_tuple[-1]) is None:
            # Sanin
            if self.menfon == support.fonwei_tuple[-2]:
                player = players_dict.get(support.fonwei_tuple[0])
            else:
                player = players_dict.get(support.fonwei_tuple[support.fonwei_tuple.index(self.menfon) + 1])
        else:
            # Yonin
            if self.menfon == support.fonwei_tuple[-1]:
                player = players_dict.get(support.fonwei_tuple[0])
            else:
                player = players_dict.get(support.fonwei_tuple[support.fonwei_tuple.index(self.menfon) + 1])
        if player is None:
            raise Exception("Could not get some players from players_dict")
        return player

    def is_menchin(self) -> bool:
        return all(furo.type == tokens.ankan for furo in self.tehai.furo_list)

    def is_furiten(self) -> bool:
        tenpai_list = self.tehai.get_tenpais()
        if not tenpai_list:
            return False
        full_set = self.doujin_furiten_pais \
                        .union(self.riichi_furiten_pais) \
                        .union(self.datsu_furiten_pais)
        return any((p in full_set) for p in tenpai_list)
        
