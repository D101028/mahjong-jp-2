from core.ext import tokens

######################### 基本字形定義 #########################
token_paitype_dict = { # 不得為數字
    tokens.man: "m",
    tokens.suo: "s",
    tokens.pin: "p", 
    tokens.zuu: "z"
}

paitype_sign_number_dict = {
    "m": 1, "s": 2, "p": 3, "z": 4
}

fonwei_tuple = (
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

