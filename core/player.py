"""
    Player class
    including calculate is_agari
    HansuuResult class
"""
from .ext import tokens
from .pai import Pai, Tehai, is_agari

class River:
    def __init__(self) -> None:
        self.pai_list: list[Pai] = []
        self.riichi_hai_pos: int | None = None

class Player:
    def __init__(self, ID: int):
        self.ID = ID # 0,1,2,(3)
        self.tensuu: int 
        self.menfon: str # lang.ton, lang.nan, lang.shaa, lang.pei
        self.tehai: Tehai
        self.river: River = River()

        self.tsumo_pai: Pai | None = None
        self.ron_temp_pai: Pai | None = None

        self.is_riichi: bool = False
        self.riichi_junme: bool | None = None
        self.player_junme: int = 0 # plus 1 if 自家摸牌、鳴牌 or 任一人吃、碰、槓、拔北

        self.doujin_furiten_pais: list[Pai] = []
        self.riichi_furiten_pais: list[Pai] = []
        self.datsu_furiten_pais: list[Pai] = []

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        else:
            return self.ID == other.ID

    def is_menchin(self):
        return all([furo.type == tokens.ankan for furo in self.tehai.furo_list])

    def is_agari(self):
        # 檢查胡牌型
        all_pai: list[Pai] = []
        if self.tsumo_pai is None:
            if self.ron_temp_pai is None:
                return False
            all_pai.append(self.ron_temp_pai)
        else:
            all_pai.append(self.tsumo_pai)
        furo_pai: list[Pai] = []
        for furo in self.tehai.furo_list:
            furo_pai += furo.to_agari_cal()
        all_pai += self.tehai.pai_list + furo_pai

        return is_agari(all_pai)

    def is_furiten(self):
        tenpai_list = self.tehai.get_tenpais()
        if not tenpai_list:
            return False
        full_list = self.doujin_furiten_pais + self.riichi_furiten_pais + self.datsu_furiten_pais
        return any(p in full_list for p in tenpai_list)
