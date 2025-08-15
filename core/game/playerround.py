"""
「Player Round」定義：玩家當前需要打牌的時候即是 Player Round 的開始，
打出牌後，觸發一連串的事件（如吃碰槓榮和等）。
一個 Player Round 包含了玩家打牌、事件處理（吃碰槓和）、下個玩家摸牌（若可摸）。
"""

from typing import Union, Literal

from core.pai import Param, Pai, FuroType, BasicFuro, Minkan, Ankan, Kakan, \
                     get_kuikae_list
from core.player import Player, players_dict
from core.game.yama import YoninYama
from core.interface import Intent, Prompt, Interactor

class PRTokens:
    motion_tsumo_normal: int = 1
    motion_chii: int = 2
    motion_pon: int = 3
    motion_minkan_rinshan: int = 4
    motion_kakan_rinshan: int = 5
    motion_ankan_rinshan: int = 6
    motion_penuki_rinshan: int = 7

class PlayerRoundParam:
    def __init__(
        self, 
        player_last_motion: int, 
        last_motion_furo: FuroType | None = None
    ) -> None:
        if player_last_motion not in PRTokens.__dict__.values():
            raise ValueError(f"Invalid player_last_motion: {player_last_motion}")
        self.player_last_motion = player_last_motion
        self.last_motion_furo = last_motion_furo

class RoundResult:
    def __init__(self) -> None:
        pass

class YoninPlayerRound:
    def __init__(self, player: Player, yama: YoninYama, chanfon: int, prparam: PlayerRoundParam) -> None:
        self.player = player
        self.yama = yama
        self.chanfon = chanfon
        self.prparam = prparam
    
    def ask_and_datsuhai(self, kuikae_list: list) -> Pai:
        choices: list[int] = []
        for idx, p in enumerate(self.player.tehai.pai_list):
            if p not in kuikae_list:
                choices.append(idx)
        if not choices:
            raise Exception("You do not have available tehai to play!")
        intent = Intent('standard', 'ask-to-datsuhai', {"datsuhai-choices": choices})
        prompt = Prompt(self.player, intent)
        response = Interactor([prompt]).communicate()[0]
        pai = self.player.datsuhai(choices[int(response)])
        pass # update msg
        return pai

    def datsuhai_after(self, pai: Pai) -> Union['YoninPlayerRound', RoundResult]:
        next_player = self.player.next()
        player_actions_dict: dict[Player, list[Literal["chi", "pon", "minkan", "ron"]]] = {
            player: [] for player in players_dict.values()
        }
        remaining = self.yama.get_remaining()
        is_last_player_round = remaining == 0
        if not is_last_player_round and next_player.tehai.is_able_to_chii(pai):
            player_actions_dict[next_player].append('chi')
        for player in players_dict.values():
            if not is_last_player_round:
                if player.tehai.is_able_to_pon(pai):
                    player_actions_dict[player].append('pon')
                if player.tehai.is_able_to_kan(pai):
                    player_actions_dict[player].append('minkan')
            if player.tehai.is_able_to_ron(pai, Param(
                player.riichi_junme, player.player_junme, 'ron', player.break_junme, 
                False, remaining, player.menfon, self.chanfon, 
                False, self.yama.dora_hyouji.get_dora_hyoujis(), self.yama.dora_hyouji.get_ura_hyoujis()
            )):
                player_actions_dict[player].append('ron')
        prompts: list[Prompt] = []
        for player, actions in player_actions_dict.items():
            if actions:
                intent = Intent('standard', 'ask-to-choices', {
                    "choices": [*actions, 'cancel']
                })
                prompt = Prompt(player, intent)
                prompts.append(prompt)
        if prompts:
            interactor = Interactor(prompts)
            results = interactor.communicate()
            for idx, prompt in enumerate(prompts):
                result = results[idx]
        if is_last_player_round:
            pass # check 流局滿貫
            return RoundResult()
        else:
            next_player.draw(self.yama)
            return YoninPlayerRound(next_player, self.yama, self.chanfon, PlayerRoundParam(
                PRTokens.motion_tsumo_normal
            ))

    def run(self) -> Union['YoninPlayerRound', RoundResult]:
        """Run the round and return next round or None if it's the last player round"""
        last_motion = self.prparam.player_last_motion
        if last_motion in (PRTokens.motion_chii, PRTokens.motion_pon):
            if self.prparam.last_motion_furo is None:
                raise Exception("Last motion furo not found")
            if not isinstance(self.prparam.last_motion_furo, BasicFuro):
                raise Exception("Expect a BasicFuro")
            kuikae_list = get_kuikae_list(self.prparam.last_motion_furo)
            pai = self.ask_and_datsuhai(kuikae_list)
            return self.datsuhai_after(pai)
        elif last_motion in (PRTokens.motion_tsumo_normal, 
                             PRTokens.motion_minkan_rinshan, 
                             PRTokens.motion_kakan_rinshan, 
                             PRTokens.motion_ankan_rinshan):
            pass # Not Yet
            return RoundResult()
        else:
            raise ValueError(f"Invalid token of prparam.player_last_motion: {last_motion}")
        