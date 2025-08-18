class BaseRules:

    shibarisuu = 1 # 飜縛

    koyaku_enabled = False # 啟用古役

    aotenjyou_enabled = False # 啟用青天井規則

    kuitan_enabled = True # 是否有食斷

    pinfu_ron_fusuu = 30 # 平和榮和符數

    rienfontoitsu_fusuu = 2 # 連風對子符數

    akadora_enabled = True # 啟用紅寶牌

    tobitsuzuku_enabled = False # 啟用擊飛繼續規則

    last_oya_infinitely_renchan_enabled = False # 啟用 all last 可無限連莊規則 (i.e. 末莊在最後一局結束時保持 1 位，並且該局末莊是贏家或者流局有聽牌，則末莊可選擇是否連莊，或直接結束遊戲)

    atamahane_enabled = False # 啟用截胡（頭跳ね）

    is_nagashimankan_hoora = False # 啟用時，流局滿貫計為胡牌，否則為流局

class YoninRules: # 四人規則

    initial_tensuu = 25000 # 玩家起始點數

    least_winner_tensuu = 30000 # 遊戲結束的最低點數門檻 (不含四人東西入 or 四人南北入)

class SanninRules: # 三人規則

    initial_tensuu = 35000 # 玩家起始點數

    least_winner_tensuu = 40000 # 遊戲結束的最低點數門檻 (不含三人東西入 or 三人南北入)


    