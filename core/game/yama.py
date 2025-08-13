import random
from typing import Iterable

from core.pai import Pai
from core.player import Player, players_dict
from core.ext import support
from core.ext.index import *
from core.ext.rule import CommonRules, YoninRules, SanninRules

class DoraHyouji:
    def __init__(self, hyouji_pai_list: list[Pai]) -> None:
        self.current_hyouji_suu: int = 1
        self.dora_hyouji_list: list[Pai] = []
        self.ura_hyouji_list: list[Pai] = []
        for idx, p in enumerate(reversed(hyouji_pai_list)):
            if idx % 2:
                self.dora_hyouji_list.append(p)
            else:
                self.ura_hyouji_list.append(p)
    
    def get_dora_hyoujis(self) -> list[Pai]:
        return self.dora_hyouji_list[:self.current_hyouji_suu]
    
    def get_ura_hyoujis(self) -> list[Pai]:
        return self.ura_hyouji_list[:self.ura_hyouji_list]

    def flop(self) -> Pai:
        if self.current_hyouji_suu + 1 >= len(self.dora_hyouji_list):
            raise Exception("there is no more dora_hyoujihai can be flopped")
        self.current_hyouji_suu += 1
        return self.dora_hyouji_list[self.current_hyouji_suu - 1]

class YamaChain:
    def __init__(self, pai_index_list: Iterable[str], rinshansuu: int, dora_hyoujisuu: int) -> None:
        if rinshansuu % 2 or dora_hyoujisuu % 2:
            raise ValueError("rinshansuu and dora_hyoujisuu must be even")
        chain1 = [Pai(s) for s in pai_index_list]
        random.shuffle(chain1)
        self.initial_chain = chain1 # chain for backup
        
        # chain structure: [*(pais for tehais), first pai, second, ..., first wanpai, ..., first rinshanpai, ...]
        chain = [p.copy() for p in chain1]
        self.normal_list = chain[:-(rinshansuu + dora_hyoujisuu)]
        self.wanpai_list = chain[-(rinshansuu + dora_hyoujisuu):]
        self.rinshan_list = chain[-rinshansuu:]
        self.dora_hyouji = DoraHyouji(self.wanpai_list[:-rinshansuu])
    
    def deal(self, players_dict: dict[int, Player] = players_dict) -> None:
        """發牌"""
        # 按照風位取得 player 順序列表
        players: list[Player] = []
        player_num: int
        for idx, token in enumerate(support.fonwei_tuple):
            player = players_dict.get(token)
            if player is None:
                if idx == len(support.fonwei_tuple) - 1:
                    player_num = len(support.fonwei_tuple) - 1
                    break
                else:
                    raise Exception(f"Could not get some players from players_dict: {players_dict}")
            else:
                players.append(player)
        else:
            player_num = len(support.fonwei_tuple)
        
        # 擷取預計會抓的牌
        pais = self.normal_list[:13 * player_num]
        self.normal_list = self.normal_list[13 * player_num:]

        # 按一般規則抓牌
        for _ in range(3):
            for player in players:
                player.tehai.pai_list += pais[-4:]
                pais = pais[:-4]
        for _ in range(3):
            for player in players:
                player.tehai.pai_list.append(pais.pop())

    def draw(self) -> Pai:
        """摸牌"""
        if self.get_remaining() == 0:
            raise Exception("there is no more remaining card can be drawn")
        return self.normal_list.pop(0)

    def get_remaining(self) -> int:
        """取得剩餘可摸牌數"""
        return len(self.normal_list)

    def flop_dora_hyouji(self) -> Pai:
        """翻一張寶牌指示牌"""
        return self.dora_hyouji.flop()

    def draw_rinshan(self) -> Pai:
        """摸一張領上牌"""
        if len(self.rinshan_list) == 0:
            raise Exception("there is no more rinshanhai can be drawn")
        p = self.rinshan_list.pop()
        self.wanpai_list.pop()
        self.wanpai_list.insert(0, self.normal_list.pop())
        return p

class YoninYama(YamaChain):
    def __init__(self) -> None:
        if CommonRules.akadora_enabled:
            super().__init__(
                PAI_INDEX_WITH_AKADORA, support.yonin_rinshansuu, support.yonin_dora_hyoujisuu
            )
        else:
            super().__init__(
                PAI_INDEX_WITHOUT_AKADORA, support.yonin_rinshansuu, support.yonin_dora_hyoujisuu
            )

class SanninYama(YamaChain):
    def __init__(self) -> None:
        if CommonRules.akadora_enabled:
            super().__init__(
                PAI_INDEX_SANNIN_WITH_AKADORA, support.sannin_rinshansuu, support.sannin_dora_hyoujisuu
            )
        else:
            super().__init__(
                PAI_INDEX_SANNIN_WITHOUT_AKADORA, support.sannin_rinshansuu, support.sannin_dora_hyoujisuu
            )
