
class BaseRule:

    is_tobitsuzuku = False # 是否擊飛繼續

    is_last_oya_infinitely_renchan = False # 是否 all last 可無限連莊 (i.e. 末莊在最後一局結束時保持 1 位，並且該局末莊是贏家或者流局有聽牌，則末莊可選擇是否連莊，或直接結束遊戲)

    shibarisuu = 1 # 飜縛

    is_koyaku = False # 是否包含古役

    is_aotenjyou = False # 是否使用青天井規則

    is_kuitan = True # 是否有食斷

    pinfu_ron_fusuu = 30 # 平和榮和符數

    rienfontoitsu_fusuu = 2 # 連風對子符數
