"""
「Player Round」定義：玩家當前需要打牌的時候即是 Player Round 的開始，
打出牌後，觸發一連串的事件（如吃碰槓榮和等）。
一個 Player Round 包含了玩家打牌、事件處理（吃碰槓和）、下個玩家摸牌（若可摸）。
"""

from collections import OrderedDict
from itertools import combinations_with_replacement
from typing import Literal, Iterable

from core.ext import tokens, support
from core.ext.rule import BaseRules
from core.game.yama import YoninYama
from core.interface import Intent, Prompt, Interactor
from core.pai import Param, Pai, FuroType, BasicFuro, Minkan, Ankan, Kakan, Tehai, \
                     get_agari_result_list, AgariResult, is_agari, is_tenpai, \
                     get_kuikae_list, strict_pick_pais_with_loose_equal, strict_remove
from core.player import Player, players_dict, id_players_dict, get_ordered_players
from core.types import *

class MotionTokens:
    motion_tsumo_normal: int = 1
    motion_chii: int = 2
    motion_pon: int = 3
    motion_minkan_rinshan: int = 4
    motion_kakan_rinshan: int = 5
    motion_ankan_rinshan: int = 6
    motion_penuki_rinshan: int = 7

class RoundResultTokens:
    tsumo: int = 1
    ron: int = 2
    normal_ryuukyoku: int = 3
    suuhonrenta_ryuukyoku: int = 4
    suukansanra_ryuukyoku: int = 5
    kyuushukyuhai_ryuukyoku: int = 6
    suuchariichi_ryuukyoku: int = 7
    sanchahoo_ryuukyoku: int = 8
    nagashimankan: int = 9

class PlayerRoundParam:
    def __init__(
        self, 
        player_last_motion: int, 
        last_motion_furo: FuroType | None = None
    ) -> None:
        if player_last_motion not in MotionTokens.__dict__.values():
            raise ValueError(f"Invalid player_last_motion: {player_last_motion}")
        self.player_last_motion = player_last_motion
        self.last_motion_furo = last_motion_furo

class RoundResult:
    def __init__(
        self, 
        type_: int, 
        tenpai_players: list[Player] | None = None, 
        nagashimankan_players: list[Player] | None = None, 
        ron_players_results: list[tuple[Player, AgariResult]] | None = None, 
        ron_from_player: Player | None = None, 
        tsumo_player_result: tuple[Player, AgariResult] | None = None, 
        kyuushukyuhai_player: Player | None = None, 
    ) -> None:
        if type_ not in RoundResultTokens.__dict__.values():
            raise ValueError(f"Invalid type_: {type_}")
        self.type = type_
        self.nagashimankan_players = nagashimankan_players
        self.tenpai_players = tenpai_players
        self.ron_players_results = ron_players_results
        self.ron_from_player = ron_from_player
        self.tsumo_player_result = tsumo_player_result
        self.kyuushukyuhai_player = kyuushukyuhai_player
    
    def __str__(self) -> str:
        return f'<RoundResult type={self.type}>'

def is_included(iter1: Iterable[SupportsEqual], iter2: Iterable[SupportsEqual]) -> bool:
    """return True if iter1 is included in iter2"""
    l2 = list(iter2)
    for p1 in iter1:
        for idx, p2 in enumerate(l2):
            if p2.equal(p1):
                l2.pop(idx)
                break
        else:
            return False
    return True

def get_same_pais_comb_list(pai_list: list[Pai], pai: Pai, count: int) -> list[tuple[Pai, ...]]:
    """回傳區別紅寶牌的組合列表"""
    available_list: list[Pai] = []
    available_strict_list: list[Pai] = []
    for p in pai_list:
        if p == pai:
            available_list.append(p)
            if all((not p.equal(p2)) for p2 in available_strict_list):
                available_strict_list.append(p)
    if not available_list:
        return []
    comb_list = list(combinations_with_replacement(available_strict_list, count))
    remove_idx_list: list[int] = []
    for idx, comb in enumerate(comb_list):
        if not is_included(comb, available_list):
            remove_idx_list.append(idx)
    for idx in reversed(remove_idx_list):
        comb_list.pop(idx)
    return comb_list

class YoninPlayerRound:
    def __init__(self, player: Player, yama: YoninYama, chanfon: int, prparam: PlayerRoundParam) -> None:
        self.player = player
        self.yama = yama
        self.chanfon = chanfon
        self.prparam = prparam
    
    def draw(self, player: Player) -> Pai:
        pai = player.draw(self.yama)
        Interactor([Prompt(player, Intent('no-response', 'player-tehai-update-notation', {
            'tehai-info': player.tehai.to_dict()
        }))]).communicate()
        return pai

    def draw_rinshan(self, player: Player) -> Pai:
        rinshan_pai = self.yama.draw_rinshan()
        player.tehai.new_pai = rinshan_pai
        Interactor([Prompt(player, Intent('no-response', 'player-tehai-update-notation', {
            'tehai-info': player.tehai.to_dict()
        }))]).communicate()
        return rinshan_pai
    
    def flop_dora_hyouji(self) -> Pai:
        pai = self.yama.flop_dora_hyouji()
        Interactor([Prompt(player, Intent('no-response', 'hyoujihai-update-notation', {
            'hyoujihai-info': self.yama.dora_hyouji.to_dict()
        })) for player in players_dict.values()]).communicate()
        return pai

    def ask_and_datsuhai(self, kuikae_list: list[Pai] | None = None) -> Pai:
        """詢問 & 打牌，不檢查立直"""
        # 普通打牌
        if kuikae_list is None:
            kuikae_list = []
        choices: list[int | None] = []
        for idx, p in enumerate(self.player.tehai.pai_list):
            if p not in kuikae_list:
                choices.append(idx)
        if self.player.tehai.new_pai is not None and self.player.tehai.new_pai not in kuikae_list:
            choices.append(None)
        if not choices:
            raise Exception("You do not have available tehai to play!")
        ans = Interactor([Prompt(self.player, Intent('standard', 'ask-to-datsuhai', {
            'datsuhai-choices': choices
        }))]).communicate()[0]
        pai = self.player.datsuhai(choices[int(ans)])
        
        # 播送
        Interactor([Prompt(self.player, Intent('no-response', 'player-tehai-update-notation', {
            'tehai-info': self.player.tehai.to_dict()
        }))] + [Prompt(player, Intent('no-response', 'player-datsuhai-notation', {
            "player-id": self.player.ID, 
            "datsuhai": pai.to_dict(), 
            "to-riichi": False
        })) for player in players_dict.values()]).communicate()
        return pai

    def break_junme(self) -> None:
        for player in players_dict.values():
            player.is_junme_broken = True

    def chi(self, player: Player, from_player: Player) -> 'YoninPlayerRound':
        self.break_junme()
        pai = from_player.river.pai_list[-1]
        pre2, pre1, _, next1, next2 = pai.get_near()
        choices: list[tuple[Pai, Pai]] = []
        if pre1 is not None and pre2 is not None:
            pre1_list = strict_pick_pais_with_loose_equal(player.tehai.pai_list, pre1)
            pre2_list = strict_pick_pais_with_loose_equal(player.tehai.pai_list, pre2)
            choices += [(p2, p1) for p2 in pre2_list for p1 in pre1_list]
        if pre1 is not None and next1 is not None:
            pre1_list = strict_pick_pais_with_loose_equal(player.tehai.pai_list, pre1)
            next1_list = strict_pick_pais_with_loose_equal(player.tehai.pai_list, next1)
            choices += [(p1, p2) for p1 in pre1_list for p2 in next1_list]
        if next1 is not None and next2 is not None:
            next1_list = strict_pick_pais_with_loose_equal(player.tehai.pai_list, next1)
            next2_list = strict_pick_pais_with_loose_equal(player.tehai.pai_list, next2)
            choices += [(p1, p2) for p2 in next2_list for p1 in next1_list]
        if choices:
            if len(choices) >= 2:
                # 詢問要哪個組合
                intent = Intent('standard', 'ask-to-choose-minpai-comb-content-type', {
                    'pai-comb-list': [[p.to_dict() for p in t] for t in choices]
                })
                prompt = Prompt(player, intent)
                ans = Interactor([prompt]).communicate()[0]
                choice = choices[int(ans)]
            else:
                choice = choices[0]
            from_player.river.pai_list.pop()
            for p in choice:
                strict_remove(player.tehai.pai_list, p)
            furo = BasicFuro(tokens.shuntsu, choice, pai, from_player.ID)
            player.tehai.furo_list.append(furo)
            prompt1 = Prompt(player, Intent('no-response', 'player-tehai-update-notation', {
                'tehai-info': player.tehai.to_dict()
            }))
            prompts = [prompt1] + [Prompt(plyer, Intent('no-response', 'player-minpai-notation', {
                'player-id': player.ID, 
                'furo-info': furo.to_dict(), 
            })) for plyer in players_dict.values()]
            Interactor(prompts).communicate()
            return YoninPlayerRound(player, self.yama, self.chanfon, PlayerRoundParam(
                MotionTokens.motion_chii, furo
            ))
        else:
            raise Exception(f"You cannot chii here! tehai: {player.tehai}; pai: {pai}")
    
    def pon(self, player: Player, from_player: Player) -> 'YoninPlayerRound':
        self.break_junme()
        pai = from_player.river.pai_list[-1]
        # 取得組合
        choices = get_same_pais_comb_list(player.tehai.pai_list, pai, 2)
        # 選擇組合
        if len(choices) > 1:
            prompt = Prompt(player, Intent('standard', 'ask-to-choose-minpai-comb-content-type', {
                'pai-comb-list': [[p.to_dict() for p in t] for t in choices]
            }))
            ans = Interactor([prompt]).communicate()[0]
            choice = choices[int(ans)]
        else:
            choice = choices[0]
        # 生成副露
        from_player.river.pai_list.pop()
        for p in choice:
            strict_remove(player.tehai.pai_list, p)
        furo = BasicFuro(tokens.koutsu, (choice[0], choice[1]), pai, from_player.ID)
        player.tehai.furo_list.append(furo)
        prompt1 = Prompt(player, Intent('no-response', 'player-tehai-update-notation', {
            'tehai-info': player.tehai.to_dict()
        }))
        prompts = [prompt1] + [Prompt(plyer, Intent('no-response', 'player-minpai-notation', {
            'player-id': player.ID, 
            'furo-info': furo.to_dict(), 
        })) for plyer in players_dict.values()]
        Interactor(prompts).communicate()
        return YoninPlayerRound(player, self.yama, self.chanfon, PlayerRoundParam(
            MotionTokens.motion_pon, furo
        ))
    
    def minkan(self, player: Player, from_player: Player) -> "YoninPlayerRound | RoundResult":
        self.break_junme()
        pai = from_player.river.pai_list[-1]
        
        # 取得組合
        choices = get_same_pais_comb_list(player.tehai.pai_list, pai, 3)
        if not choices:
            raise Exception(f"You cannot minkan here! tehai: {player.tehai}; pai: {pai}")
        
        # 選擇組合
        if len(choices) >= 2:
            prompt = Prompt(player, Intent('standard', 'ask-to-choose-minpai-comb-content-type', {
                'pai-comb-list': [[p.to_dict() for p in t] for t in choices]
            }))
            ans = Interactor([prompt]).communicate()[0]
            choice = choices[int(ans)]
        else:
            choice = choices[0]
        
        # 槓開
        for p in choice:
            strict_remove(player.tehai.pai_list, p)
        furo = Minkan((choice[0], choice[1], choice[2]), pai, from_player.ID)
        player.tehai.furo_list.append(furo)
        prompt1 = Prompt(player, Intent('no-response', 'player-tehai-update-notation', {
            'tehai-info': player.tehai.to_dict()
        }))
        prompts = [prompt1] + [Prompt(plyer, Intent('no-response', 'player-minpai-notation', {
            'player-id': player.ID, 
            'furo-info': furo.to_dict(), 
        })) for plyer in players_dict.values()]
        Interactor(prompts).communicate()
        
        # 若上輪有明加槓，翻指示牌
        if self.prparam.player_last_motion in (MotionTokens.motion_minkan_rinshan, MotionTokens.motion_kakan_rinshan):
            self.flop_dora_hyouji()
        
        # 摸嶺上牌
        self.draw_rinshan(player)
        return YoninPlayerRound(player, self.yama, self.chanfon, PlayerRoundParam(
            MotionTokens.motion_minkan_rinshan, furo
        ))
    
    def ron(self, players_args: list[tuple[Player, Param]], from_player: Player, agari_pai: Pai) -> RoundResult:
        ron_players_results: list[tuple[Player, AgariResult]] = []
        for player, param in players_args:
            agari_results = get_agari_result_list(player.tehai, agari_pai, param)
            if not agari_results:
                raise Exception(f"The player {player} is not agari!")
            ron_players_results.append((player, max(agari_results, key=lambda result: result.all_tensuu)))
        return RoundResult(
            RoundResultTokens.ron, 
            ron_players_results=ron_players_results, 
            ron_from_player=from_player
        )

    def kakan(self) -> "YoninPlayerRound | RoundResult":
        self.break_junme()
        player = self.player
        pai = player.tehai.new_pai
        if pai is None:
            raise Exception("Missing new_pai in tehai")
        
        # 取得所有符合的副露
        available_pos_list: list[int] = []
        available_list: list[BasicFuro] = []
        for idx, furo in enumerate(player.tehai.furo_list):
            if isinstance(furo, BasicFuro) and furo.type == tokens.koutsu and furo.pai_tuple[0] == pai:
                available_pos_list.append(idx)
                available_list.append(furo)
        if not available_pos_list:
            raise Exception(f"You can't minkan here! tehai: {player.tehai}; pai: {pai}")
        
        # 選擇加槓到的副露
        if len(available_pos_list) >= 2:
            ans = Interactor([Prompt(player, Intent('standard', 'ask-to-choose-minpai-comb-content-type', {
                'pai-comb-list': [[p.to_dict() for p in player.tehai.furo_list[pos].pai_tuple] for pos in available_pos_list]
            }))]).communicate()[0]
            idx = int(ans)
        else:
            idx = 0
        
        # 槓開
        origin_furo = available_list[idx]
        player.tehai.furo_list.pop(available_pos_list[idx])
        furo = Kakan(origin_furo, pai)
        player.tehai.furo_list.append(furo)
        player.tehai.new_pai = None
        Interactor([Prompt(player, Intent('no-response', 'player-tehai-update-notation', {
            'tehai-info': player.tehai.to_dict()
        }))] + [Prompt(plyer, Intent('no-response', 'player-minpai-notation', {
            'player-id': player.ID, 
            'furo-info': furo.to_dict()
        })) for plyer in players_dict.values()]).communicate()
        
        # 檢查搶槓
        ordered_players: list[Player] = get_ordered_players(player)
        chyankan_players: list[Player] = []
        for plyer in ordered_players:
            if plyer.is_able_to_ron(pai, Param(
                plyer.riichi_junme, plyer.player_junme, 'ron', 
                plyer.is_junme_broken, True, self.yama.get_remaining(), 
                plyer.menfon, self.chanfon, False, 
                self.yama.dora_hyouji.get_dora_hyoujis(), self.yama.dora_hyouji.get_ura_hyoujis(), 
                False, False
            )):
                chyankan_players.append(plyer)
        answers = Interactor([Prompt(plyer, Intent('standard', 'ask-to-choices', {
            'choices': ['ron', 'cancel']
        })) for plyer in ordered_players]).communicate()
        ron_players: list[Player] = []
        for idx, ans in enumerate(answers):
            plyer = ordered_players[idx]
            pos = int(ans)
            if pos == 1: # choose 'cancel'
                # 振聽處理
                plyer.doujin_furiten_pais.add(pai) # 同巡振聽
                if plyer.is_riichi:
                    plyer.is_riichi_furiten = True # 立直振聽
            else: # choose 'ron'
                ron_players.append(plyer)
        if ron_players:
            if len(ron_players) == 3 and BaseRules.atamahane_enabled:
                roundresult = RoundResult(RoundResultTokens.sanchahoo_ryuukyoku)
                return roundresult
            if BaseRules.atamahane_enabled:
                ron_players = ron_players[:1]
            players_args: list[tuple[Player, Param]] = []
            for ron_player in ron_players:
                players_args.append((ron_player, Param(
                    ron_player.riichi_junme, ron_player.player_junme, 'ron', 
                    ron_player.is_junme_broken, True, self.yama.get_remaining(), 
                    ron_player.menfon, self.chanfon, False, 
                    self.yama.dora_hyouji.get_dora_hyoujis(), self.yama.dora_hyouji.get_ura_hyoujis(), 
                    False, False
                )))
            return self.ron(players_args, self.player, pai)
        
        # 若上輪有明加槓，翻指示牌
        if self.prparam.player_last_motion in (MotionTokens.motion_minkan_rinshan, MotionTokens.motion_kakan_rinshan):
            self.flop_dora_hyouji()
        
        # 摸嶺上牌
        self.draw_rinshan(player)
        return YoninPlayerRound(player, self.yama, self.chanfon, PlayerRoundParam(
            MotionTokens.motion_kakan_rinshan, furo
        ))

    def ankan(self) -> "YoninPlayerRound | RoundResult":
        self.break_junme()
        player = self.player
        pai = player.tehai.new_pai
        if pai is None:
            raise Exception("Missing new_pai in tehai")
        player.tehai.pai_list.append(pai)
        player.tehai.new_pai = None
        
        # 蒐集可以暗槓的牌
        ankan_pai_set: set[Pai] = set()
        for p in player.tehai.pai_list:
            if p in ankan_pai_set:
                continue
            if player.tehai.pai_list.count(p) >= 4:
                ankan_pai_set.add(p)
        if not ankan_pai_set:
            raise Exception(f"You cannot ankan here! tehai: {player.tehai}")
        
        # 取得暗槓哪張牌
        choices: list[tuple[Pai, ...]] = []
        for p in ankan_pai_set:
            choices += get_same_pais_comb_list(player.tehai.pai_list, p, 4)
        if len(choices) >= 2:
            ans = Interactor([Prompt(player, Intent('standard', 'ask-to-choose-minpai-comb-content-type', {
                'pai-comb-list': [[p.to_dict() for p in choice] for choice in choices]
            }))]).communicate()[0]
            choice = choices[ans]
        else:
            choice = choices[0]
        
        # 槓開
        for p in choice:
            strict_remove(player.tehai.pai_list, p)
        furo = Ankan((choice[0], choice[1], choice[2], choice[3]))
        player.tehai.furo_list.append(furo)
        Interactor([Prompt(player, Intent('no-response', 'player-tehai-update-notation', {
            'tehai-info': player.tehai.to_dict()
        }))] + [Prompt(plyer, Intent('no-response', 'player-minpai-notation', {
            'player-id': player.ID, 
            'furo-info': furo.to_dict()
        })) for plyer in players_dict.values()]).communicate()
        
        # 檢查搶暗槓
        if pai.is_yaochuu:
            ordered_players: list[Player] = get_ordered_players(player)
            chyankan_players: list[Player] = []
            for plyer in ordered_players:
                if plyer.is_furiten():
                    continue
                if not plyer.is_menchin() \
                   or any((not p.is_yaochuu) for p in plyer.tehai.pai_list) \
                   or not is_agari(plyer.tehai.pai_list + [pai]):
                    continue
                temp_result_list = get_agari_result_list(plyer.tehai, pai, Param(
                    plyer.riichi_junme, plyer.player_junme, 'ron', 
                    plyer.is_junme_broken, True, self.yama.get_remaining(), 
                    plyer.menfon, self.chanfon, False, 
                    self.yama.dora_hyouji.get_dora_hyoujis(), self.yama.dora_hyouji.get_ura_hyoujis(), 
                    False, False
                ))
                agari_result_list: list[AgariResult] = []
                for result in temp_result_list:
                    if any((yaku.yakutoken in (tokens.kokushimusou, tokens.kokushimusoujuusanmen))
                            for yaku in result.yaku_list):
                        agari_result_list.append(result)
                if agari_result_list:
                    chyankan_players.append(plyer)
            if chyankan_players:
                answers = Interactor([Prompt(plyer, Intent('standard', 'ask-to-choices', {
                    'choices': ['ron', 'cancel']
                })) for plyer in ordered_players]).communicate()
                ron_players: list[Player] = []
                for idx, ans in enumerate(answers):
                    plyer = ordered_players[idx]
                    pos = int(ans)
                    if pos == 1: # choose 'cancel'
                        # 振聽處理
                        plyer.doujin_furiten_pais.add(pai) # 同巡振聽
                        if plyer.is_riichi:
                            plyer.is_riichi_furiten = True # 立直振聽
                    else: # choose 'ron'
                        ron_players.append(plyer)
                if ron_players:
                    if len(ron_players) == 3 and BaseRules.atamahane_enabled:
                        roundresult = RoundResult(RoundResultTokens.sanchahoo_ryuukyoku)
                        return roundresult
                    if BaseRules.atamahane_enabled:
                        ron_players = ron_players[:1]
                    players_args: list[tuple[Player, Param]] = []
                    for ron_player in ron_players:
                        players_args.append((ron_player, Param(
                            ron_player.riichi_junme, ron_player.player_junme, 'ron', 
                            ron_player.is_junme_broken, True, self.yama.get_remaining(), 
                            ron_player.menfon, self.chanfon, False, 
                            self.yama.dora_hyouji.get_dora_hyoujis(), self.yama.dora_hyouji.get_ura_hyoujis(), 
                            False, False
                        )))
                    return self.ron(players_args, self.player, pai) 
        
        # 若上輪有明加槓，翻指示牌
        if self.prparam.player_last_motion in (MotionTokens.motion_minkan_rinshan, MotionTokens.motion_kakan_rinshan):
            self.flop_dora_hyouji()
        
        # 翻指示牌
        self.flop_dora_hyouji()
        
        # 摸嶺上牌
        self.draw_rinshan(player)
        return YoninPlayerRound(player, self.yama, self.chanfon, PlayerRoundParam(
            MotionTokens.motion_ankan_rinshan, furo
        ))

    def tsumo(self, param: Param) -> RoundResult:
        player = self.player
        pai = player.tehai.new_pai
        if pai is None:
            raise Exception(f"Player {player} missing tsumo pai")
        agari_results = get_agari_result_list(player.tehai, pai, param)
        if not agari_results:
            raise Exception(f"The player {player} is not agari!")
        return RoundResult(
            RoundResultTokens.tsumo, 
            tsumo_player_result=(player, max(agari_results, key=lambda result: result.all_tensuu))
        )

    def suukansanra_ryuukyoku_satisfied(self) -> bool:
        if self.prparam.last_motion_furo not in (
            MotionTokens.motion_minkan_rinshan, MotionTokens.motion_ankan_rinshan, MotionTokens.motion_kakan_rinshan
        ):
            return False
        kantsu_count_dict: dict[Player, int] = {}
        for player in players_dict.values():
            count = 0
            for furo in player.tehai.furo_list:
                if isinstance(furo, Minkan | Kakan | Ankan):
                    count += 1
            kantsu_count_dict[player] = count
        if sum([(i == 4) for i in kantsu_count_dict.values()]) == 1:
            # 洽一人四槓 -> 不流局
            return False
        if sum(kantsu_count_dict.values()) >= 4:
            return True
        return False

    def datsuhai_after(self, pai: Pai, is_to_riichi: bool = False) -> "YoninPlayerRound | RoundResult":
        # 判斷四風連打
        if all((plyer.player_junme == 1 and len(plyer.river.pai_list) == 1) for plyer in players_dict.values()) and self.player.menfon == tokens.pei:
            fonpais = tuple(Pai(name) for name in [support.token_yakuhai_painame_dict[t] for t in (tokens.yakuhai_ton, tokens.yakuhai_nan, tokens.yakuhai_shaa, tokens.yakuhai_pei)])
            if pai in fonpais and all(plyer.river.pai_list[0] == pai for plyer in get_ordered_players(self.player)):
                return RoundResult(RoundResultTokens.suuhonrenta_ryuukyoku)
        
        suukansanra_satisfied = self.suukansanra_ryuukyoku_satisfied() # 是否滿足四槓散了 (後面若沒有和就會直接流局)
        next_player = self.player.next()
        
        # 獲取所有玩家的鳴牌/胡牌選項
        ordered_players: list[Player] = get_ordered_players(self.player)
        player_actions_dict: OrderedDict[Player, list[Literal['chi', 'pon', 'minkan', 'ron']]] = OrderedDict(
            [(player, []) for player in ordered_players]
        )
        remaining = self.yama.get_remaining()
        is_last_player_round = remaining == 0
        if not is_last_player_round and not suukansanra_satisfied and next_player.tehai.is_able_to_chi(pai):
            player_actions_dict[next_player].append('chi')
        for player in player_actions_dict:
            if not is_last_player_round and not suukansanra_satisfied:
                if player.tehai.is_able_to_pon(pai):
                    player_actions_dict[player].append('pon')
                if player.tehai.is_able_to_kan(pai):
                    player_actions_dict[player].append('minkan')
            if player.is_able_to_ron(pai, Param(
                player.riichi_junme, player.player_junme, 'ron', player.is_junme_broken, 
                False, remaining, player.menfon, self.chanfon, 
                False, self.yama.dora_hyouji.get_dora_hyoujis(), self.yama.dora_hyouji.get_ura_hyoujis(), 
                self.prparam.player_last_motion in (
                    MotionTokens.motion_minkan_rinshan, 
                    MotionTokens.motion_kakan_rinshan, 
                    MotionTokens.motion_ankan_rinshan
                ), is_to_riichi
            )):
                player_actions_dict[player].append('ron')
        
        # 生成 Prompt
        prompts: list[Prompt] = []
        for player, actions in player_actions_dict.items():
            if 'ron' not in actions:
                # 振聽處理
                player.doujin_furiten_pais.add(pai) # 同巡振聽
            if not actions:
                continue
            intent = Intent('standard', 'ask-to-choices', {
                "choices": [*actions, 'cancel']
            })
            prompt = Prompt(player, intent)
            prompts.append(prompt)
        
        # 播送並執行鳴牌、胡牌
        if prompts:
            interactor = Interactor(prompts)
            answers = interactor.communicate()
            # choose the action with highest priority
            # ron > minkan > pon > chi; 三家和 => 流局 or 截胡規則
            sorted_results: dict[str, list[Player]] = {
                'ron': [], 
                'minkan': [], 
                'pon': [], 
                'chi': []
            }
            for ans, prompt in zip(answers, prompts):
                choice = prompt.intent.content['choices'][int(ans)]
                if choice != 'cancel':
                    if sorted_results.get(choice) is None:
                        raise ValueError(f"Unknown answer to prompt {prompt.to_dict()}: {choice}")
                    sorted_results[choice].append(prompt.target_player)
                # 振聽處理
                if 'ron' in prompt.intent.content['choices'] and choice == 'cancel':
                    # 同巡振聽
                    prompt.target_player.doujin_furiten_pais.add(pai)
                    # 立直振聽
                    if prompt.target_player.is_riichi:
                        prompt.target_player.is_riichi_furiten = True
            
            if sorted_results['ron']:
                players = sorted_results['ron']
                ordered_ron_players = players
                from_player = self.player
                agari_pai = pai
                if len(ordered_ron_players) == 3 and BaseRules.atamahane_enabled:
                    roundresult = RoundResult(RoundResultTokens.sanchahoo_ryuukyoku)
                    return roundresult
                if BaseRules.atamahane_enabled:
                    ordered_ron_players = ordered_ron_players[:1]
                players_args: list[tuple[Player, Param]] = []
                for ron_player in ordered_ron_players:
                    players_args.append((ron_player, Param(
                        ron_player.riichi_junme, ron_player.player_junme, 'ron', 
                        ron_player.is_junme_broken, False, self.yama.get_remaining(), 
                        ron_player.menfon, self.chanfon, False, 
                        self.yama.dora_hyouji.get_dora_hyoujis(), self.yama.dora_hyouji.get_ura_hyoujis(), 
                        False, False
                    )))
                return self.ron(players_args, from_player, agari_pai)
            if sorted_results['minkan']:
                player = sorted_results['minkan'][0]
                return self.minkan(player, self.player)
            if sorted_results['pon']:
                player = sorted_results['pon'][0]
                return self.pon(player, self.player)
            if sorted_results['chi']:
                player = sorted_results['chi'][0]
                return self.chi(player, self.player)
        
        # 流局 or 下一輪
        if suukansanra_satisfied:
            # 四槓散了
            return RoundResult(RoundResultTokens.suukansanra_ryuukyoku)
        elif is_last_player_round:
            # 流滿判斷
            players = ordered_players.copy()
            players.append(self.player)
            removing_set: set[Player] = set()
            ## 移除被鳴牌的玩家
            for player in players_dict.values():
                for furo in player.tehai.furo_list:
                    if isinstance(furo, BasicFuro):
                        removing_set.add(id_players_dict[furo.from_player_id])
                    elif isinstance(furo, Minkan):
                        removing_set.add(id_players_dict[furo.from_player_id])
                    elif isinstance(furo, Kakan):
                        removing_set.add(id_players_dict[furo.koutsu_furo.from_player_id])
            for player in removing_set:
                players.remove(player)
            ## 確認牌河全為么九
            nagashimankan_players: list[Player] = []
            for player in players:
                if all(pai.is_yaochuu for pai in player.river.pai_list):
                    nagashimankan_players.append(player)
            if nagashimankan_players:
                # 流滿
                if BaseRules.atamahane_enabled:
                    return RoundResult(
                        type_=RoundResultTokens.nagashimankan, 
                        nagashimankan_players=[nagashimankan_players[0]]
                    )
                else:
                    return RoundResult(
                        type_=RoundResultTokens.nagashimankan, 
                        nagashimankan_players=nagashimankan_players
                    )
            else:
                # 普通流局
                tenpai_players: list[Player] = []
                for player in players_dict.values():
                    if player.tehai.is_tenpai():
                        tenpai_players.append(player)
                return RoundResult(
                    type_=RoundResultTokens.normal_ryuukyoku, 
                    tenpai_players=tenpai_players
                )
        else:
            self.draw(next_player)
            return YoninPlayerRound(next_player, self.yama, self.chanfon, PlayerRoundParam(
                MotionTokens.motion_tsumo_normal
            ))

    def riichi(self, original_choices: list[Literal['ankan', 'kakan', 'penuki', 'tsumo', 'kyuushukyuhai', 'riichi', 'cancel']]) -> "YoninPlayerRound | RoundResult":
        # riichi
        new_pai = self.player.tehai.new_pai
        if new_pai is None:
            raise Exception("Missing new_pai in tehai")
        new_datsuhai_choices: list[int] = []
        for idx, p in enumerate(self.player.tehai.pai_list):
            if any(p.equal(self.player.tehai.pai_list[pos1]) for pos1 in new_datsuhai_choices):
                continue
            copied_list = self.player.tehai.pai_list.copy() + [new_pai]
            copied_list.pop(idx)
            if is_tenpai(copied_list):
                new_datsuhai_choices.append(idx)
        if is_tenpai(self.player.tehai.pai_list):
            datsuhai_choices = new_datsuhai_choices + [None]
        else:
            datsuhai_choices = new_datsuhai_choices
        ans = Interactor([Prompt(self.player, Intent('standard', 'ask-to-play-riichi-content-type', {
            'datsuhai-choices': datsuhai_choices, 
            'choices': ['cancel']
        }))]).communicate()[0]
        pos1 = int(ans)
        if pos1 >= len(datsuhai_choices):
            return self.ask_and_execute(original_choices)
        else:
            pai = self.player.datsuhai(datsuhai_choices[pos1], to_riichi=True)
            # 播送
            Interactor([Prompt(self.player, Intent('no-response', 'player-tehai-update-notation', {
                'tehai-info': self.player.tehai.to_dict()
            }))] + [Prompt(plyer, Intent('no-response', 'player-datsuhai-notation', {
                'player-id': self.player.ID, 
                'datsuhai': pai.to_dict(), 
                'to-riichi': True
            })) for plyer in players_dict.values()]).communicate()
            return self.datsuhai_after(pai, True)

    def ask_and_execute(self, choices: list[Literal['ankan', 'kakan', 'penuki', 'tsumo', 'kyuushukyuhai', 'riichi', 'cancel']]) -> "YoninPlayerRound | RoundResult":
        datsuhai_choices = [i for i in range(len(self.player.tehai.pai_list))] + [None]
        ans = Interactor([Prompt(self.player, Intent('standard', 'ask-to-datsuhai-or-other-choices', {
            'datsuhai-choices': datsuhai_choices, 
            'other-choices': choices
        }))]).communicate()[0]
        pos = int(ans)
        choice = (datsuhai_choices + choices)[pos]
        if isinstance(choice, str):
            # 執行
            match choice:
                case 'cancel':
                    pai = self.ask_and_datsuhai()
                    return self.datsuhai_after(pai)
                case 'ankan':
                    return self.ankan()
                case 'kakan':
                    return self.kakan()
                case 'kyuushukyuhai':
                    return RoundResult(
                        RoundResultTokens.kyuushukyuhai_ryuukyoku, 
                        kyuushukyuhai_player=self.player
                    )
                case 'tsumo':
                    return self.tsumo(Param(
                        self.player.riichi_junme, self.player.player_junme, 'tsumo', 
                        self.player.is_junme_broken, False, self.yama.get_remaining(), 
                        self.player.menfon, self.chanfon, self.prparam.player_last_motion in (
                            MotionTokens.motion_minkan_rinshan, 
                            MotionTokens.motion_kakan_rinshan, 
                            MotionTokens.motion_ankan_rinshan
                        ), self.yama.dora_hyouji.get_dora_hyoujis(), self.yama.dora_hyouji.get_ura_hyoujis(), 
                        False, False
                    ))
                case 'riichi':
                    return self.riichi(choices)
                case _:
                    raise Exception(f"Unsupported option here: {choice}")
        else:
            # 打牌
            choice = ([i for i in range(len(self.player.tehai.pai_list))] + [None])[pos]
            pai = self.player.datsuhai(choice)
            # 播送
            Interactor([Prompt(self.player, Intent('no-response', 'player-tehai-update-notation', {
                'tehai-info': self.player.tehai.to_dict()
            }))] + [Prompt(plyer, Intent('no-response', 'player-datsuhai-notation', {
                'player-id': self.player.ID, 
                'datsuhai': pai.to_dict(), 
                'to-riichi': False
            })) for plyer in players_dict.values()]).communicate()
            return self.datsuhai_after(pai)

    def run(self) -> "YoninPlayerRound | RoundResult":
        """Run the round and return next round or RoundResult if it's the last player round"""
        last_motion = self.prparam.player_last_motion
        if last_motion in (MotionTokens.motion_chii, MotionTokens.motion_pon):
            if self.prparam.last_motion_furo is None:
                raise Exception("Last motion furo not found")
            if not isinstance(self.prparam.last_motion_furo, BasicFuro):
                raise Exception("Expect a BasicFuro")
            
            # 取得食替
            kuikae_list = get_kuikae_list(self.prparam.last_motion_furo)
            
            # 打牌
            pai = self.ask_and_datsuhai(kuikae_list)
            return self.datsuhai_after(pai)
        elif last_motion in (MotionTokens.motion_tsumo_normal, 
                             MotionTokens.motion_minkan_rinshan, 
                             MotionTokens.motion_kakan_rinshan, 
                             MotionTokens.motion_ankan_rinshan):
            is_rinshan: bool = last_motion in (MotionTokens.motion_minkan_rinshan, 
                                               MotionTokens.motion_kakan_rinshan, 
                                               MotionTokens.motion_ankan_rinshan)
            new_pai = self.player.tehai.new_pai
            if new_pai is None:
                raise Exception("Missing new_pai in tehai")
            full_pai_list: list[Pai] = self.player.tehai.pai_list + [new_pai]
            param = Param(
                self.player.riichi_junme, self.player.player_junme, 'tsumo', 
                self.player.is_junme_broken, False, self.yama.get_remaining(), 
                self.player.menfon, self.chanfon, is_rinshan, 
                self.yama.dora_hyouji.get_dora_hyoujis(), self.yama.dora_hyouji.get_ura_hyoujis(), 
                False, False
            )

            # 判斷/執行 自摸、加槓、暗槓、九種九牌、立直打牌
            choices: list[Literal['ankan', 'kakan', 'penuki', 'tsumo', 'kyuushukyuhai', 'riichi', 'cancel']] = []
            ## 判斷自摸
            if is_agari(full_pai_list):
                if self.player.player_junme == 0 and not self.player.is_junme_broken and support.fonwei_tuple.index(self.player.menfon) == 0:
                    # 東家第一輪，手牌中任意牌皆可做為自摸牌
                    pai_strict_list: list[Pai] = []
                    for p in full_pai_list:
                        if any(p.equal(p1) for p1 in pai_strict_list):
                            continue
                        else:
                            pai_strict_list.append(p)

                    maximum: int | float = -float('inf')
                    max_idx: int | None = None
                    for idx, p in enumerate(pai_strict_list):
                        copied_list = full_pai_list.copy()
                        strict_remove(copied_list, p)
                        tehai = Tehai(copied_list)
                        tehai.new_pai = p
                        result_list = get_agari_result_list(tehai, p, param)
                        if not result_list:
                            continue
                        result = max(result_list, key=lambda result: result.all_tensuu)
                        if result.all_tensuu >= maximum:
                            maximum = result.all_tensuu
                            max_idx = idx
                            self.player.tehai = tehai
                    if max_idx is not None:
                        choices.append('tsumo')
                elif get_agari_result_list(self.player.tehai, new_pai, param):
                    choices.append('tsumo')
            ## 判斷加槓
            if any((furo.pai_tuple[0] in full_pai_list) for furo in self.player.tehai.furo_list if furo.type == tokens.koutsu):
                choices.append('kakan')
            ## 判斷暗槓
            if any(full_pai_list.count(p) >= 4 for p in full_pai_list):
                choices.append('ankan')
            ## 判斷九種九牌
            if self.player.player_junme == 0 and not self.player.is_junme_broken:
                counted_set: set[Pai] = set()
                count = 0
                for p in full_pai_list:
                    if p.is_yaochuu and p not in counted_set:
                        counted_set.add(p)
                        count += 1
                if count >= 9:
                    choices.append('kyuushukyuhai')
            ## 判斷立直
            if self.yama.get_remaining() >= len(players_dict) and self.player.is_able_to_riichi():
                choices.append('riichi')
            ## 詢問/執行
            if choices:
                choices.append('cancel')
                return self.ask_and_execute(choices)

            # 若上輪是明加槓，開指示牌
            if last_motion in (MotionTokens.motion_minkan_rinshan, MotionTokens.motion_kakan_rinshan):
                self.flop_dora_hyouji()

            # 打牌
            pai = self.ask_and_datsuhai()
            return self.datsuhai_after(pai)
        else:
            raise ValueError(f"Invalid token of prparam.player_last_motion: {last_motion}")
    
    def debug_skip(self) -> "YoninPlayerRound | RoundResult":
        """直接摸切(或者打 tehai.pai_list 的最後一張)，並跳過所有玩家選擇，然後下家摸牌或者流局結束"""
        if self.player.tehai.new_pai is None:
            pai = self.player.datsuhai(len(self.player.tehai.pai_list)-1)
        else:
            pai = self.player.datsuhai()
        print(f"Player datsuhai: {pai}")
        next_player = self.player.next()
        
        # 判斷四風連打
        if all((plyer.player_junme == 1 and len(plyer.river.pai_list) == 1) for plyer in players_dict.values()) and self.player.menfon == tokens.pei:
            fonpais = tuple(Pai(name) for name in [support.token_yakuhai_painame_dict[t] for t in (tokens.yakuhai_ton, tokens.yakuhai_nan, tokens.yakuhai_shaa, tokens.yakuhai_pei)])
            if pai in fonpais and all(plyer.river.pai_list[0] == pai for plyer in get_ordered_players(self.player)):
                return RoundResult(RoundResultTokens.suuhonrenta_ryuukyoku)
        
        # 流局 or 下一輪
        if self.suukansanra_ryuukyoku_satisfied():
            # 四槓散了
            return RoundResult(RoundResultTokens.suukansanra_ryuukyoku)
        elif self.yama.get_remaining() == 0:
            # 普通流局
            tenpai_players: list[Player] = []
            for player in players_dict.values():
                if player.tehai.is_tenpai():
                    tenpai_players.append(player)
            return RoundResult(
                type_=RoundResultTokens.normal_ryuukyoku, 
                tenpai_players=tenpai_players
            )
        else:
            self.draw(next_player)
            return YoninPlayerRound(next_player, self.yama, self.chanfon, PlayerRoundParam(
                MotionTokens.motion_tsumo_normal
            ))
