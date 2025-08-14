from core.ext import tokens, support
from core.pai import Pai, Tehai, is_agari

class River:
    def __init__(self) -> None:
        self.pai_list: list[Pai] = []
        self.riichi_hai_pos: int | None = None

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

        # self.tsumo_pai: Pai | None = None
        # self.ron_temp_pai: Pai | None = None

        self.riichi_junme: bool | None = None # 打出立直牌後的巡目
        self.player_junme: int = 0

        self.doujin_furiten_pais: set[Pai] = set() # 保存會同巡振聽的牌，玩家打出牌後清空
        self.riichi_furiten_pais: set[Pai] = set() # 保存會立直振聽的牌
        self.datsu_furiten_pais: set[Pai] = set()  # 保存所有打出過的牌

        players_dict[menfon] = self

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return False
        else:
            return self.ID == other.ID

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

    # def is_agari(self):
    #     # 檢查胡牌型
    #     pai_list: list[Pai] = []
    #     if self.tsumo_pai is None:
    #         if self.ron_temp_pai is None:
    #             return False
    #         pai_list.append(self.ron_temp_pai)
    #     else:
    #         pai_list.append(self.tsumo_pai)
    #     pai_list += self.tehai.pai_list

    #     return is_agari(pai_list)

    def is_furiten(self) -> bool:
        tenpai_list = self.tehai.get_tenpais()
        if not tenpai_list:
            return False
        full_set = self.doujin_furiten_pais \
                        .union(self.riichi_furiten_pais) \
                        .union(self.datsu_furiten_pais)
        return any((p in full_set) for p in tenpai_list)
        
