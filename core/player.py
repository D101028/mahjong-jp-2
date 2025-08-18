from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.game.yama import YamaType

from core.ext import tokens, support
from core.pai import Pai, Tehai, Param, is_tenpai
from core.types import *

class River:
    def __init__(self) -> None:
        self.pai_list: list[Pai] = []
        self.riichi_hai_pos: int | None = None

    def datsuhai(self, pai: Pai, to_riichi: bool = False) -> None:
        self.pai_list.append(pai)
        if to_riichi:
            self.riichi_hai_pos = len(self.pai_list) - 1
    
    def to_dict(self) -> RiverDictType:
        return {
            "pai-list": [pai.to_dict() for pai in self.pai_list], 
            "riichi-hai-pos": self.riichi_hai_pos
        }

players_dict: dict[int, 'Player'] = {}
id_players_dict: dict[int, 'Player'] = {}

def get_ordered_players(player: 'Player') -> list['Player']:
    """回傳不含傳入 player 的 player chain (從下家開始)"""
    result: list['Player'] = []
    temp_player = player.next()
    while temp_player != player:
        result.append(temp_player)
    return result

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
        self.is_junme_broken: bool = False

        self.doujin_furiten_pais: set[Pai] = set() # 保存會同巡振聽的牌，玩家打出牌後清空
        # self.riichi_furiten_pais: set[Pai] = set() # 保存會立直振聽的牌
        self.datsu_furiten_pais: set[Pai] = set()  # 保存所有打出過的牌
        self.is_riichi_furiten: bool = False

        players_dict[menfon] = self
        id_players_dict[ID] = self

    def __hash__(self) -> int:
        return self.ID.__hash__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        else:
            return self.ID == other.ID

    @property
    def is_riichi(self) -> bool:
        return self.riichi_junme is not None

    def draw(self, yama: 'YamaType') -> None:
        """從 yama 摸牌"""
        if self.tehai.new_pai is not None:
            raise Exception("there already exists a pai in the tehai")
        p = yama.draw()
        self.tehai.new_pai = p

    def datsuhai(self, pos: int | None = None, to_riichi: bool = False) -> Pai:
        """從 tehai 打牌"""
        # 巡目處理
        self.player_junme += 1
        self.is_junme_broken = False
        if to_riichi:
            self.riichi_junme = self.player_junme
        # 選擇打/切牌
        if pos is None:
            # 摸切
            if self.tehai.new_pai is None:
                raise Exception("Could not found new_pai in tehai")
            p = self.tehai.new_pai
            self.river.datsuhai(p, to_riichi)
            self.tehai.new_pai = None
            return p
        if pos >= len(self.tehai.pai_list) or pos < -len(self.tehai.pai_list):
            raise IndexError(f"Out of length of tehai.pai_list. Length: {len(self.tehai.pai_list)}, Given: {pos}")
        # 打出牌
        pai = self.tehai.pai_list.pop(pos)
        if self.tehai.new_pai is not None:
            self.tehai.pai_list.append(self.tehai.new_pai)
            self.tehai.new_pai = None
        self.river.datsuhai(pai, to_riichi)
        # 振聽處理
        self.doujin_furiten_pais.clear()
        self.datsu_furiten_pais.add(pai)
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
        if self.is_riichi_furiten:
            return True
        tenpai_list = self.tehai.get_tenpais()
        if not tenpai_list:
            return False
        full_set = self.doujin_furiten_pais.union(self.datsu_furiten_pais)
        return any((p in full_set) for p in tenpai_list)
        
    def is_able_to_ron(self, pai: Pai, param: Param) -> bool:
        if self.is_furiten():
            return False
        return self.tehai.is_able_to_ron(pai, param)
    
    def is_able_to_riichi(self) -> bool:
        if not self.is_menchin():
            return False
        pai_list = self.tehai.pai_list.copy()
        if self.tehai.new_pai is not None:
            pai_list.append(self.tehai.new_pai)
        else:
            raise Exception("self.tehai.new_pai here should not be None")
            # return False
        pais_set: set[Pai] = set(pai_list)
        copied_list = pai_list.copy()
        for p in pais_set:
            copied_list.remove(p)
            if is_tenpai(copied_list):
                return True
            copied_list = pai_list.copy()
        return False
