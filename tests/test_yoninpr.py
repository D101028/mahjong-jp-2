import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from core.ext import support
from core.game import *
from core.interface import *
from core.pai import *
from core.player import *
from tests.support import modify_tehai

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

class SetUpClass():
    def setUp(self):
        # Create Players
        self.players = [
            Player(0, '東', 25000, support.fonwei_tuple[0]), 
            Player(1, '南', 25000, support.fonwei_tuple[1]), 
            Player(2, '西', 25000, support.fonwei_tuple[2]), 
            Player(3, '北', 25000, support.fonwei_tuple[3]), 
        ]

        # Create Yama
        self.yama = YoninYama()
        
        # Deal Cards
        self.yama.deal(players_dict)

        # Send Messages
        Interactor([Prompt(plyer, Intent('no-response', 'player-tehai-update-notation', {
            'tehai-info': plyer.tehai.to_dict()
        })) for plyer in self.players]).communicate()

        # Open The Door
        player = self.players[0]
        player.draw(self.yama)

        # Send Messages
        Interactor([Prompt(player, Intent('no-response', 'player-tehai-update-notation', {
            'tehai-info': player.tehai.to_dict()
        }))]).communicate()

        # Create First PlayerRound
        self.prround: PlayerRound = PlayerRound(
            player, 
            self.yama, 
            support.fonwei_tuple[0], 
            PlayerRoundParam(
                MotionTokens.motion_tsumo_normal
            )
        )

class TestMinpai(SetUpClass, unittest.TestCase):
    # 檢查鳴牌
    
    def testChi(self): # 吃
        modify_tehai(0, '123456789s1234z', '5m')
        modify_tehai(1, '123456s4445566m', None)
        modify_tehai(2, '1112345678999p', None)
        modify_tehai(3, '1112345678999s', None)
        DebugInput.push('[13]', '[0]')
        result = self.prround.run()

    def testPon(self): # 碰
        modify_tehai(0, '123456789s1234z', '5m')
        modify_tehai(1, '123456s4445566m', None)
        modify_tehai(2, '1112345678999p', None)
        modify_tehai(3, '1112345678999s', None)
        DebugInput.push('[13]', '[1]')
        result = self.prround.run()

    def testMinkan(self): # 明槓
        modify_tehai(0, '123456789s1234z', '5m')
        modify_tehai(1, '1112345678s111z', None)
        modify_tehai(2, '1112345678999p', None)
        modify_tehai(3, '1112345678999s', None)
        DebugInput.push('[9]', '[1]')
        result = self.prround.run()

    def testKakan(self): # 加槓、搶槓
        modify_tehai(0, '123456789s1z', '5m', [BasicFuro(
            tokens.koutsu, (Pai('5m'), Pai('5m')), Pai('5m'), 2
        )])
        modify_tehai(1, '1112345678s111z', None)
        modify_tehai(2, '1112345678999p', None)
        modify_tehai(3, '1112346789999m', None)
        DebugInput.push('[11]', '[0]')
        result = self.prround.run()
        assert isinstance(result, RoundResult)
        assert result.ron_players_results is not None
        assert result.ron_from_player is not None
        for player, result, _ in result.ron_players_results:
            print(player, result, sep='\n')

    def testKakan2(self): # 加槓、領上開花
        self.prround.debug_skip().debug_skip().debug_skip().debug_skip() # type: ignore
        modify_tehai(0, '123456789s1z', '5m', [BasicFuro(
            tokens.koutsu, (Pai('5m'), Pai('5m')), Pai('5m'), 2
        )])
        modify_tehai(1, '1112345678s111z', None)
        modify_tehai(2, '1112345678999p', None)
        modify_tehai(3, '1112346789999s', None)
        DebugInput.push('[11]') # 加槓
        next_round = self.prround.run()
        assert isinstance(next_round, PlayerRound)
        modify_tehai(0, '123456789s1z', '1z')
        DebugInput.push('[11]') # 自摸
        result = next_round.run()
        assert isinstance(result, RoundResult)
        assert result.tsumo_player_result is not None
        player, result, _ = result.tsumo_player_result
        print(player, result, sep='\n')

    def testAnkan(self): # 暗槓、取消天和、嶺上開花
        self.yama.dora_hyouji._dora_hyouji_list[1] = Pai('7z')
        modify_tehai(0, '11m12345679s111z', '1z')
        modify_tehai(1, '1145m14s1919810p', None)
        modify_tehai(2, '1145m14s1919810p', None)
        modify_tehai(3, '1145m14s1919810p', None)
        DebugInput.push('[14]') # 暗槓
        next_round = self.prround.run()
        assert isinstance(next_round, PlayerRound)
        modify_tehai(0, None, '8s')
        DebugInput.push('[11]') # 自摸
        result = next_round.run()
        assert isinstance(result, RoundResult)
        assert result.tsumo_player_result is not None
        print('寶牌指示牌：', *self.yama.dora_hyouji.get_dora_hyoujis())
        print(*result.tsumo_player_result, sep='\n')

    def testAnkan2(self): # 暗槓、搶槓
        modify_tehai(0, '111114459s1111z', '2z')
        modify_tehai(1, '19m19s19p1234567z')
        modify_tehai(2, '114514s1919m810p')
        modify_tehai(3, '19m19s19p2234567z')
        DebugInput.push('[14]', '[1]') # 暗槓 1z
        DebugInput.push('[0, 0]') # 兩家搶槓
        result = self.prround.run()
        assert isinstance(result, RoundResult)
        assert result.ron_from_player is not None
        assert result.ron_players_results is not None
        print('放銃：', result.ron_from_player)
        for player, result, _ in result.ron_players_results:
            print(player, result, sep='\n')

    def testAnkan3(self): # 暗槓、搶槓、三家和
        modify_tehai(0, '114514191s1111z', '2z')
        modify_tehai(1, '19m19s19p1234567z')
        modify_tehai(2, '19m19s19p1234567z')
        modify_tehai(3, '19m19s19p2234567z')
        DebugInput.push('[14]', '[1]') # 暗槓 1z
        DebugInput.push('[0, 0, 0]') # 三家和
        result = self.prround.run()
        assert isinstance(result, RoundResult)
        self.assertEqual(result.type, RoundResultTokens.sanchahoo_ryuukyoku)

class TestFuriten(SetUpClass, unittest.TestCase):
    # 檢查振聽

    def testDatsu(self): # 打出振聽
        modify_tehai(0, '1112345678999s', '9s')
        modify_tehai(1, '1133m5s11223344z')
        modify_tehai(2, '33588s11223344p')
        modify_tehai(3, '1133p5s11223344z')
        DebugInput.push('[13]') # 打出 9s
        next_round = self.prround.run()
        assert isinstance(next_round, PlayerRound)
        DebugInput.push('[4]') # 打出 5s
        with self.assertRaises(DebugInputExit) as ms:
            next_round.run()

    def testDoujin(self): # 同巡振聽
        modify_tehai(0, '23678s234p55577m', '1z')
        modify_tehai(1, '1145m14s1919810p')
        modify_tehai(2, '1145m14s1919810p')
        modify_tehai(3, '1145m14s1919810p')
        DebugInput.push('[13]') # 打出 1z
        next_round = self.prround.run()
        assert isinstance(next_round, PlayerRound)
        modify_tehai(1, '1145m14s1919810p', '1z')
        DebugInput.push('[4]') # 打出 1s
        next_round = next_round.run()
        assert isinstance(next_round, PlayerRound)
        modify_tehai(2, '1145m14s1919810p', '1z')
        DebugInput.push('[5]') # 打出 4s
        next_round.run()

    def testRiichi(self): # 立直振聽
        modify_tehai(0, '23678s234p55577m', '1z')
        modify_tehai(1, '1145m14s1919810p')
        modify_tehai(2, '1145m14s1919810p')
        modify_tehai(3, '1145m14s1919810p')
        DebugInput.push('[14]', '[0]') # 立直、打出 1z
        next_round = self.prround.run()
        assert isinstance(next_round, PlayerRound)
        DebugInput.push('[4]', '[1]') # 打出 1s、不和
        next_round = next_round.run()
        assert isinstance(next_round, PlayerRound)
        DebugInput.push('[5]') # 打出 4s
        next_round.run()

class TestHoora(SetUpClass, unittest.TestCase):
    # 檢查和牌/自摸

    def testTsumo(self): # 自摸
        modify_tehai(0, '1111234567899s', '9s')
        DebugInput.push('[14]')
        result = self.prround.run()
        assert isinstance(result, RoundResult)
        assert result.type == RoundResultTokens.tsumo and result.tsumo_player_result is not None
        print(*result.tsumo_player_result) # 天和、純正九蓮寶燈

    def testTsumo1(self): # 天和轉十三面
        modify_tehai(0, '19m19s19p1234566z', '7z')
        DebugInput.push('[14]')
        result = self.prround.run()
        assert isinstance(result, RoundResult)
        assert result.tsumo_player_result is not None
        print(*result.tsumo_player_result, sep='\n')
    
    def testRon(self): # 榮和
        modify_tehai(0, '111234567899m1z', '9s')
        modify_tehai(1, '1112345678999s', None)
        modify_tehai(2, '1112345678999m', None)
        modify_tehai(3, '1112345678999m', None)
        DebugInput.push('[13]', '[3]')
        assert isinstance(self.prround, PlayerRound)
        result = self.prround.run()
        assert isinstance(result, RoundResult)
        assert result.type == 2 and result.ron_players_results is not None
        print("放銃:", result.ron_from_player)
        for player, result, _ in result.ron_players_results:
            print(player, '\n', result) # 純正九蓮
    
    def testRon2(self): # 兩家榮和
        modify_tehai(0, '111234567899p1z', '9m')
        modify_tehai(1, '1112345678999s', None)
        modify_tehai(2, '1112345678999m', None)
        modify_tehai(3, '1112345678999m', None)
        DebugInput.push('[13]', '[2, 2]')
        assert isinstance(self.prround, PlayerRound)
        result = self.prround.run()
        assert isinstance(result, RoundResult)
        assert result.type == 2 and result.ron_players_results is not None
        print("放銃:", result.ron_from_player)
        for player, result, _ in result.ron_players_results:
            print(player, '\n', result) # 純正九蓮

    def testRon3(self): # 三家榮和
        modify_tehai(0, '111234567899p1z', '9m')
        modify_tehai(1, '123456789s11z78m', None)
        modify_tehai(2, '123456789p22z78m', None)
        modify_tehai(3, '1112345678999m', None)
        DebugInput.push('[13]', '[1, 0, 2]') # 打 9m、三家和
        result = self.prround.run()
        assert isinstance(result, RoundResult)
        self.assertEqual(result.type, RoundResultTokens.sanchahoo_ryuukyoku)

    def testTsumo2(self): # 海底
        next_prround = self.prround.debug_skip()
        while self.yama.get_remaining() != 0:
            assert isinstance(next_prround, PlayerRound)
            next_prround = next_prround.debug_skip()
        assert isinstance(next_prround, PlayerRound)
        modify_tehai(1, '111789m222s333p4z', '4z')
        DebugInput.push('[14]')
        result = next_prround.run()
        assert isinstance(result, RoundResult)
        assert result.type == RoundResultTokens.tsumo 
        assert result.tsumo_player_result is not None
        print(*result.tsumo_player_result) # 自摸

    def testNagashimankan(self): # 流滿
        modify_tehai(0, '135579m2468s123z', '1z')
        next_round = self.prround.debug_skip()
        while self.yama.get_remaining() != 0:
            assert isinstance(next_round, PlayerRound)
            if self.players[0].tehai.new_pai is not None:
                modify_tehai(0, None, '1z')
            next_round = next_round.debug_skip()
        assert isinstance(next_round, PlayerRound)
        result = next_round.debug_skip()
        assert isinstance(result, RoundResult)
        self.assertEqual(result.type, RoundResultTokens.nagashimankan)
        assert result.nagashimankan_players is not None
        print(*result.nagashimankan_players)

class TestSekininbarai(SetUpClass, unittest.TestCase):
    # 檢查包牌

    def testDaisangen(self): # 大三元一家包、一家銃
        modify_tehai(0, '123s45p55z', '1z', [
            BasicFuro(tokens.koutsu, (Pai('7z'), Pai('7z')), Pai('7z'), 1), 
            BasicFuro(tokens.koutsu, (Pai('6z'), Pai('6z')), Pai('6z'), 1), 
        ])
        modify_tehai(1, '2468m13579s4455z')
        modify_tehai(2, '2468m13579s3455p')
        modify_tehai(3, '2468m122356679s')
        DebugInput.push('[7]') # 打 1z
        DebugInput.push('[12]') # 打 5z
        DebugInput.push('[0]') # 碰
        next_round = self.prround.run().run() # type: ignore
        assert isinstance(next_round, PlayerRound)
        DebugInput.push('[3]') # 0 打 4p
        next_round = next_round.run()
        assert isinstance(next_round, PlayerRound)
        DebugInput.push('[0]') # 1 打 2m
        next_round = next_round.run()
        assert isinstance(next_round, PlayerRound)
        DebugInput.push('[12]', '[0]') # 2 打 5p and 0 ron
        result = next_round.run()
        assert isinstance(result, RoundResult)
        assert result.ron_players_results is not None and result.ron_players_results is not None
        player, agari_result, sekinin = result.ron_players_results[0]
        print('放銃：', result.ron_from_player)
        print('包牌：', *sekinin[0])
        print(agari_result)

    def testSuukantsu(self): # 大三元四槓子一家包大三元、一家包四槓子、一家銃
        modify_tehai(0, '1m999p', '3z', [
            Ankan((Pai('7z'), Pai('7z'), Pai('7z'), Pai('7z'))), 
            Minkan((Pai('6z'), Pai('6z'), Pai('6z')), Pai('6z'), 3), 
            Minkan((Pai('5z'), Pai('5z'), Pai('5z')), Pai('5z'), 3), 
        ])
        modify_tehai(1, '123456789m1234s')
        modify_tehai(2, '112233456789s9p')
        modify_tehai(3, '12m1234779s3456p')
        DebugInput.push('[4]') # 打 3z
        next_round = self.prround.run()
        assert isinstance(next_round, PlayerRound)
        modify_tehai(1, None, '2z')
        DebugInput.push('[1]') # 1 打 2m
        next_round = next_round.run()
        assert isinstance(next_round, PlayerRound)
        modify_tehai(2, None, '2z')
        DebugInput.push('[12]', '[1]') # 2 打 9p and 0 kan
        next_round = next_round.run()
        assert isinstance(next_round, PlayerRound)
        modify_tehai(0, None, '4z')
        DebugInput.push('[1]') # 0 打 4z
        next_round = next_round.run()
        assert isinstance(next_round, PlayerRound)
        DebugInput.push('[0]', '[0]') # 1 打 1m and 0 ron
        result = next_round.run()
        assert isinstance(result, RoundResult)
        assert result.ron_players_results is not None and result.ron_players_results is not None
        player, agari_result, sekinin = result.ron_players_results[0]
        print('放銃：', result.ron_from_player)
        print('包牌：', *sekinin[0], '|', *sekinin[1])
        print(agari_result)

class TestKoyakuSekininbarai(SetUpClass, unittest.TestCase):
    # 古役包牌
    def testSuurenkoo(self): # 包四連刻
        BaseRules.koyaku_enabled = True
        BaseRules.aotenjyou_enabled = True
        modify_tehai(0, '9s', '8s', [
            Minkan((Pai('1s'), Pai('1s'), Pai('1s')), Pai('1s'), 3), 
            BasicFuro(tokens.koutsu, (Pai('2s'), Pai('2s')), Pai('2s'), 3), 
            BasicFuro(tokens.koutsu, (Pai('4s'), Pai('4s')), Pai('4s'), 3), 
            BasicFuro(tokens.koutsu, (Pai('3s'), Pai('3s')), Pai('3s'), 2), 
        ])
        modify_tehai(1, '13579m24689s123z')
        modify_tehai(2, '13579m24689p123z')
        modify_tehai(3, '13579m24689p123z')
        DebugInput.push('[1]') # 1 打 8s
        next_round = self.prround.run()
        assert isinstance(next_round, PlayerRound)
        DebugInput.push('[9]', '[0]') # 2 打 9s、0 和
        result = next_round.run()
        assert isinstance(result, RoundResult)
        assert result.ron_from_player is not None and result.ron_players_results is not None
        player, agari_result, sekinin = result.ron_players_results[0]
        print(agari_result)
        print(*sekinin[0])

if __name__ == '__main__':
    unittest.main()
