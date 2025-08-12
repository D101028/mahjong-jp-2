from . import tokens

######################### 遊戲規則設定 ##########################
# gametype_tensuu_init_dict = { # 開局點數
#     lang.yonin_ton: 25000,
#     lang.yonin_ton_ikkyoku: 25000,
#     lang.yonin_nan: 25000,
#     lang.sannin_ton: 35000,
#     lang.sannin_ton_ikkyoku: 35000,
#     lang.sannin_nan: 35000
# }

# gametype_tensuu_over_dict = { # 最低結束點數
#     lang.yonin_ton: 30000,
#     lang.yonin_ton_ikkyoku: 30000,
#     lang.yonin_nan: 30000,
#     lang.sannin_ton: 40000,
#     lang.sannin_ton_ikkyoku: 40000,
#     lang.sannin_nan: 40000
# }

# is_tobitsuzuku = False # 是否擊飛繼續

# is_last_oya_infinitely_renchan = False

# shibarisuu = 1 # 飜縛

# is_koyaku = False # 是否包含古役

# is_aotenjyou = False # 是否使用青天井規則

# is_kuitan = True # 是否有食斷

# pinfu_ron_fusuu = 30 # 平和榮和符數

# rienfontoitsu_fusuu = 2 # 連風對子符數

################################################################

#################### 驗證語言字形合法性 #########################

if len({tokens.man, tokens.suo, tokens.pin, tokens.zuu}) != 4 or \
    len({tokens.ton, tokens.nan, tokens.shaa, tokens.pei}) != 4 or \
    len({tokens.yakuhai_ton,
        tokens.yakuhai_nan,
        tokens.yakuhai_shaa,
        tokens.yakuhai_pei,
        tokens.yakuhai_ton_chanfon,
        tokens.yakuhai_nan_chanfon,
        tokens.yakuhai_shaa_chanfon,
        tokens.yakuhai_pei_chanfon,
        tokens.yakuhai_haku,
        tokens.yakuhai_hatsu,
        tokens.yakuhai_chun}) != 11:
    raise ValueError("language error")

################################################################

######################### 基本字形定義 #########################
##### key 不得重複 #####
token_paitype_dict = { # 不得重複 # 不得為數字
    tokens.man: "m",
    tokens.suo: "s",
    tokens.pin: "p", 
    tokens.zuu: "z"
}

paitype_sign_number_dict = {
    "m": 1, "s": 2, "p": 3, "z": 4
}

fonwei_tuple = ( # 不得重複
    tokens.ton, tokens.nan, tokens.shaa, tokens.pei
)

token_yakuhai_painame_dict = {
    tokens.yakuhai_ton: "1z", 
    tokens.yakuhai_nan: "2z", 
    tokens.yakuhai_shaa: "3z", 
    tokens.yakuhai_pei: "4z", 
    tokens.yakuhai_ton_chanfon: "1z", 
    tokens.yakuhai_nan_chanfon: "2z", 
    tokens.yakuhai_shaa_chanfon: "3z", 
    tokens.yakuhai_pei_chanfon: "4z", 
    tokens.yakuhai_haku: "5z", 
    tokens.yakuhai_hatsu: "6z", 
    tokens.yakuhai_chun: "7z"
}

fonwei_token_tsufon_yaku_dict = {
    tokens.ton: tokens.yakuhai_ton, 
    tokens.nan: tokens.yakuhai_nan, 
    tokens.shaa: tokens.yakuhai_shaa, 
    tokens.pei: tokens.yakuhai_pei, 
}

fonwei_token_chanfon_yaku_dict = {
    tokens.ton: tokens.yakuhai_ton_chanfon, 
    tokens.nan: tokens.yakuhai_nan_chanfon, 
    tokens.shaa: tokens.yakuhai_shaa_chanfon, 
    tokens.pei: tokens.yakuhai_pei_chanfon, 
}

######################### 特殊牌組字形 ##########################

yaochuu_paitype_tuple = ("1m", "9m", "1p", "9p", "1s", "9s", "1z", "2z", "3z", "4z", "5z", "6z", "7z")
ryuuiisoopai_paitype_tuple = ("2s", "3s", "4s", "6s", "8s", "6z")
chinroutoupai_paitype_tuple = ("1m", "9m", "1p", "9p", "1s", "9s")
sanyuanpai_paitype_tuple = ("5z", "6z", "7z")
suushiipai_paitype_tuple = ("1z", "2z", "3z", "4z")

################################################################

