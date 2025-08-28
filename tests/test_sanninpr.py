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

class SetUpClass():
    def setUp(self):
        # Create Players
        self.players = [
            Player(0, '東', 35000, support.fonwei_tuple[0]), 
            Player(1, '南', 35000, support.fonwei_tuple[1]), 
            Player(2, '西', 35000, support.fonwei_tuple[2]), 
        ]

        # Create Yama
        self.yama = SanninYama()
        
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

class TestHoora(SetUpClass, unittest.TestCase):
    def testPenukiRinshan(self): # 拔北嶺上開花
        modify_tehai(0, '111m234567s8999p', '4z')
        modify_tehai(1, '99m123499s11p123z')
        modify_tehai(2, '99m147899s11p123z')
        DebugInput.push('[14]') # 拔北
        next_round = self.prround.run()
        modify_tehai(0, None, '8p')
        assert isinstance(next_round, PlayerRound)
        DebugInput.push('[14]') # 自摸
        result = next_round.run()
        assert isinstance(result, RoundResult)
        assert result.tsumo_player_result is not None
        player, agari_result, _ = result.tsumo_player_result
        print(agari_result)

    def testPenukiChyankan(self): # 拔北搶槓
        BaseRules.koyaku_enabled = True
        modify_tehai(0, '111m234567s8999p', '4z')
        modify_tehai(1, '1122334556677z')
        modify_tehai(2, '1122334556677z')
        DebugInput.push('[14]', '[0, 0]') # 拔北、搶槓
        result = self.prround.run()
        assert isinstance(result, RoundResult)
        assert result.ron_players_results is not None
        for player, agari_result, _ in result.ron_players_results:
            print(player, agari_result, sep='\n')

if __name__ == '__main__':
    unittest.main()