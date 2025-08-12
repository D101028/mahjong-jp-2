class BaseRules:

    shibarisuu = 1 # 飜縛

    is_koyaku = False # 是否包含古役

    is_aotenjyou = False # 是否使用青天井規則

    is_kuitan = True # 是否有食斷

    pinfu_ron_fusuu = 30 # 平和榮和符數

    rienfontoitsu_fusuu = 2 # 連風對子符數

class CommonRules:

    using_akadora = True # 啟用紅寶牌

    is_tobitsuzuku = False # 是否擊飛繼續

    is_last_oya_infinitely_renchan = False # 是否 all last 可無限連莊 (i.e. 末莊在最後一局結束時保持 1 位，並且該局末莊是贏家或者流局有聽牌，則末莊可選擇是否連莊，或直接結束遊戲)

class YoninRules: # 四人規則

    initial_tensuu = 25000 # 玩家起始點數

    least_winner_tensuu = 30000 # 遊戲結束的最低點數門檻 (不含四人東西入 or 四人南北入)

class SanninRules: # 三人規則

    initial_tensuu = 35000 # 玩家起始點數

    least_winner_tensuu = 40000 # 遊戲結束的最低點數門檻 (不含三人東西入 or 三人南北入)


    