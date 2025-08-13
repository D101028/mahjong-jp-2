from core.ext import tokens, support
from core.pai import Pai, Tehai, is_agari

class River:
    def __init__(self) -> None:
        self.pai_list: list[Pai] = []
        self.riichi_hai_pos: int | None = None

players_dict: dict[int, 'Player'] = {}

class Player:
    def __init__(self, ID: int, name: str, tensuu: int, menfon: int):
        if menfon not in support.fonwei_tuple:
            raise ValueError(f"Unknown menfon: {menfon}")

        self.ID = ID # 0,1,2,(3)
        self.name = name
        self.tensuu: int = tensuu
        self.menfon: int = menfon # tokens.ton, tokens.nan, tokens.shaa, tokens.pei
        self.tehai: Tehai = Tehai([])
        self.river: River = River()

        self.tsumo_pai: Pai | None = None
        self.ron_temp_pai: Pai | None = None

        self.riichi_junme: bool | None = None # 打出立直牌後的巡目
        self.player_junme: int = 0

        self.doujin_furiten_pais: list[Pai] = []
        self.riichi_furiten_pais: list[Pai] = []
        self.datsu_furiten_pais: list[Pai] = []

        players_dict[menfon] = self

    def __eq__(self, other):
        if not isinstance(other, Player):
            return False
        else:
            return self.ID == other.ID

    def is_menchin(self):
        return all([furo.type == tokens.ankan for furo in self.tehai.furo_list])

    def is_agari(self):
        # 檢查胡牌型
        pai_list: list[Pai] = []
        if self.tsumo_pai is None:
            if self.ron_temp_pai is None:
                return False
            pai_list.append(self.ron_temp_pai)
        else:
            pai_list.append(self.tsumo_pai)
        pai_list += self.tehai.pai_list

        return is_agari(pai_list)

    def is_furiten(self):
        tenpai_list = self.tehai.get_tenpais()
        if not tenpai_list:
            return False
        full_list = self.doujin_furiten_pais + self.riichi_furiten_pais + self.datsu_furiten_pais
        return any(p in full_list for p in tenpai_list)
