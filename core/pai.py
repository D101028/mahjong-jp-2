"""
「junme」、「巡目」、「巡目破壞」：一巡指玩家從打完一張牌到打出下一張牌之間的過程，
巡目破壞指玩家打出下一張牌之前，有出現會破壞巡目的行為，如任一玩家鳴牌。
「junme」計數：玩家初始 junme 為 0，每打出一張牌會 +1。
"""

from typing import Literal, Iterable, overload

from .ext import support, yaku, tokens
from .ext.index import *
from .ext.rule import BaseRules, EnabledKoyaku
from .ext.yaku import Yaku, token_yaku_dict, token_koyaku_dict
from .types import *

class Pai:
    def __init__(self, arg: str | PaiDictType):
        self._number: int
        self._type: str
        self._is_akadora: bool
        
        if isinstance(arg, dict) and is_same_dict_type(arg, PaiDictType):
            arg = arg["name"]
        
        if not isinstance(arg, str):
            raise TypeError(f"Pai() argument must be a string or PaiDictType like dictionary, not '{type(arg).__name__}'")

        if len(arg) != 2 or \
            not arg[0].isdigit() or \
            arg[1] not in support.token_paitype_dict.values():
            raise ValueError(f"Invalid value for Pai parameter name: {arg}")
        if arg[1] == support.token_paitype_dict[tokens.zuu]:
            num = int(arg[0])
            if num > 7 or num == 0:
                raise ValueError(f"Invalid value for Pai parameter name: {arg}")

        self._number = int(arg[0]) if arg[0] != "0" else 5
        self._type = arg[1]
        self._is_akadora = (arg[0] == "0")

    @property
    def number(self) -> int:
        return self._number
    @property
    def type(self) -> str:
        return self._type
    @property
    def is_akadora(self) -> bool:
        return self._is_akadora
    @property
    def name(self) -> str:
        """return name with akadora info"""
        if self.is_akadora:
            return f"0{self.type}"
        return f"{self.number}{self.type}"
    @property
    def usual_name(self) -> str:
        return f"{self.number}{self.type}"

    @property
    def is_yaochuu(self) -> bool:
        if self._number in (1, 9):
            return True
        if self._type == support.token_paitype_dict[tokens.zuu]:
            return True
        return False

    def __hash__(self) -> int:
        return hash(self.usual_name)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pai | str):
            return False
        if isinstance(other, str):
            other = Pai(other)
        return other.type == self.type and other.number == self.number
    
    def __str__(self) -> str:
        return f"<Pai {self.name}>"

    def equal(self, other: "Pai | str", is_strict: bool = True) -> bool:
        if not isinstance(other, Pai | str):
            raise TypeError(f"other must be a Pai or str, not {type(other).__name__}")
        if isinstance(other, str):
            other = Pai(other)
        if is_strict:
            return self.name == other.name
        return self == other

    def int_sign(self, is_include_akadora = False) -> int:
        # 1~9; 11~19; 21~29; 31~39; 41~47; 00 10 20 (akadora)
        if not is_include_akadora:
            return support.paitype_sign_number_dict[self.type]*10 + self.number
        else:
            return support.paitype_sign_number_dict[self.type]*10 + int(self.name[0])

    @overload
    def next(self, allow_mod: Literal[False] = False) -> "Pai | None":
        ...
    @overload
    def next(self, allow_mod: Literal[True]) -> 'Pai':
        ...
    def next(self, allow_mod = False) -> "Pai | None":
        if self.type == support.token_paitype_dict[tokens.zuu]:
            if self.number >= 7 and not allow_mod:
                return None
            return Pai(f"{self.number + 1}{self.type}" if self.number != 7 else f"1{self.type}")
        else:
            if self.number >= 9 and not allow_mod:
                return None
            return Pai(f"{self.number + 1}{self.type}" if self.number != 9 else f"1{self.type}")
    
    @overload
    def previous(self, allow_mod: Literal[False] = False) -> "Pai | None":
        ...
    @overload
    def previous(self, allow_mod: Literal[True]) -> 'Pai':
        ...
    def previous(self, allow_mod = False) -> "Pai | None":
        if self.type == support.token_paitype_dict[tokens.zuu]:
            if self.number <= 1 and not allow_mod:
                return None
            return Pai(f"{self.number - 1}{self.type}" if self.number != 1 else f"7{self.type}")
        else:
            if self.number <= 1 and not allow_mod:
                return None
            return Pai(f"{self.number - 1}{self.type}" if self.number != 1 else f"9{self.type}")

    @overload
    def get_shuntsu(self, form: Literal['head'] = 'head') -> tuple['Pai', "Pai | None", "Pai | None"]:
        ...
    @overload
    def get_shuntsu(self, form: Literal['middle']) -> tuple["Pai | None", 'Pai', "Pai | None"]:
        ...
    @overload
    def get_shuntsu(self, form: Literal['tail']) -> tuple["Pai | None", "Pai | None", 'Pai']:
        ...
    def get_shuntsu(self, form: Literal['head', 'middle', 'tail'] = 'head') -> tuple["Pai | None", "Pai | None", "Pai | None"]:
        if self.type == support.token_paitype_dict[tokens.zuu]:
            return (self, None, None)
        if form == 'head':
            next1 = self.next()
            if next1 is None:
                return (self, None, None)
            next2 = next1.next()
            return (self, next1, next2)
        elif form == 'middle':
            return (self.previous(), self, self.next())
        elif form == 'tail':
            pre1 = self.previous()
            if pre1 is None:
                return (None, None, self)
            pre2 = pre1.previous()
            return (pre2, pre1, self)

    def get_near(self) -> tuple["Pai | None", "Pai | None", 'Pai', "Pai | None", "Pai | None"]:
        if self.type == support.token_paitype_dict[tokens.zuu]:
            return (None, None, self, None, None)
        pre1: "Pai | None" = self.previous()
        pre2: "Pai | None" = None
        next1: "Pai | None" = self.next()
        next2: "Pai | None" = None
        next1 = self.next()
        if next1 is not None:
            next2 = next1.next()
        if pre1 is not None:
            pre2 = pre1.previous()
        return (pre2, pre1, self, next1, next2)

    def copy(self) -> 'Pai':
        new_pai = Pai(self.name)
        return new_pai

    def normalize(self) -> None:
        """去除紅寶牌資訊"""
        self._is_akadora = False

    def get_normal(self) -> 'Pai':
        """回傳去除紅寶牌資訊的 Pai"""
        new = self.copy()
        new.normalize()
        return new

    def to_akadora(self) -> None:
        """轉換成紅寶牌"""
        if self.number != 5 or self.type == support.token_paitype_dict[tokens.zuu]:
            raise Exception(f"Could not change the pai `{self}` to akadora")
        self._is_akadora = True

    def to_dict(self) -> PaiDictType:
        return {
            "name": self.name
        }

def strict_pick_pais_with_loose_equal(pai_list: list[Pai], pai: Pai) -> list[Pai]:
    result: list[Pai] = []
    for p in pai_list:
        if pai == p and all((not p2.equal(p)) for p2 in result):
            result.append(p)
    return result

def strict_remove(pai_list: list[Pai], pai: Pai) -> None:
    """raise Value error if pai is strictly not in pai_list"""
    for idx, p in enumerate(pai_list):
        if pai.equal(p, True):
            pai_list.pop(idx)
            return 
    else:
        raise ValueError(f"pai: {pai} not found in pai_list")

yaochuu_list = [Pai(p) for p in support.yaochuu_paitype_tuple]
ryuuiisoopai_list = [Pai(p) for p in support.ryuuiisoopai_paitype_tuple]
chinroutoupai_list = [Pai(p) for p in support.chinroutoupai_paitype_tuple]
sanyuanpai_list = [Pai(p) for p in support.sanyuanpai_paitype_tuple]
suushiipai_list = [Pai(p) for p in support.suushiipai_paitype_tuple]
heiiisoopai_list = [Pai(p) for p in support.heiiisoopai_paitype_tuple]
benikujyakupai_list = [Pai(p) for p in support.benikujyakupai_paitype_tuple]

def create_pai_list(name_list: Iterable[str] | str) -> list[Pai]:
    if (not isinstance(name_list, Iterable) and not isinstance(name_list, str)) or \
        (isinstance(name_list, Iterable) and not isinstance(name_list, str) and not all(isinstance(_, str) for _ in name_list)):
        raise TypeError(f"name_list should be Iterable[str] or a str, not '{type(name_list).__name__}'")
    pai_list = []
    if isinstance(name_list, str):
        num_list: list[str] = []
        for i in name_list:
            if i.isdigit():
                num_list.append(i)
            else:
                pai_list += [Pai(n+i) for n in num_list]
                num_list.clear()
    else:
        pai_list = [Pai(i) for i in name_list]
    return pai_list

class Mentsu:
    def __init__(self, type_: int, pai_list: list[Pai]) -> None:
        if type_ not in (tokens.koutsu, tokens.shuntsu):
            raise ValueError(f"Unknown type {type_} for Mentsu")
        self._type = type_ # tokens.koutsu, tokens.shuntsu, (tokens.ankan, tokens.kakan, tokens.minkan only appear in furo)
        self.pai_list = pai_list
    
    @property
    def type(self) -> int:
        return self._type

    def __str__(self) -> str:
        output = "(" + " ".join([str(p.name) for p in self.pai_list]) + ")"
        return f"<Mentsu {output}>"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Mentsu):
            return False
        return self.type == other.type and min(p.int_sign() for p in self.pai_list) == min(p.int_sign() for p in other.pai_list)
    
    def __hash__(self) -> int:
        return f"{self.type}-{min(p.int_sign() for p in self.pai_list)}".__hash__()

    def copy(self) -> 'Mentsu':
        return Mentsu(self.type, [p.copy() for p in self.pai_list])

def get_mentsu(pai_list: list[Pai]) -> Mentsu:
    """生成順子 or 刻子，只能輸入 len(pai_list) 為 3"""
    pai_list = sorted(pai_list, key=lambda p: p.int_sign())
    if pai_list.count(pai_list[0]) == 1:
        return Mentsu(tokens.shuntsu, pai_list)
    else:
        return Mentsu(tokens.koutsu, pai_list)

class Toitsu:
    def __init__(self, pai: Pai | None = None, pai_list: list[Pai] | None = None) -> None:
        self.pai_list: list[Pai]
        if pai is None:
            if pai_list is None:
                raise ValueError("`pai` and `pai_list` could not be None at the same time.")
            else:
                self.pai_list = pai_list
        else:
            self.pai_list = [pai, pai.copy()]
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Toitsu):
            return False
        return self.pai_list[0] == other.pai_list[0]

    def __str__(self) -> str:
        output = "(" + " ".join([str(p.name) for p in self.pai_list]) + ")"
        return f"<Toitsu {output}>"

    def copy(self) -> 'Toitsu':
        return Toitsu(pai_list=[p.copy() for p in self.pai_list])

def to_furo(arg: FuroDictType):
    if not is_same_dict_type(arg, FuroDictType):
        raise ValueError(f'Expect a FuroDictType')
    type_ = arg["type"]
    self_pai_tuple = arg["self-pai-tuple"]
    received_pai = arg["received-pai"]
    from_player_id = arg["from-player-id"]
    self_koutsu_furo = arg["self-koutsu-furo"]
    if type_ in (tokens.koutsu, tokens.shuntsu):
        assert self_pai_tuple is not None and received_pai is not None and from_player_id is not None
        return BasicFuro(type_, (Pai(self_pai_tuple[0]), Pai(self_pai_tuple[1])), Pai(received_pai), from_player_id)
    elif type_ == tokens.minkan:
        assert self_pai_tuple is not None and received_pai is not None and from_player_id is not None
        return Minkan((Pai(self_pai_tuple[0]), Pai(self_pai_tuple[1]), Pai(self_pai_tuple[2])), Pai(received_pai), from_player_id)
    elif type_ == tokens.kakan:
        assert self_koutsu_furo is not None and received_pai is not None
        return Kakan(to_furo(self_koutsu_furo), Pai(received_pai))
    elif type_ == tokens.ankan:
        assert self_pai_tuple is not None
        p1, p2, p3, p4 = self_pai_tuple
        return Ankan((Pai(p1), Pai(p2), Pai(p3), Pai(p4)))
    else:
        raise ValueError(f"Unknown type: {type_}")

class BasicFuro:
    """基本副露：吃、碰形成的副露"""
    def __init__(self, 
                 type_: int, 
                 self_pai_tuple: tuple[Pai, Pai], 
                 received_pai: Pai, 
                 from_player_id: int) -> None:
        if type_ not in (tokens.koutsu, tokens.shuntsu):
            raise ValueError(f"Unknown type {type_} for BasicFuro")
        self._type: int = type_ # token.koutsu, token.shuntsu
        self._self_pai_tuple: tuple[Pai, Pai] = self_pai_tuple
        self._received_pai: Pai = received_pai
        self._from_player_id: int = from_player_id
    
    @property
    def type(self) -> int:
        return self._type
    @property
    def self_pai_tuple(self) -> tuple[Pai, Pai]:
        return self._self_pai_tuple
    @property
    def received_pai(self) -> Pai:
        return self._received_pai
    @property
    def from_player_id(self) -> int:
        return self._from_player_id
    @property
    def pai_tuple(self) -> tuple[Pai, Pai, Pai]:
        return (*self.self_pai_tuple, self.received_pai)

    def to_mentsu(self) -> Mentsu:
        return Mentsu(self.type, [p.copy() for p in self.pai_tuple])
    
    def __str__(self) -> str:
        output = "(" + " ".join([p.name for p in self.pai_tuple]) + ")"
        return f"<Furo {output}>"

    def to_dict(self) -> FuroDictType:
        return {
            "type": self.type, 
            "self-pai-tuple": tuple(pai.to_dict() for pai in self.self_pai_tuple), 
            "received-pai": self.received_pai.to_dict(), 
            "from-player-id": self.from_player_id, 
            "self-koutsu-furo": None
        }

class Minkan:
    def __init__(self, self_pai_tuple: tuple[Pai, Pai, Pai], received_pai: Pai, from_player_id: int) -> None:
        self.type = tokens.minkan
        self.self_pai_tuple = self_pai_tuple
        self.received_pai = received_pai
        self.from_player_id = from_player_id

        self.pai_tuple = (*self.self_pai_tuple, received_pai)
    
    def __str__(self) -> str:
        output = "(" + " ".join([p.name for p in self.pai_tuple]) + ")"
        return f"<Minkan {output}>"

    def to_mentsu(self) -> Mentsu:
        """會丟失紅寶牌等細節資訊"""
        p = self.pai_tuple[0].get_normal()
        return Mentsu(tokens.koutsu, [p, p.copy(), p.copy()])

    def to_dict(self) -> FuroDictType:
        return {
            "type": self.type, 
            "self-pai-tuple": tuple(pai.to_dict() for pai in self.self_pai_tuple), 
            "received-pai": self.received_pai.to_dict(), 
            "from-player-id": self.from_player_id, 
            "self-koutsu-furo": None
        }

class Kakan:
    def __init__(self, koutsu_furo: BasicFuro, received_pai: Pai) -> None:
        self.type = tokens.kakan
        self.koutsu_furo = koutsu_furo
        self.received_pai = received_pai

        self.pai_tuple = (*koutsu_furo.pai_tuple, received_pai)
    
    def __str__(self) -> str:
        output = "(" + " ".join([p.name for p in self.pai_tuple]) + ")"
        return f"<Kakan {output}>"
    
    def to_mentsu(self) -> Mentsu:
        """會丟失紅寶牌等細節資訊"""
        p = self.pai_tuple[0].get_normal()
        return Mentsu(tokens.koutsu, [p, p.copy(), p.copy()])

    def to_dict(self) -> FuroDictType:
        return {
            "type": self.type, 
            "self-pai-tuple": None, 
            "received-pai": self.received_pai.to_dict(), 
            "from-player-id": None, 
            "self-koutsu-furo": self.koutsu_furo.to_dict()
        }
    
class Ankan:
    def __init__(self, self_pai_tuple: tuple[Pai, Pai, Pai, Pai]) -> None:
        self.type = tokens.ankan
        self.self_pai_tuple = self_pai_tuple

        self.pai_tuple = self_pai_tuple
    
    def __str__(self) -> str:
        output = "(" + " ".join([p.name for p in self.pai_tuple]) + ")"
        return f"<Ankan {output}>"

    def to_mentsu(self) -> Mentsu:
        """會丟失紅寶牌等細節資訊"""
        p = self.pai_tuple[0].get_normal()
        return Mentsu(tokens.koutsu, [p, p.copy(), p.copy()])

    def to_dict(self) -> FuroDictType:
        return {
            "type": self.type, 
            "self-pai-tuple": tuple(pai.to_dict() for pai in self.self_pai_tuple), 
            "received-pai": None, 
            "from-player-id": None, 
            "self-koutsu-furo": None
        }
    
FuroType = BasicFuro | Minkan | Kakan | Ankan

def get_kuikae_list(furo: FuroType) -> list[Pai]:
    result: list[Pai] = []
    if not isinstance(furo, BasicFuro):
        return result
    if furo.type == tokens.shuntsu:
        result.append(furo.received_pai)
        p1, p2 = sorted(furo.self_pai_tuple, key=lambda pai: pai.number)
        if p2.number - p1.number == 1:
            pre = p1.previous()
            if pre is not None:
                result.append(pre)
    elif furo.type == tokens.koutsu:
        result.append(furo.received_pai)
    return result

class AgariComb:
    # 不考慮摸到哪張牌，拆分後的胡牌手牌 # 可為 2 5 8 11 14 張牌
    # 會將紅寶牌替換成普通牌，並記錄在 self.akadora_list 裡面
    def __init__(self, 
                 hoora_type: int, 
                 mentsu_list: list[Mentsu] | None = None, 
                 toitsu_list: list[Toitsu] | None = None, 
                 tanhai_list: list[Pai] | None = None, 
                 akadora_list: list[Pai] | None = None) -> None: 
        if mentsu_list is None:
            mentsu_list = []
        if toitsu_list is None:
            toitsu_list = []
        if tanhai_list is None:
            tanhai_list = []
        self.hoora_type: int = hoora_type # such as token.chiitoitsu_agari_type
        self.mentsu_list: list[Mentsu] = mentsu_list
        self.toitsu_list: list[Toitsu] = toitsu_list # len = 1 if not being chiitoitsu and koyaku
        self.tanhai_list: list[Pai] = tanhai_list # only for kokushi if not including koyaku
        
        self.akadora_list: list[Pai]
        if akadora_list is None:
            self.akadora_list = []
            self.extract_akadora()
        else:
            self.akadora_list = akadora_list
    
    def __str__(self) -> str:
        output = ""
        output += f"{tokens.to_lang(self.hoora_type)}: "
        for t in self.toitsu_list:
            output += "(" + ",".join([str(p.name) for p in t.pai_list]) + ")"
        output += " | "
        for m in self.mentsu_list:
            output += "(" + ",".join([str(p.name) for p in m.pai_list]) + ")"
        output += " | "
        output += "(" + ",".join([str(p.name) for p in self.tanhai_list]) + ")"
        return output

    def extract_akadora(self) -> None:
        for m in self.mentsu_list:
            for p in m.pai_list:
                if p.is_akadora:
                    self.akadora_list.append(p.copy())
                    p.normalize()
        for t in self.toitsu_list:
            for p in t.pai_list:
                if p.is_akadora:
                    self.akadora_list.append(p.copy())
                    p.normalize()
        for p in self.tanhai_list:
            if p.is_akadora:
                self.akadora_list.append(p.copy())
                p.normalize()

class TehaiComb:
    # 拆分後的面搭胡牌組合 # 包含所有手牌
    def __init__(self, 
                 tenpai_type: int, 
                 tenpai: Pai, 
                 waiting_comb: list[Pai] | None = None, 
                 toitsu_list: list[Toitsu] | None = None, 
                 mentsu_list: list[Mentsu] | None = None, 
                 furo_list: list[FuroType] | None = None, 
                 tanhai_list: list[Pai] | None = None, 
                 akadora_revise_list: list[Pai] | None = None) -> None:
        if waiting_comb is None:
            waiting_comb = []
        if toitsu_list is None:
            toitsu_list = []
        if mentsu_list is None:
            mentsu_list = []
        if furo_list is None:
            furo_list = []
        if tanhai_list is None:
            tanhai_list = []
        if akadora_revise_list is None:
            akadora_revise_list = []

        self.tenpai_type = tenpai_type # such as tokens.ryanmenmachi
        self.tenpai = tenpai

        self.waiting_comb = waiting_comb # 搭子 or 七對子單面 or 空列表(國士單面聽) or 國士十三面之一
        self.toitsu_list = toitsu_list
        self.mentsu_list = mentsu_list
        self.tanhai_list = tanhai_list # only for kokushi if not including koyaku

        self.furo_list = furo_list

        self.akadora_list = akadora_revise_list

        if self.akadora_list:
            # 將紅寶牌替換回去
            self.revise_akadora(akadora_revise_list)
    
    def __str__(self) -> str:
        output = ""
        output += f"{tokens.to_lang(self.tenpai_type)}："
        for t in self.toitsu_list:
            output += "(" + ",".join([str(p.name) for p in t.pai_list]) + ")"
        output += " | "
        for m in self.mentsu_list:
            output += "(" + ",".join([str(p.name) for p in m.pai_list]) + ")"
        output += " | "
        output += "(" + ",".join([str(p.name) for p in self.tanhai_list]) + ")"
        output += " | "
        for f in self.furo_list:
            output += "(" + ",".join([str(p.name) for p in f.pai_tuple]) + ")"
        output += " | "
        output += "(" + ",".join([str(p.name) for p in self.waiting_comb]) + ")"
        output += f"；聽：{self.tenpai.name}"
        return output

    def revise_akadora(self, revise_list: list[Pai]) -> None:
        list_copy = revise_list.copy()
        for m in self.mentsu_list:
            for p in m.pai_list:
                if p in list_copy:
                    list_copy.remove(p)
                    p.to_akadora()
            if len(list_copy) == 0:
                return
        for t in self.toitsu_list:
            for p in t.pai_list:
                if p in list_copy:
                    list_copy.remove(p)
                    p.to_akadora()
            if len(list_copy) == 0:
                return
        for p in self.waiting_comb:
            if p in list_copy:
                list_copy.remove(p)
                p.to_akadora()
        if len(list_copy) == 0:
            return 
        for p in self.tanhai_list:
            if p in list_copy:
                list_copy.remove(p)
                p.to_akadora()
        
    def all_pais(self) -> list[Pai]:
        output = []
        for m in self.mentsu_list:
            output += m.pai_list
        for t in self.toitsu_list:
            output += t.pai_list
        for f in self.furo_list:
            output += list(f.pai_tuple)
        output += self.tanhai_list
        output += self.waiting_comb
        output.append(self.tenpai)
        return output

def is_agari(pai_list: list[Pai]) -> bool:
    """檢查胡牌型 可傳入 2 5 8 11 14 張"""
    
    all_pai = pai_list.copy()
    all_pai.sort(key=lambda p: p.int_sign())

    # 七對子型 and 是否有對子
    double = []
    for p in all_pai:
        if all_pai.count(p) >= 2 and not p in double:
            double.append(p)
    if len(double) == 0:
        return False 
    if len(double) == 7:
        return True

    # 國士無雙型
    if all(p in all_pai for p in yaochuu_list) and len(pai_list) == 14:
        return True

    # 普通和牌型
    a1 = all_pai.copy()
    a2 = []
    for x in double:
        a1.remove(x)
        a1.remove(x)
        a2.append((x,x))
        for i in range(len(a1) // 3):
            if a1.count(a1[0]) == 3:
                a2.append((a1[0],)*3)
                a1 = a1[3:]
                continue
            a, ap, app = a1[0].get_shuntsu()
            if ap is not None and app is not None and ap in a1 and app in a1:
                a2.append((a, ap, app))
                a1.remove(a)
                a1.remove(ap)
                a1.remove(app)
                continue
            # 重製
            a1 = all_pai.copy()
            a2 = []
            break
        else:
            return True
    
    if BaseRules.koyaku_enabled:
        # 古役

        # 南北戰爭型
        all_pai_temp = all_pai.copy()
        nan_pai = Pai("2"+support.token_paitype_dict[tokens.zuu])
        pei_pai = Pai("4"+support.token_paitype_dict[tokens.zuu])
        if all_pai_temp.count(nan_pai) == 3 and all_pai_temp.count(pei_pai) == 3:
            all_pai_temp.remove(nan_pai)
            all_pai_temp.remove(nan_pai)
            all_pai_temp.remove(nan_pai)
            all_pai_temp.remove(pei_pai)
            all_pai_temp.remove(pei_pai)
            all_pai_temp.remove(pei_pai)
            l = [1,1,1,5,6,6,8,8]
            if l == sorted([pai.number for pai in all_pai_temp]):
                return True

    return False

def is_tenpai(pai_list: list[Pai]) -> bool:
    """檢查是否聽牌 可傳入 1 4 7 10 13 張"""
    for i in INDEX_WITHOUT_AKADORA:
        pai = Pai(i)
        if is_agari(pai_list + [pai]):
            return True
    return False

def create_mentsu_comb_list(pai_list: list[Pai], first_koutsu_deny: bool = False) -> list[list[Mentsu]]:
    """分割去除對子之胡牌組合 可傳入 0 3 6 9 12 張，pai_list 必須已排序"""
    if len(pai_list) == 0:
        return []
    if  pai_list.count(pai_list[0]) < 3 or first_koutsu_deny:
        # 沒刻子拔 or 必須先拔順子
        copied_list = pai_list.copy()
        p, pp, ppp = copied_list[0].get_shuntsu()
        if pp is None or ppp is None or pp not in copied_list or ppp not in copied_list:
            return []
        mentsu = Mentsu(tokens.shuntsu, [p, pp, ppp])
        copied_list.remove(p)
        copied_list.remove(pp)
        copied_list.remove(ppp)
        if not copied_list:
            return [[mentsu]]
        sub_comb = create_mentsu_comb_list(copied_list, first_koutsu_deny)
        if sub_comb:
            return [[mentsu] + l for l in sub_comb]
        else:
            return []
    else:
        result: list[list[Mentsu]] = []
        # 先拔刻子
        copied_list = pai_list.copy()
        p = copied_list[0]
        mentsu = Mentsu(tokens.koutsu, [p, p, p])
        copied_list.pop(0)
        copied_list.pop(0)
        copied_list.pop(0)
        if not copied_list:
            return [[mentsu]]
        sub_comb = create_mentsu_comb_list(copied_list)
        if sub_comb:
            result += [[mentsu] + l for l in sub_comb]

        # 再拔順子
        result += create_mentsu_comb_list(pai_list, True)
        return result

def get_agari_comb_list(pai_list: list[Pai]) -> list[AgariComb]:
    """分割胡牌組合 可傳入 2 5 8 11 14 張"""

    result: list[AgariComb] = []
    all_pai = [p.copy() for p in pai_list]
    all_pai.sort(key = lambda p: p.int_sign())

    # extrack akadora
    akadora_list: list[Pai] = []
    for p in all_pai:
        if p.is_akadora:
            akadora_list.append(p.copy())
            p.normalize()

    # 七對子型
    double: list[Pai]
    double = []
    for p in all_pai:
        if all_pai.count(p) >= 2 and not p in double:
            double.append(p)
    if len(double) == 0:
        return result # 暫無無對子之胡牌型
    if len(double) == 7:
        comb = AgariComb(tokens.chiitoitsu_agari_type, toitsu_list=[Toitsu(p) for p in double], akadora_list=akadora_list)
        result.append(comb)

    # 國士無雙型
    if all(p in all_pai for p in yaochuu_list):
        yaochuu_list_copy = yaochuu_list.copy()
        yaochuu_list_copy.remove(double[0])
        comb = AgariComb(tokens.kokushimusou_agari_type, toitsu_list=[Toitsu(double[0])], tanhai_list=yaochuu_list_copy, akadora_list=akadora_list)
        result.append(comb)
        return result # no other possible type

    # 普通型
    a1 = all_pai.copy()
    # comb_list = []
    for x in double:
        a1.remove(x)
        a1.remove(x)
        if len(a1) == 0:
            comb = AgariComb(tokens.normal_agari_type, [], [Toitsu(pai_list=[x.copy(), x.copy()])], [], akadora_list)
            result.append(comb)
            break
        mentsu_comb_list = create_mentsu_comb_list(a1)
        for comb in mentsu_comb_list:
            comb = AgariComb(tokens.normal_agari_type, comb, [Toitsu(pai_list=[x.copy(), x.copy()])], [], akadora_list=akadora_list)
            result.append(comb)
        # 重製
        a1 = all_pai.copy()

    # 古役
    if BaseRules.koyaku_enabled:
        pass 

    return result

def get_tenpai_list(pai_list: list[Pai]) -> list[Pai]:
    # 可傳入 1 4 7 10 13 張
    result = []
    for i in INDEX_WITHOUT_AKADORA:
        p = Pai(i)
        if pai_list.count(p) == 4: # 已有四張者不計入聽牌
            continue
        if is_agari(pai_list + [p]):
            result.append(p)
    return result

class Tehai:
    def __init__(self, arg: list[Pai] | list[str] | str | TehaiDictType) -> None:
        self.pai_list: list[Pai]
        self.furo_list: list[FuroType] = []
        self.penuki_list: list[Pai] = []
        self.new_pai: Pai | None = None
        
        if isinstance(arg, dict) and is_same_dict_type(arg, TehaiDictType):
            self.pai_list = list(map(Pai, arg["pai-list"]))
            self.furo_list = list(map(to_furo, arg["furo-list"]))
            self.penuki_list = list(map(Pai, arg["penuki-list"]))
            self.new_pai = Pai(arg["new-pai"]) if arg["new-pai"] is not None else None
        elif isinstance(arg, str):
            self.pai_list = create_pai_list(arg)
        elif isinstance(arg, list):
            self.pai_list = [Pai(p) if isinstance(p, str) else p.copy() for p in arg]
        else:
            raise ValueError(f"arg should be a string, list of Pai or string, or TehaiDictType like dictionary, not {type(arg).__name__}")

    def __str__(self) -> str:
        output = " ".join([p.name for p in self.pai_list])
        if self.new_pai:
            output += f" | {self.new_pai.name}"
        else:
            output += " | None"
        if self.furo_list:
            output += " | " + " ".join([f.__str__() for f in self.furo_list])
        if self.penuki_list:
            output += " | " + " ".join([p.name for p in self.penuki_list])
        return output

    def to_dict(self) -> TehaiDictType:
        return {
            "pai-list": [pai.to_dict() for pai in self.pai_list], 
            "furo-list": [furo.to_dict() for furo in self.furo_list], 
            "penuki-list": [pai.to_dict() for pai in self.penuki_list], 
            "new-pai": self.new_pai.to_dict() if self.new_pai is not None else None
        }

    def sort(self) -> None:
        self.pai_list.sort(key = lambda p: p.int_sign())
    
    def is_tenpai(self) -> bool:
        return is_tenpai(self.pai_list)

    def get_tenpais(self) -> list[Pai]:
        return get_tenpai_list(self.pai_list)

    def get_tehai_comb_list(self) -> list[TehaiComb]:
        tenpai_list = self.get_tenpais()
        if len(tenpai_list) == 0: # no ten
            return []

        result = []
        for p in tenpai_list:
            # 分析進 p 的所有面搭組合

            agari_comb_list = get_agari_comb_list(self.pai_list + [p])
            # create tehai combination list
            tehai_comb_list = []
            for agari_comb in agari_comb_list:
                furo_list = self.furo_list.copy()
                toitsu_list = agari_comb.toitsu_list.copy()
                mentsu_list = agari_comb.mentsu_list.copy()
                tanhai_list = agari_comb.tanhai_list.copy()
                if agari_comb.hoora_type == tokens.kokushimusou_agari_type: # 國士型
                    tanhai_list_copy = tanhai_list.copy()
                    if tanhai_list.count(p) == 1: # 國士單面聽
                        tanhai_list_copy.remove(p)
                        tehai_comb_list.append(TehaiComb(tokens.kokushimusoutanmenmachi, 
                                                         p, 
                                                         [], 
                                                         toitsu_list=[t0.copy() for t0 in toitsu_list], 
                                                         tanhai_list=tanhai_list_copy))
                    elif tanhai_list.count(p) == 0: # 國士十三面聽
                        tehai_comb_list.append(TehaiComb(tokens.kokushimusoujuusanmenmachi, 
                                                         p, 
                                                         [agari_comb.toitsu_list[0].pai_list[0].copy()], 
                                                         toitsu_list=[], 
                                                         tanhai_list=tanhai_list))
                elif agari_comb.hoora_type == tokens.chiitoitsu_agari_type: # 七對子型
                    toitsu_list_copy = [t0.copy() for t0 in toitsu_list]
                    toitsu_list_copy.remove(Toitsu(p))
                    tehai_comb_list.append(TehaiComb(tokens.chiitoitsutanmenmachi, 
                                                     p, 
                                                     [p.copy()], 
                                                     toitsu_list_copy, 
                                                     akadora_revise_list=agari_comb.akadora_list))
                elif agari_comb.hoora_type == tokens.normal_agari_type: # 普通型
                    for t in toitsu_list: # 單騎聽
                        if p in t.pai_list:
                            toitsu_list_copy = [t0.copy() for t0 in toitsu_list]
                            toitsu_list_copy.remove(Toitsu(p))
                            tehai_comb_list.append(TehaiComb(tokens.tankimachi, 
                                                             p.copy(), 
                                                             [p.copy()], 
                                                             toitsu_list_copy, 
                                                             [m.copy() for m in agari_comb.mentsu_list], 
                                                             furo_list, 
                                                             akadora_revise_list=agari_comb.akadora_list))
                    dealed_mentsu_list = []
                    for m in mentsu_list: # 邊張、崁張、兩面、雙碰
                        if m in dealed_mentsu_list:
                            continue
                        if p in m.pai_list:
                            mentsu_list_copy = [m0.copy() for m0 in mentsu_list]
                            mentsu_list_copy.remove(m)
                            if m.type == tokens.koutsu: # 雙碰
                                tehai_comb_list.append(TehaiComb(
                                    tokens.soohoomachi, 
                                    p.copy(), 
                                    [p.copy(), p.copy()], 
                                    [p0.copy() for p0 in agari_comb.toitsu_list], 
                                    mentsu_list_copy, 
                                    furo_list, 
                                    akadora_revise_list=agari_comb.akadora_list
                                ))
                            elif m.type == tokens.shuntsu: # 邊張、崁張、兩面
                                sorted_list = sorted(m.pai_list, key=lambda pai: pai.int_sign())
                                pos = sorted_list.index(p)
                                if pos == 0:
                                    if sorted_list[-1].number == 9: # 右半邊張
                                        tehai_comb_list.append(TehaiComb(
                                            tokens.henchoomachi, 
                                            sorted_list[0], 
                                            sorted_list[1:], 
                                            [p0.copy() for p0 in agari_comb.toitsu_list], 
                                            mentsu_list_copy, 
                                            furo_list, 
                                            akadora_revise_list=agari_comb.akadora_list
                                        ))
                                    else: # 兩面
                                        tehai_comb_list.append(TehaiComb(
                                            tokens.ryanmenmachi, 
                                            sorted_list[0], 
                                            sorted_list[1:], 
                                            [p0.copy() for p0 in agari_comb.toitsu_list], 
                                            mentsu_list_copy, 
                                            furo_list, 
                                            akadora_revise_list=agari_comb.akadora_list
                                        ))
                                elif pos == 1: # 崁張
                                    tehai_comb_list.append(TehaiComb(
                                        tokens.kanchoomachi, 
                                        sorted_list[1], 
                                        [sorted_list[0], sorted_list[2]], 
                                        [p0.copy() for p0 in agari_comb.toitsu_list], 
                                        mentsu_list_copy, 
                                        furo_list, 
                                        akadora_revise_list=agari_comb.akadora_list
                                    ))
                                elif pos == 2: 
                                    if sorted_list[0].number == 1: # 左半邊張
                                        tehai_comb_list.append(TehaiComb(
                                            tokens.henchoomachi, 
                                            sorted_list[2], 
                                            sorted_list[:2], 
                                            [p0.copy() for p0 in agari_comb.toitsu_list], 
                                            mentsu_list_copy, 
                                            furo_list, 
                                            akadora_revise_list=agari_comb.akadora_list
                                        ))
                                    else: # 兩面
                                        tehai_comb_list.append(TehaiComb(
                                            tokens.ryanmenmachi, 
                                            sorted_list[2], 
                                            sorted_list[:2], 
                                            [p0.copy() for p0 in agari_comb.toitsu_list], 
                                            mentsu_list_copy, 
                                            furo_list, 
                                            akadora_revise_list=agari_comb.akadora_list
                                        ))
                        dealed_mentsu_list.append(m)
                elif agari_comb.hoora_type == tokens.special_koyaku_agari_type: # 特殊古役型
                    pass 
        
            result += tehai_comb_list
        return result

    def is_able_to_chi(self, pai: Pai) -> bool:
        if pai.type == support.token_paitype_dict[tokens.zuu]:
            return False
        pre2, pre1, _, next1, next2 = pai.get_near()
        if (next1 in self.pai_list and next2 in self.pai_list) or \
           (pre1 in self.pai_list and next1 in self.pai_list) or \
           (pre1 in self.pai_list and pre2 in self.pai_list):
            return True
        return False

    def is_able_to_pon(self, pai: Pai) -> bool:
        if self.pai_list.count(pai) >= 2:
            return True
        return False

    def is_able_to_kan(self, pai: Pai) -> bool:
        if self.pai_list.count(pai) >= 3:
            return True
        return False

    def is_able_to_ron(self, pai: Pai, param: 'Param') -> bool:
        if not is_agari(self.pai_list + [pai]):
            return False
        agari_result_list = get_agari_result_list(self, pai, param)
        return len(agari_result_list) != 0

class Param:
    @overload
    def __init__(self, 
                 riichi_junme: int | None, 
                 agari_junme: int, 
                 agari_type: Literal['ron'], 
                 is_junme_broken: bool, 
                 is_chyankan: Literal[True], 
                 remaining_pai_num: int, 
                 menfon: int, 
                 chanfon: int, 
                 is_rinshankaihou: Literal[False], 
                 dora_pointers: list[Pai], 
                 uradora_pointers: list[Pai] | None, 
                 is_kanhuri: Literal[False], 
                 is_tsubamegaeshi: Literal[False]) -> None:
        ...
    @overload
    def __init__(self, 
                 riichi_junme: int | None, 
                 agari_junme: int, 
                 agari_type: Literal['ron'], 
                 is_junme_broken: bool, 
                 is_chyankan: Literal[False], 
                 remaining_pai_num: int, 
                 menfon: int, 
                 chanfon: int, 
                 is_rinshankaihou: Literal[False], 
                 dora_pointers: list[Pai], 
                 uradora_pointers: list[Pai] | None, 
                 is_kanhuri: bool, 
                 is_tsubamegaeshi: bool) -> None:
        ...
    @overload
    def __init__(self, 
                 riichi_junme: int | None, 
                 agari_junme: int, 
                 agari_type: Literal['tsumo'], 
                 is_junme_broken: bool, 
                 is_chyankan: Literal[False], 
                 remaining_pai_num: int, 
                 menfon: int, 
                 chanfon: int, 
                 is_rinshankaihou: bool, 
                 dora_pointers: list[Pai], 
                 uradora_pointers: list[Pai] | None, 
                 is_kanhuri: Literal[False], 
                 is_tsubamegaeshi: Literal[False]) -> None:
        ...
    def __init__(self, 
                 riichi_junme: int | None, 
                 agari_junme: int, 
                 agari_type: Literal["ron", "tsumo"], 
                 is_junme_broken: bool, 
                 is_chyankan: bool, 
                 remaining_pai_num: int, 
                 menfon: int, 
                 chanfon: int, 
                 is_rinshankaihou: bool, 
                 dora_pointers: list[Pai], 
                 uradora_pointers: list[Pai] | None, 
                 is_kanhuri: bool, 
                 is_tsubamegaeshi: bool) -> None:
        self.riichi_junme = riichi_junme # 打出立直牌後的巡目
        self.agari_junme = agari_junme
        self.agari_type: Literal["ron", "tsumo"] = agari_type
        self.is_junme_broken: bool = is_junme_broken
        self.is_chyankan = is_chyankan
        self.remaining_pai_num = remaining_pai_num
        self.menfon = menfon
        self.chanfon = chanfon
        self.is_rinshankaihou = is_rinshankaihou
        self.dora_pointers = dora_pointers
        self.uradora_pointers = uradora_pointers if uradora_pointers is not None else []
        
        self.is_kanfuri = is_kanhuri # 槓振
        self.is_tsubamegaeshi = is_tsubamegaeshi # 燕返

class Han:
    """將計入最終飜數的飜種 (含役、寶牌)"""
    def __init__(self, yaku_or_token: Yaku | int, is_menchin: bool, dora_hansuu: int | None = None) -> None:
        # self.name: str
        self.token: int
        self.hansuu: int
        if isinstance(yaku_or_token, Yaku): # yaku
            self.token = yaku_or_token.yakutoken
            if yaku_or_token.is_furo_minus and not is_menchin:
                self.hansuu = yaku_or_token.ori_hansuu - 1
            else:
                self.hansuu = yaku_or_token.ori_hansuu
        elif isinstance(yaku_or_token, int): # dora # token.dora, token.akadora, token.uradora
            if dora_hansuu is None:
                raise ValueError('`dora_hansuu` could not be None when name is of type str')
            self.token = yaku_or_token
            self.hansuu = dora_hansuu
        else:
            raise ValueError(f"name type error: {type(yaku_or_token).__name__}")
    
    def __str__(self) -> str:
        return f"<Han {tokens.to_lang(self.token)}：{self.hansuu}飜>"

class AgariResult:
    def __init__(self, 
                 is_yakuman: bool, 
                 tehai_comb: TehaiComb, 
                 yaku_list: list[Yaku], 
                 han_list: list[Han], 
                 hansuu: int, 
                 fusuu: int | None, 
                 basic_tensuu: int, 
                 tensuu: tuple[int] | tuple[int, int], 
                 all_tensuu: int
                 ) -> None:
        self.is_yakuman: bool = is_yakuman
        self.tehai_comb: TehaiComb = tehai_comb
        self.yaku_list: list[Yaku] = yaku_list
        self.han_list: list[Han] = han_list
        self.hansuu: int = hansuu
        self.fusuu: int | None = fusuu
        self.basic_tensuu: int = basic_tensuu
        self.tensuu: tuple[int] | tuple[int, int] = tensuu
        self.all_tensuu: int = all_tensuu

    def __str__(self) -> str:
        return  f"""--------------------------------------------------------
{self.tehai_comb.__str__()}
{"\n".join(h.__str__() for h in self.han_list)}
{f"{self.hansuu}飜 {self.fusuu if not self.fusuu is None else '*'}符"}
{str(self.all_tensuu)}
--------------------------------------------------------"""

def get_agari_result_list(tehai: Tehai, agari_pai: Pai, param: Param) -> list[AgariResult]:
    result: list[AgariResult] = []
    # get tehai comb list
    tehai_comb_list = tehai.get_tehai_comb_list()
    if len(tehai_comb_list) == 0: # no ten
        return result
    available_tehai_comb_list: list[TehaiComb] = []
    for tc in tehai_comb_list:
        if tc.tenpai == agari_pai:
            available_tehai_comb_list.append(tc)

    # 處理每種和牌型
    is_menchin = all(furo.type == tokens.ankan for furo in tehai.furo_list)
    for tc in available_tehai_comb_list:
        # 飜數
        hansum = 0
        han_list = []
        yl = get_yaku_list(tc, param)
        for y in yl:
            han = Han(y, is_menchin)
            han_list.append(han)
            hansum += han.hansuu
        if hansum < BaseRules.shibarisuu: # less than yaku shibari
            continue
        is_yakuman = yl[0].is_yakuman
        if BaseRules.aotenjyou_enabled or not is_yakuman: # calculate dora
            all_pai = tc.all_pais()
            # akadora
            akadora_suu = len(tc.akadora_list)
            if akadora_suu != 0:
                hansum += akadora_suu
                han_list.append(Han(tokens.akadora, is_menchin, akadora_suu))
            # dora
            dora_suu = 0
            for dora_pointer in param.dora_pointers:
                dora = dora_pointer.next(True)
                dora_suu += all_pai.count(dora)
                dora_suu += tehai.penuki_list.count(dora) # penuki
            # (penuki dora)
            if len(tehai.penuki_list) != 0:
                dora_suu += len(tehai.penuki_list)
            if dora_suu != 0:
                hansum += dora_suu
                han_list.append(Han(tokens.dora, is_menchin, dora_suu))
            # uradora
            if param.riichi_junme is not None:
                uradora_suu = 0
                for uradora_pointer in param.uradora_pointers:
                    uradora = uradora_pointer.next(True)
                    uradora_suu += all_pai.count(uradora)
                    uradora_suu += tehai.penuki_list.count(uradora) # penuki
                if uradora_suu > 0:
                    hansum += uradora_suu
                    han_list.append(Han(tokens.uradora, is_menchin, uradora_suu))
        
        # 符數
        fusuu = get_fusuu(yl, tc, param, is_menchin)

        # 點數
        basic_tensuu, tensuu, all_tensuu = get_tensuu(hansum, fusuu, is_yakuman, param)
        
        result.append(AgariResult(is_yakuman, tc, yl, han_list, hansum, fusuu, basic_tensuu, tensuu, all_tensuu))
    return result

def get_fusuu(yaku_list: list[Yaku], tehai_comb: TehaiComb, param: Param, is_menchin: bool) -> int:
    # if not BaseRules.aotenjyou_enabled: # 非青天井則役滿不計符數
    #     if yaku_list[0].is_yakuman: # 役滿以上
    #         return None
    if tehai_comb.tenpai_type == tokens.chiitoitsutanmenmachi: # 七對子
        return 25
    if BaseRules.koyaku_enabled:
        pass 
    if tehai_comb.tenpai_type in (tokens.kokushimusoutanmenmachi, tokens.kokushimusoujuusanmenmachi): # 國士
        return 30
    elif token_yaku_dict[tokens.pinfu] in yaku_list: # 平和
        if param.agari_type == 'tsumo':
            return 20
        else:
            return BaseRules.pinfu_ron_fusuu
    fu = 20
    if is_menchin and param.agari_type == 'ron': # 門前清榮胡加符
        fu += 10
    if param.agari_type == 'tsumo': # 自摸符
        fu += 2
    if tehai_comb.tenpai_type in (tokens.kanchoomachi, tokens.tankimachi, tokens.henchoomachi): # 中洞、邊獨、單騎聽牌
        fu += 2
    # 面子和雀頭加符
    toitsu_pai: Pai = tehai_comb.tenpai if tehai_comb.tenpai_type == tokens.tankimachi else tehai_comb.toitsu_list[0].pai_list[0]
    minkou_pai: list[Pai] = []
    ankou_pai: list[Pai] = []
    minkan_pai: list[Pai] = []
    ankan_pai: list[Pai] = []
    for f in tehai_comb.furo_list:
        if f.type == tokens.koutsu:
            minkou_pai.append(f.pai_tuple[0])
        elif f.type in (tokens.minkan, tokens.kakan):
            minkan_pai.append(f.pai_tuple[0])
        elif f.type == tokens.ankan:
            ankan_pai.append(f.pai_tuple[0])
    for m in tehai_comb.mentsu_list:
        if m.type == tokens.koutsu:
            ankou_pai.append(m.pai_list[0])
    if tehai_comb.tenpai_type == tokens.soohoomachi: # 雙碰聽計刻
        if param.agari_type == 'tsumo':
            ankan_pai.append(tehai_comb.tenpai)
        else: # 榮和計為明刻
            minkan_pai.append(tehai_comb.tenpai)
    yakuhai_tuple = (
        Pai(support.token_yakuhai_painame_dict[support.fonwei_token_tsufon_yaku_dict[param.menfon]]), 
        Pai(support.token_yakuhai_painame_dict[support.fonwei_token_tsufon_yaku_dict[param.chanfon]]), 
        Pai(support.token_yakuhai_painame_dict[tokens.yakuhai_haku]), 
        Pai(support.token_yakuhai_painame_dict[tokens.yakuhai_hatsu]), 
        Pai(support.token_yakuhai_painame_dict[tokens.yakuhai_chun])
    )
    temp = yakuhai_tuple.count(toitsu_pai)
    if temp == 1:
        fu += 2
    elif temp == 2:
        fu += BaseRules.rienfontoitsu_fusuu
    for p in minkou_pai:
        if p in yaochuu_list:
            fu += 4
        else:
            fu += 2
    for p in ankou_pai:
        if p.is_yaochuu:
            fu += 8
        else:
            fu += 4
    for p in minkan_pai:
        if p.is_yaochuu:
            fu += 16
        else:
            fu += 8
    for p in ankan_pai:
        if p.is_yaochuu:
            fu += 32
        else:
            fu += 16

    return round_up(fu, 1)
    
def round_up(n: int, ndigits: int) -> int:
    mod = 10**ndigits
    return (n//mod + (n % mod != 0)) * mod

def get_tensuu(hansuu: int, fusuu: int, is_yakuman: bool, param: Param) -> tuple[int, tuple[int] | tuple[int, int], int]:
    basic_tensuu: int
    if BaseRules.aotenjyou_enabled or hansuu < 3 or (hansuu == 4 and fusuu <= 30) or (hansuu == 3 and fusuu <= 60):
        basic_tensuu = fusuu * 2**(hansuu + 2)
    elif is_yakuman:
        basic_tensuu = 8000 * (hansuu//13)
    elif hansuu >= 3 and hansuu <= 5: # mankan
        basic_tensuu = 2000
    elif hansuu >= 6 and hansuu <= 7: # haneman
        basic_tensuu = 3000
    elif hansuu >= 8 and hansuu <= 10: # baiman
        basic_tensuu = 4000
    elif hansuu >= 11 and hansuu <= 12: # sanbaiman
        basic_tensuu = 6000
    else: # kazoeyakuman
        basic_tensuu = 8000
    
    if param.menfon == support.fonwei_tuple[0]: # 莊
        if param.agari_type == 'tsumo':
            n = round_up(basic_tensuu*2, 2)
            tensuu = (n, )
            all_tensuu = n*3
        else:
            tensuu = (round_up(basic_tensuu*6, 2), )
            all_tensuu = tensuu[0]
    else: # 閒
        if param.agari_type == 'tsumo':
            n1 = round_up(basic_tensuu*2, 2)
            n2 = round_up(basic_tensuu, 2)
            tensuu = (n1, n2)
            all_tensuu = n1 + n2*2
        else:
            tensuu = (round_up(basic_tensuu*4, 2), )
            all_tensuu = tensuu[0]
    return basic_tensuu, tensuu, all_tensuu

def get_yaku_list(tehai_comb: TehaiComb, param: Param) -> list[Yaku]:
    """獲取給定胡牌組合的全役種"""
    
    result: list[Yaku] = []

    all_pai = tehai_comb.all_pais() # may be more than 14 pieces of pais
    all_pai.sort(key = lambda p: p.int_sign())
    
    # 獲取面子、順子、刻子列表(所有槓轉刻)
    mentsu_furo_list = tehai_comb.mentsu_list + [f.to_mentsu() for f in tehai_comb.furo_list] # lost akadora msg
    if tehai_comb.tenpai_type in (tokens.ryanmenmachi, tokens.henchoomachi, tokens.kanchoomachi, tokens.soohoomachi):
        if len(tehai_comb.waiting_comb) != 2:
            raise RuntimeError("length error")
        mentsu_furo_list.append(get_mentsu(tehai_comb.waiting_comb + [tehai_comb.tenpai]))
    shuntsu_list: list[Mentsu] = [] # 所有順子(含副露)
    koutsu_list: list[Mentsu] = [] # 所有刻子(含副露及槓(轉刻)) # lost akadora msg
    for m in mentsu_furo_list:
        if m.type == tokens.shuntsu:
            shuntsu_list.append(m)
        else:
            koutsu_list.append(m)
    # 獲得對子列表(含單騎那對)
    toitsu_list: list[Toitsu] = [] # lost akadora msg
    toitsu_list += tehai_comb.toitsu_list
    if tehai_comb.tenpai_type in (tokens.kokushimusoujuusanmenmachi, tokens.chiitoitsutanmenmachi, tokens.tankimachi):
        toitsu_list.append(Toitsu(tehai_comb.tenpai))
    
    # 是否門清，暗槓計門清
    is_menchin = all(furo.type == tokens.ankan for furo in tehai_comb.furo_list)

    # 立直、雙立直、一發
    if param.riichi_junme is not None:
        if param.riichi_junme == 1:
            result.append(token_yaku_dict[tokens.dabururiichi])
        else:
            result.append(token_yaku_dict[tokens.riichi])
        if not param.is_junme_broken:
            if param.agari_type == 'tsumo' and param.agari_junme == param.riichi_junme: # 一發自摸
                result.append(token_yaku_dict[tokens.ippatsu])
            elif param.agari_type == 'ron' and param.agari_junme == param.riichi_junme: # 一發榮和
                result.append(token_yaku_dict[tokens.ippatsu])

    # 搶槓
    if param.is_chyankan:
        result.append(token_yaku_dict[tokens.chyankan])

    # 海底撈月、河底撈魚
    if param.remaining_pai_num == 0:
        if param.agari_type == 'tsumo':
            result.append(token_yaku_dict[tokens.haiteiraoyue])
        elif param.agari_type == 'ron':
            result.append(token_yaku_dict[tokens.houteiraoyui])
    
    # 斷么九
    if all(not p.is_yaochuu for p in all_pai):
        if not BaseRules.kuitan_enabled and not is_menchin:
            pass 
        else:
            result.append(token_yaku_dict[tokens.tanyaochuu])
        
    # 役牌
    for mentsu in koutsu_list:
        if mentsu.pai_list[0].type == support.token_paitype_dict[tokens.zuu]:
            pai_name = mentsu.pai_list[0].name
            # 三元牌
            if pai_name == support.token_yakuhai_painame_dict[tokens.yakuhai_haku]:
                result.append(token_yaku_dict[tokens.yakuhai_haku])
            elif pai_name == support.token_yakuhai_painame_dict[tokens.yakuhai_hatsu]:
                result.append(token_yaku_dict[tokens.yakuhai_hatsu])
            elif pai_name == support.token_yakuhai_painame_dict[tokens.yakuhai_chun]:
                result.append(token_yaku_dict[tokens.yakuhai_chun])
            # 自風牌
            if support.token_yakuhai_painame_dict[support.fonwei_token_tsufon_yaku_dict[param.menfon]] == pai_name:
                result.append(token_yaku_dict[support.fonwei_token_tsufon_yaku_dict[param.menfon]])
            # 場風牌
            if support.token_yakuhai_painame_dict[support.fonwei_token_chanfon_yaku_dict[param.chanfon]] == pai_name:
                result.append(token_yaku_dict[support.fonwei_token_chanfon_yaku_dict[param.chanfon]])

    # 門清役
    if is_menchin: # 門清
        # 自摸
        if param.agari_type == 'tsumo':
            result.append(token_yaku_dict[tokens.tsumo])

        # 平和
        yakuhai_list = [Pai(p) for p in (support.token_yakuhai_painame_dict[support.fonwei_token_tsufon_yaku_dict[param.menfon]], 
                                         support.token_yakuhai_painame_dict[support.fonwei_token_tsufon_yaku_dict[param.chanfon]], 
                                         support.token_yakuhai_painame_dict[tokens.yakuhai_haku], 
                                         support.token_yakuhai_painame_dict[tokens.yakuhai_hatsu], 
                                         support.token_yakuhai_painame_dict[tokens.yakuhai_chun])]
        if all((
            tehai_comb.tenpai_type == tokens.ryanmenmachi, # 兩面聽
            toitsu_list[0].pai_list[0] not in yakuhai_list, # 無役牌對子
            len(shuntsu_list) == 4 # 四個順子
        )):
            result.append(token_yaku_dict[tokens.pinfu])

        # 一盃口、二盃口
        if len(shuntsu_list) >= 2:
            shuntsu_set = [x for i, x in enumerate(shuntsu_list) if x not in shuntsu_list[:i]]
            peekoosuu = sum([shuntsu_list.count(m) == 2 for m in shuntsu_set])
            if peekoosuu >= 1:
                result.append(token_yaku_dict[tokens.iipeekoo])
            if peekoosuu >= 2:
                result.append(token_yaku_dict[tokens.ryanpeekoo])

        # 四暗刻
        if len(koutsu_list) >= 4:
            if tehai_comb.tenpai_type == tokens.soohoomachi and param.agari_type == 'tsumo':
                result.append(token_yaku_dict[tokens.suuankoo])
            elif tehai_comb.tenpai_type == tokens.tankimachi:
                result.append(token_yaku_dict[tokens.suuankootanki])
 
        # 國士、國士十三
        if tehai_comb.tenpai_type == tokens.kokushimusoutanmenmachi:
            result.append(token_yaku_dict[tokens.kokushimusou])
        elif tehai_comb.tenpai_type == tokens.kokushimusoujuusanmenmachi:
            result.append(token_yaku_dict[tokens.kokushimusoujuusanmen])

        # 九蓮寶燈
        if len(tehai_comb.furo_list) == 0:
            pai_type = all_pai[0].type
            if all(p.type == pai_type for p in all_pai):
                tehai_int_list = [p.number for p in all_pai] # 14
                chuuren_int_list = [1,1,1,2,3,4,5,6,7,8,9,9,9] # 13
                for i in chuuren_int_list:
                    if i in tehai_int_list:
                        tehai_int_list.remove(i)
                    else:
                        break
                else:
                    if tehai_int_list[0] == tehai_comb.tenpai.number: # 純正
                        result.append(token_yaku_dict[tokens.junseichuurenpouton])
                    else:
                        result.append(token_yaku_dict[tokens.chuurenpouton])

    # 嶺上開花
    if param.agari_type == 'tsumo' and param.is_rinshankaihou:
        result.append(token_yaku_dict[tokens.rinshankaihou])

    # 七對子
    if tehai_comb.tenpai_type == tokens.chiitoitsutanmenmachi:
        result.append(token_yaku_dict[tokens.chiitoitsu])

    # 三色同順
    if len(shuntsu_list) >= 3:
        temp_dict = {} # dict[str, list]
        for m in shuntsu_list:
            number_string = "".join(sorted([str(p.number) for p in m.pai_list]))
            pai_type = m.pai_list[0].type
            types = temp_dict.get(number_string)
            if types is not None:
                if pai_type not in types:
                    types.append(pai_type)
            else:
                temp_dict[number_string] = [pai_type]
        for key, value in temp_dict.items():
            if len(value) == 3:
                result.append(token_yaku_dict[tokens.sanshokudoujun])
                break

    # 一氣通貫
    if len(shuntsu_list) >= 3:
        temp_dict = {
            support.token_paitype_dict[tokens.man]: [], 
            support.token_paitype_dict[tokens.suo]: [], 
            support.token_paitype_dict[tokens.pin]: []
        } # dict[str, list[str]]
        for m in shuntsu_list:
            type_ = m.pai_list[0].type
            if type_ is None:
                raise ValueError("pai type here could not be None")
            temp_dict[type_].append("".join(sorted([str(p.number) for p in m.pai_list])))
        for key, value in temp_dict.items():
            if all(s in value for s in ("123", "456", "789")): # type: ignore
                result.append(token_yaku_dict[tokens.ikkitsuukan])
                break

    # 混全、純全
    if all(t.pai_list[0].is_yaochuu for t in toitsu_list):
        if all(any(p.is_yaochuu for p in m.pai_list) for m in mentsu_furo_list):
            if all(t.pai_list[0] in chinroutoupai_list for t in toitsu_list) and all(any(p in chinroutoupai_list for p in m.pai_list) for m in mentsu_furo_list):
                result.append(token_yaku_dict[tokens.junchantaiyaochuu])
            else:
                result.append(token_yaku_dict[tokens.honchantaiyaochuu])

    # 對對和
    if len(koutsu_list) == 4:
        result.append(token_yaku_dict[tokens.toitoihoo])

    # 三暗刻
    if len(koutsu_list) >= 3:
        ankou_ankan_count = 0
        for m in tehai_comb.mentsu_list: # 暗刻
            if m.type == tokens.koutsu:
                ankou_ankan_count += 1
        for f in tehai_comb.furo_list: # 暗槓
            if f.type == tokens.ankan:
                ankou_ankan_count += 1
        if param.agari_type == 'tsumo' and tehai_comb.tenpai_type == tokens.soohoomachi: # 自摸雙碰多一暗刻
            ankou_ankan_count += 1
        if ankou_ankan_count >= 3:
            result.append(token_yaku_dict[tokens.sanankoo])

    # 混老頭、清老頭
    if all(p.is_yaochuu for p in all_pai):
        if all(p in chinroutoupai_list for p in all_pai):
            result.append(token_yaku_dict[tokens.chinroutou])
        elif all(p.type != support.token_paitype_dict[tokens.zuu] for p in all_pai):
            result.append(token_yaku_dict[tokens.honroutou])

    # 三色同刻
    if len(koutsu_list) >= 3:
        temp_dict = {} # dict[int, list]
        for m in koutsu_list:
            n = m.pai_list[0].number
            pai_type = m.pai_list[0].type
            if pai_type == support.token_paitype_dict[tokens.zuu]:
                continue
            if temp_dict.get(n) is not None:
                if pai_type not in temp_dict[n]:
                    temp_dict[n].append(pai_type)
            else:
                temp_dict[n] = [pai_type]
        for key, value in temp_dict.items():
            if len(value) == 3:
                result.append(token_yaku_dict[tokens.sanshokudookoo])
                break

    # 三槓子、四槓子
    if len(tehai_comb.furo_list) >= 3:
        kantsu_number = sum([f.type in (tokens.minkan, tokens.ankan, tokens.kakan) for f in tehai_comb.furo_list])
        if kantsu_number == 4:
            result.append(token_yaku_dict[tokens.sankantsu])
            result.append(token_yaku_dict[tokens.suukantsu])
        elif kantsu_number == 3:
            result.append(token_yaku_dict[tokens.sankantsu])

    # 小三元
    if toitsu_list[0].pai_list[0] in sanyuanpai_list:
        list_copy = sanyuanpai_list.copy()
        list_copy.remove(toitsu_list[0].pai_list[0])
        for m in koutsu_list:
            pai = m.pai_list[0]
            if pai in list_copy:
                list_copy.remove(pai)
        if len(list_copy) == 0:
            result.append(token_yaku_dict[tokens.shousangen])

    # 混一色、清一色、字一色
    type_set = {p.type for p in all_pai}
    if len(type_set) <= 2:
        if support.token_paitype_dict[tokens.zuu] in type_set:
            if len(type_set) == 1: # 字一色
                result.append(token_yaku_dict[tokens.tsuuiisoo])
            else: # 混一色
                result.append(token_yaku_dict[tokens.honiisoo])
        elif len(type_set) == 1: # 清一色
            result.append(token_yaku_dict[tokens.chiniisoo])
    
    # 天地和
    if param.agari_type == 'tsumo' and param.agari_junme == 0 and not param.is_junme_broken:
        # 天和
        if param.menfon == support.fonwei_tuple[0]:
            result.append(token_yaku_dict[tokens.tenhou])
        # 地和
        else:
            result.append(token_yaku_dict[tokens.chiihou])

    # 大三元
    if len(koutsu_list) >= 3:
        sanyuanpai_list_copy = sanyuanpai_list.copy()
        for m in koutsu_list:
            if m.pai_list[0] in sanyuanpai_list_copy:
                sanyuanpai_list_copy.remove(m.pai_list[0])
        if len(sanyuanpai_list_copy) == 0:
            result.append(token_yaku_dict[tokens.daisangen])

    # 小四喜
    if len(koutsu_list) >= 3 and toitsu_list[0].pai_list[0] in suushiipai_list:
        suushiipai_list_copy = suushiipai_list.copy()
        suushiipai_list_copy.remove(toitsu_list[0].pai_list[0])
        for m in koutsu_list:
            if m.pai_list[0] in suushiipai_list_copy:
                suushiipai_list_copy.remove(m.pai_list[0])
        if len(suushiipai_list_copy) == 0:
            result.append(token_yaku_dict[tokens.shousuushii])

    # 綠一色
    if all(p in ryuuiisoopai_list for p in all_pai):
        result.append(token_yaku_dict[tokens.ryuuiisoo])

    # 大四喜
    if len(koutsu_list) >= 4:
        suushiipai_list_copy = suushiipai_list.copy()
        for m in koutsu_list:
            if m.pai_list[0] in suushiipai_list_copy:
                suushiipai_list_copy.remove(m.pai_list[0])
        if len(suushiipai_list_copy) == 0:
            result.append(token_yaku_dict[tokens.daisuushii])

    # 古役
    if BaseRules.koyaku_enabled:
        # 燕返
        if EnabledKoyaku.tsubamegaeshi and param.is_tsubamegaeshi:
            result.append(token_koyaku_dict[tokens.tsubamegaeshi])
        
        # 槓振
        if EnabledKoyaku.kanfuri and param.is_kanfuri:
            result.append(token_koyaku_dict[tokens.kanfuri])
        
        # 十二落抬
        if EnabledKoyaku.shiiaruraotai and sum([furo.type != tokens.ankan for furo in tehai_comb.furo_list]) >= 4:
            result.append(token_koyaku_dict[tokens.shiiaruraotai])
        
        # 小三風
        if EnabledKoyaku.shousanfon and len(toitsu_list) == 1 and toitsu_list[0].pai_list[0] in suushiipai_list and len(koutsu_list) >= 2:
            suushi_set: set[Pai] = set((toitsu_list[0].pai_list[0], ))
            for koutsu in koutsu_list:
                p = koutsu.pai_list[0]
                if p in suushiipai_list:
                    suushi_set.add(p)
            if len(suushi_set) >= 2:
                result.append(token_koyaku_dict[tokens.shousanfon])
        
        # 一堆刻
        if len(koutsu_list) >= 3:
            # 三連刻、四連刻、純正四連刻
            pai_set: set[Pai] = set((k.pai_list[0] for k in koutsu_list))
            sorted_list = sorted(pai_set, key=lambda p: p.int_sign())
            for p in sorted_list[:-2]:
                if p.type == support.token_paitype_dict[tokens.zuu]:
                    continue
                for _ in range(2):
                    p = p.next()
                    if p is None or p not in pai_set:
                        break
                else:
                    if EnabledKoyaku.sanrenkoo:
                        result.append(token_koyaku_dict[tokens.sanrenkoo])
                    p = p.next()
                    if p is not None and p in pai_set:
                        if EnabledKoyaku.suurenkoo:
                            result.append(token_koyaku_dict[tokens.suurenkoo])
                        if tehai_comb.tenpai_type == tokens.soohoomachi and EnabledKoyaku.junseisuurenkoo:
                            result.append(token_koyaku_dict[tokens.junseisuurenkoo])
                    break
        
            # 三風刻
            if EnabledKoyaku.sanfonkoo:
                count = 0
                for p in pai_set:
                    if p in suushiipai_list:
                        count += 1
                if count >= 3:
                    result.append(token_koyaku_dict[tokens.sanfonkoo])
            
            # 跳牌刻 四跳牌刻
            for p in sorted_list[:-2]:
                if p.type == support.token_paitype_dict[tokens.zuu]:
                    continue
                for _ in range(2):
                    p = p.next()
                    if p is None:
                        break
                    p = p.next()
                    if p is None or p not in pai_set:
                        break
                else:
                    if EnabledKoyaku.chyaopaikoo:
                        result.append(token_koyaku_dict[tokens.chyaopaikoo])
                    p = p.next()
                    if p is None:
                        break
                    p = p.next()
                    if p is not None and p in pai_set and EnabledKoyaku.suuchyaopaikoo:
                        result.append(token_koyaku_dict[tokens.suuchyaopaikoo])
                    break

            # 頂三刻
            if EnabledKoyaku.teinsankoo:
                for t in (tokens.man, tokens.suo, tokens.pin):
                    s = support.token_paitype_dict[t]
                    if all((Pai(f'{i}{s}') in pai_set) for i in (1, 5, 9)):
                        result.append(token_koyaku_dict[tokens.teinsankoo])
                        break
            
            # 筋牌刻
            if EnabledKoyaku.chinpaikoo:
                for t in ((1, 4, 7), (2, 5, 8), (3, 6, 9)):
                    if all(
                        (p.type != support.token_paitype_dict[tokens.zuu] \
                        and p.number in t)
                        for p in pai_set
                    ):
                        result.append(token_koyaku_dict[tokens.chinpaikoo])
                        break

        # 五門齊、五族協和
        mens: dict[Literal['man', 'suo', 'pin', 'fon', 'yuan'], bool] = {
            'man': False, 
            'suo': False, 
            'pin': False, 
            'fon': False, 
            'yuan': False
        }
        for p in all_pai:
            match p.type:
                case tokens.man:
                    mens["man"] = True
                case tokens.suo:
                    mens["suo"] = True
                case tokens.pin:
                    mens['pin'] = True
                case _:
                    if 1 <= p.number <= 4:
                        mens["fon"] = True
                    else:
                        mens['yuan'] = True
        if all(mens.values()):
            if EnabledKoyaku.uumensai:
                result.append(token_koyaku_dict[tokens.uumensai])
            if is_menchin and len(koutsu_list) >= 4 and \
               toitsu_list[0].pai_list[0].type == support.token_paitype_dict[tokens.zuu]:
                if EnabledKoyaku.gozokukyouwa:
                    result.append(token_koyaku_dict[tokens.gozokukyouwa])

        # 二暗槓、三暗槓、四暗槓
        ankan_suu = sum(furo.type == tokens.ankan for furo in tehai_comb.furo_list)
        if ankan_suu >= 2:
            if EnabledKoyaku.ryanankan:
                result.append(token_koyaku_dict[tokens.ryanankan])
            if ankan_suu >= 3:
                if EnabledKoyaku.sanankan:
                    result.append(token_koyaku_dict[tokens.sanankan])
                if ankan_suu >= 4 and EnabledKoyaku.suuankan:
                    result.append(token_koyaku_dict[tokens.suuankan])
        
        # 一色三同順、一色四同順
        if len(shuntsu_list) >= 3:
            sorted_list = sorted(shuntsu_list, key=lambda s: min([p.int_sign() for p in s.pai_list]))
            for idx, shuntsu in enumerate(sorted_list[:-2]):
                next1_shuntsu = sorted_list[idx+1]
                next2_shuntsu = sorted_list[idx+2]
                if shuntsu != next1_shuntsu or shuntsu != next2_shuntsu:
                    continue
                if EnabledKoyaku.isshokusanjun:
                    result.append(token_koyaku_dict[tokens.isshokusanjun])
                if idx + 3 >= len(sorted_list):
                    break
                next3_shuntsu = sorted_list[idx+3]
                if shuntsu == next3_shuntsu and EnabledKoyaku.isshokuyonjun:
                    result.append(token_koyaku_dict[tokens.isshokuyonjun])
                break

        # 斷紅和、清斷紅和
        pai_list = ryuuiisoopai_list + heiiisoopai_list + [Pai(support.token_yakuhai_painame_dict[tokens.yakuhai_haku])]
        if all(p in pai_list for p in all_pai):
            if EnabledKoyaku.tanhonhoo:
                result.append(token_koyaku_dict[tokens.tanhonhoo])
            s = support.token_paitype_dict[tokens.zuu]
            if EnabledKoyaku.chitanhonhoo and all(p.type != s for p in pai_list):
                result.append(token_koyaku_dict[tokens.chitanhonhoo])

        # 同順二盃口
        if EnabledKoyaku.ryansuushun and is_menchin and len(shuntsu_list) >= 4:
            shuntsu_set = set(shuntsu_list)
            double_shuntsu_list: list[Mentsu] = []
            for shuntsu in shuntsu_set:
                if shuntsu_list.count(shuntsu) >= 2:
                    double_shuntsu_list.append(shuntsu)
            if len(double_shuntsu_list) >= 2:
                count = 0
                for idx, shuntsu in enumerate(double_shuntsu_list):
                    for shuntsu2 in double_shuntsu_list[idx+1: ]:
                        if min(p.number for p in shuntsu2.pai_list) == min(p.number for p in shuntsu.pai_list):
                            count += 1
                if count >= 2:
                    result.append(token_koyaku_dict[tokens.ryansuushun])

        # 人和
        if EnabledKoyaku.renhou and not param.is_junme_broken and param.agari_junme == 0 and param.agari_type == 'ron':
            result.append(token_koyaku_dict[tokens.renhou])

        # 四槓落抬 (四槓後若嶺上牌沒自摸，則蓋牌胡役滿)
        # 四槓花開 (四槓後且嶺上開花，加上這個共兩倍役滿)

        # 花天月地
        if EnabledKoyaku.katengecchi and param.is_rinshankaihou and param.remaining_pai_num == 0:
            result.append(token_koyaku_dict[tokens.katengecchi])

        # 石上三年
        if EnabledKoyaku.ishiuesannen and param.riichi_junme == 1 and param.remaining_pai_num == 0:
            result.append(token_koyaku_dict[tokens.ishiuesannen])

        # 黑一色
        if EnabledKoyaku.heiiisoo and all((p in heiiisoopai_list) for p in all_pai):
            result.append(token_koyaku_dict[tokens.heiiisoo])
        
        # 紅孔雀
        if EnabledKoyaku.benikujyaku and all((p in benikujyakupai_list) for p in all_pai):
            result.append(token_koyaku_dict[tokens.benikujyaku])

        # 大車輪、大數鄰、大竹林、大七星、純正黑一色
        if tehai_comb.tenpai_type == tokens.chiitoitsutanmenmachi:
            p = toitsu_list[0].pai_list[0]
            type_ = p.type
            if type_ != support.token_paitype_dict[tokens.zuu] and p.number not in (1, 9):
                num_set: set[int] = set()
                num_set.add(p.number)
                for toitsu in toitsu_list[1:]:
                    p = toitsu.pai_list[0]
                    if type_ != p.type or p.number not in (1, 9) or p.number in num_set:
                        break
                    else:
                        num_set.add(p.number)
                else:
                    if type_ == tokens.man and EnabledKoyaku.daisuurin:
                        result.append(token_koyaku_dict[tokens.daisuurin])
                    elif type_ == tokens.suo and EnabledKoyaku.daichikurin:
                        result.append(token_koyaku_dict[tokens.daichikurin])
                    elif type_ == tokens.pin and EnabledKoyaku.daisharin:
                        result.append(token_koyaku_dict[tokens.daisharin])
            
            if EnabledKoyaku.daichisei and type_ == support.token_paitype_dict[tokens.zuu]:
                num_set: set[int] = set()
                num_set.add(p.number)
                for toitsu in toitsu_list[1:]:
                    p = toitsu.pai_list[0]
                    if p.number in num_set:
                        break
                    else:
                        num_set.add(p.number)
                else:
                    result.append(token_koyaku_dict[tokens.daichisei])

            if EnabledKoyaku.junseiheiiisoo and all(t.pai_list[0] in heiiisoopai_list for t in toitsu_list):
                result.append(token_koyaku_dict[tokens.junseiheiiisoo])

        # 三色同暗刻
        if EnabledKoyaku.sanshokudooankoo and token_yaku_dict[tokens.sanshokudookoo] in result and token_yaku_dict[tokens.sanankoo] in result:
            result.append(token_koyaku_dict[tokens.sanshokudooankoo])
        
        # 三色同槓
        if EnabledKoyaku.sanshokudookan and len(koutsu_list) >= 3 and sum(isinstance(furo, Minkan | Kakan | Ankan) for furo in tehai_comb.furo_list) >= 3:
            count_dict: dict[int, int] = {i:0 for i in range(1, 10)}
            for furo in tehai_comb.furo_list:
                if not isinstance(furo, Minkan | Kakan | Ankan):
                    continue
                p = furo.pai_tuple[0]
                if p.type == support.token_paitype_dict[tokens.zuu]:
                    continue
                count_dict[p.number] += 1
            if any(i >= 3 for i in count_dict.values()):
                result.append(token_koyaku_dict[tokens.sanshokudookan])

    # 處理複合役
    koumokukoukan_dict: dict[int, tuple[Yaku, ...]] = {}
    koumokukoukan_dict.update(yaku.koumokukoukan_token_dict)
    if BaseRules.koyaku_enabled:
        # 加入古役用複合役
        koumokukoukan_dict.update(yaku.koumokukoukan_koyaku_token_dict)
    if BaseRules.aotenjyou_enabled: # 青天井
        koumokukoukan_dict.update(yaku.oatenjyou_koumokukoukan_token_dict)
        if BaseRules.koyaku_enabled:
            # 加入古役用複合役
            koumokukoukan_dict.update(yaku.oatenjyou_koumokukoukan_koyaku_token_dict)
    else:
        # 若有役滿，則刪除役滿以外
        if any(y.is_yakuman for y in result):
            for y0 in result.copy():
                result.remove(y0) if not y0.is_yakuman else None
    for key, value in koumokukoukan_dict.items():
        if token_yaku_dict[key] in result:
            for y in value:
                result.remove(y) if y in result else None

    # sort
    result.sort(key = lambda n: n.ori_hansuu)

    return result
