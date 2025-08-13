"""
「junme」、「巡目」、「巡目破壞」：一巡指玩家從打完一張牌到打出下一張牌之間的過程，
巡目破壞指玩家打出下一張牌之前，有出現會破壞巡目的行為，如任一玩家鳴牌。
「junme」計數：玩家初始 junme 為 0，每打出一張牌會 +1。
"""

from typing import overload, Literal, Iterable

from core.ext import support, yaku, tokens
from core.ext.index import *
from core.ext.rule import BaseRules
from core.ext.yaku import Yaku, token_yaku_dict

class Pai:
    def __init__(self, name: str | None):
        if not isinstance(name, str | None):
            raise TypeError(f"Pai() argument must be a string or None, not '{type(name).__name__}'")
        if name is None:
            # null type
            self.name, self.number, self.type, self.is_akadora, self.usual_name = None, None, None, None, None
        else:
            if len(name) != 2 or \
                not name[0].isdigit() or \
                name[1] not in (value for _, value in support.token_paitype_dict.items()):
                raise ValueError(f"Invalid value for Pai parameter name: {self.name}")
            if name[1] == support.token_paitype_dict[tokens.zuu]:
                num = int(name[0])
                if num > 7 or num == 0:
                    raise ValueError(f"Invalid value for Pai parameter name: {self.name}")

            self.name = name # here will preserve the akadora msg
            self.number = int(name[0]) if name[0] != "0" else 5
            self.type = name[1]
            self.is_akadora = (name[0] == "0")
            self.usual_name = str(self.number) + self.type
    
    def __eq__(self, other):
        if not isinstance(other, Pai | str):
            raise ValueError(f"Undefined operator __eq__ for Pai and {type(other).__name__}")
        if isinstance(other, str):
            other = Pai(other)
        if other.type is None or self.type is None:
            return False
        return other.type == self.type and other.number == self.number
    
    def __str__(self):
        return f"<Pai {self.name}>"

    def equal(self, other, is_strict: bool = True):
        if not isinstance(other, Pai | str):
            raise TypeError(f"other must be a Pai or str, not {type(other).__name__}")
        if isinstance(other, str):
            other = Pai(other)
        if self.type is None or other.type is None:
            return False
        if is_strict:
            return self.name == other.name
        return other.type == self.type and other.number == self.number

    def int_sign(self, is_include_akadora = False) -> int:
        # 1~9; 11~19; 21~29; 31~39; 41~47; 00 10 20 (akadora)
        if not isinstance(self.number, int):
            raise TypeError(f"cannot get sign with self.type: {type(self.number).__name__}")
        if not isinstance(self.type, str):
            raise TypeError(f"cannot get sign with self.type: {type(self.type).__name__}")
        if not isinstance(self.name, str):
            raise TypeError(f"cannot get sign with self.type: {type(self.name).__name__}")
        if not is_include_akadora:
            return support.paitype_sign_number_dict[self.type]*10 + self.number
        else:
            return support.paitype_sign_number_dict[self.type]*10 + int(self.name[0])

    def next(self, allow_mod = False):
        if self.number is None or self.type is None or self.name is None:
            return Pai(None)
        if self.type == support.token_paitype_dict[tokens.zuu]:
            if self.number >= 7 and not allow_mod:
                return Pai(None) 
            return Pai(str((self.number + 1) % 7) + self.type)
        else:
            if self.number >= 9 and not allow_mod:
                return Pai(None) 
            return Pai(str((self.number + 1) % 10) + self.type)
    
    def previous(self, allow_mod = False):
        if not isinstance(self.number, int):
            raise TypeError(f"cannot get previous with self.type: {type(self.number).__name__}")
        if not isinstance(self.type, str):
            raise TypeError(f"cannot get previous with self.type: {type(self.type).__name__}")
        if not isinstance(self.name, str):
            raise TypeError(f"cannot get previous with self.type: {type(self.name).__name__}")
        if self.type is None:
            return Pai(None)
        if self.type == support.token_paitype_dict[tokens.zuu]:
            if self.number <= 1 and not allow_mod:
                return Pai(None)
            return Pai(str((self.number - 1) % 7) + self.type)
        else:
            if self.number <= 1 and not allow_mod:
                return Pai(None)
            return Pai(str((self.number - 1) % 10) + self.type)

    def copy(self):
        new_pai = Pai(self.name)
        return new_pai

    @staticmethod
    def strict_remove(pai_list: list['Pai'], pai):
        if not isinstance(pai, Pai):
            raise TypeError(f"pai must be a Pai, not {type(pai).__name__}")
        pos: int | None = None
        count = 0
        for p in pai_list:
            if p.equal(pai):
                pos = count
                break
            count += 1
        if pos is None:
            return 
        del pai_list[pos]

yaochuu_list = [Pai(p) for p in support.yaochuu_paitype_tuple]
ryuuiisoopai_list = [Pai(p) for p in support.ryuuiisoopai_paitype_tuple]
chinroutoupai_list = [Pai(p) for p in support.chinroutoupai_paitype_tuple]
sanyuanpai_list = [Pai(p) for p in support.sanyuanpai_paitype_tuple]
suushiipai_list = [Pai(p) for p in support.suushiipai_paitype_tuple]

def create_pai_list(name_list: Iterable[str] | str):
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
    def __init__(self, type_: int, pai_list: list[Pai]):
        if type_ not in (tokens.koutsu, tokens.shuntsu):
            raise ValueError(f"Unknown type {type_} for Mentsu")
        self.type = type_ # tokens.koutsu, tokens.shuntsu, (tokens.ankan, tokens.kakan, tokens.minkan only appear in furo)
        self.pai_list = pai_list
    
    def __str__(self):
        output = "(" + " ".join([str(p.name) for p in self.pai_list]) + ")"
        return f"<Mentsu {output}>"
    
    def __eq__(self, other):
        if not isinstance(other, Mentsu):
            return False
        return self.type == other.type and sorted(self.pai_list, key=lambda p: p.int_sign())[0] == sorted(other.pai_list, key=lambda p: p.int_sign())[0]
    
    def copy(self):
        return Mentsu(self.type, [p.copy() for p in self.pai_list])

def get_mentsu(pai_list: list[Pai]) -> Mentsu:
    """生成順子 or 刻子，只能輸入 len(pai_list) 為 3"""
    pai_list = sorted(pai_list, key=lambda p: p.int_sign())
    if pai_list.count(pai_list[0]) == 1:
        return Mentsu(tokens.shuntsu, pai_list)
    else:
        return Mentsu(tokens.koutsu, pai_list)

class Toitsu:
    def __init__(self, pai: Pai | None = None, pai_list: list[Pai] | None = None):
        self.pai_list: list[Pai]
        if pai is None:
            if pai_list is None:
                raise ValueError("`pai` and `pai_list` could not be None at the same time.")
            else:
                self.pai_list = pai_list
        else:
            self.pai_list = [pai, pai.copy()]
    
    def __eq__(self, other):
        if not isinstance(other, Toitsu):
            return False
        return self.pai_list[0] == other.pai_list[0]

    def __str__(self):
        output = "(" + " ".join([str(p.name) for p in self.pai_list]) + ")"
        return f"<Toitsu {output}>"

    def copy(self):
        return Toitsu(pai_list=[p.copy() for p in self.pai_list])

class BasicFuro:
    """基本副露：吃、碰形成的副露"""
    # @overload
    # def __init__(self, type_: int, pai_tuple: tuple[Pai, ...], minpai_pai: Literal[None], from_player_id: Literal[None]) -> None:
    #     ...
    # @overload
    # def __init__(self, type_: int, pai_tuple: tuple[Pai, ...], minpai_pai: Pai, from_player_id: int):
    #     ...

    def __init__(self, 
                 type_: int, 
                 self_pai_tuple: tuple[Pai, Pai], 
                 received_pai: Pai, 
                 from_player_id: int) -> None:
        if type_ not in (tokens.koutsu, tokens.shuntsu):
            raise ValueError(f"Unknown type {type_} for BasicFuro")
        self.type = type_ # token.koutsu, token.shuntsu
        self.self_pai_tuple = self_pai_tuple
        self.received_pai = received_pai
        self.from_player_id = from_player_id

        self.pai_tuple = (*self_pai_tuple, received_pai)
    
    def to_mentsu(self):
        return Mentsu(self.type, [p.copy() for p in self.pai_tuple])
    
    def __str__(self):
        output = "(" + " ".join([p.__str__() for p in self.pai_tuple]) + ")"
        return f"<Furo {output}>"

class Minkan:
    def __init__(self, self_pai_tuple: tuple[Pai, Pai, Pai], received_pai: Pai, from_player_id: int) -> None:
        self.type = tokens.minkan
        self.self_pai_tuple = self_pai_tuple
        self.received_pai = received_pai
        self.from_player_id = from_player_id

        self.pai_tuple = (*self.self_pai_tuple, received_pai)
    
    def to_mentsu(self):
        """會丟失紅寶牌等細節資訊"""
        p = self.pai_tuple[0]
        if p.is_akadora:
            p = Pai(p.usual_name)
        return Mentsu(tokens.koutsu, [p, p.copy(), p.copy()])

class Kakan:
    def __init__(self, koutsu_furo: BasicFuro, received_pai: Pai) -> None:
        self.type = tokens.kakan
        self.koutsu_furo = koutsu_furo
        self.received_pai = received_pai

        self.pai_tuple = (*koutsu_furo.pai_tuple, received_pai)
    
    def to_mentsu(self):
        """會丟失紅寶牌等細節資訊"""
        p = self.pai_tuple[0]
        if p.is_akadora:
            p = Pai(p.usual_name)
        return Mentsu(tokens.koutsu, [p, p.copy(), p.copy()])

class Ankan:
    def __init__(self, self_pai_tuple: tuple[Pai, Pai, Pai, Pai]) -> None:
        self.type = tokens.ankan
        self.self_pai_tuple = self_pai_tuple

        self.pai_tuple = self_pai_tuple
    
    def to_mentsu(self):
        """會丟失紅寶牌等細節資訊"""
        p = self.pai_tuple[0]
        if p.is_akadora:
            p = Pai(p.usual_name)
        return Mentsu(tokens.koutsu, [p, p.copy(), p.copy()])

FuroType = BasicFuro | Minkan | Kakan | Ankan

class AgariComb:
    # 不考慮摸到哪張牌，拆分後的胡牌手牌 # 可為 2 5 8 11 14 張牌
    # 會將紅寶牌替換成普通牌，並記錄在 self.akadora_list 裡面
    def __init__(self, 
                 mentsu_list: list[Mentsu] | None = None, 
                 toitsu_list: list[Toitsu] | None = None, 
                 tanhai_list: list[Pai] | None = None, 
                 hoora_type: int | None = None, 
                 akadora_list: list[Pai] | None = None): 
        if mentsu_list is None:
            mentsu_list = []
        if toitsu_list is None:
            toitsu_list = []
        if tanhai_list is None:
            tanhai_list = []
        self.mentsu_list = mentsu_list
        self.toitsu_list = toitsu_list # len = 1 if not being chiitoitsu and koyaku
        self.tanhai_list = tanhai_list # only for kokushi if not including koyaku
        self.hoora_type = hoora_type # such as token.chiitoitsu_agari_type
        
        self.akadora_list: list[Pai]
        if akadora_list is None:
            self.akadora_list = []
            self.extract_akadora()
        else:
            self.akadora_list = akadora_list
    
    def __str__(self):
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

    def extract_akadora(self):
        for m in self.mentsu_list:
            for p in m.pai_list:
                if p.is_akadora:
                    self.akadora_list.append(p.copy())
                    p.is_akadora = False
        for t in self.toitsu_list:
            for p in t.pai_list:
                if p.is_akadora:
                    self.akadora_list.append(p.copy())
                    p.is_akadora = False
        for p in self.tanhai_list:
            if p.is_akadora:
                self.akadora_list.append(p.copy())
                p.is_akadora = False

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
                 akadora_revise_list: list[Pai] | None = None):
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

        self.tenpai_type = tenpai_type # such as token.ryanmenmachi
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
    
    def __str__(self):
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

    def revise_akadora(self, revise_list: list[Pai]):
        list_copy = revise_list.copy()
        for m in self.mentsu_list:
            for p in m.pai_list:
                if p in list_copy:
                    list_copy.remove(p)
                    p.is_akadora = True
                    p.name = "0" + p.name[1] # type: ignore
            if len(list_copy) == 0:
                return
        for t in self.toitsu_list:
            for p in t.pai_list:
                if p in list_copy:
                    list_copy.remove(p)
                    p.is_akadora = True
                    p.name = "0" + p.name[1] # type: ignore
            if len(list_copy) == 0:
                return
        for p in self.waiting_comb:
            if p in list_copy:
                list_copy.remove(p)
                p.is_akadora = True
                p.name = "0" + p.name[1] # type: ignore
        if len(list_copy) == 0:
            return 
        for p in self.tanhai_list:
            if p in list_copy:
                list_copy.remove(p)
                p.is_akadora = True
                p.name = "0" + p.name[1] # type: ignore
        
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

def is_agari(pai_list: list[Pai]):
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
            elif a1[0].type != support.token_paitype_dict[tokens.zuu] and a1[0] in a1 and a1[0].next() in a1 and a1[0].next().next() in a1:
                a, ap, app = a1[0], a1[0].next(), a1[0].next().next()
                a2.append((a, ap, app))
                a1.remove(a)
                a1.remove(ap)
                a1.remove(app)
            else:
                # 重製
                a1 = all_pai.copy()
                a2 = []
                break
        else:
            return True
    
    if BaseRules.is_koyaku:
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
            if l == sorted([pai.number for pai in all_pai_temp]): # type: ignore
                return True

    return False

def create_mentsu_list(pai_list: list[Pai], first_koutsu_deny: bool = False)  -> list[list[Mentsu]] | None:
    """分割去除對子之胡牌組合 可傳入 0 3 6 9 12 張，input 必須已排序"""
    if len(pai_list) == 0:
        return 
    all_pai = [pai.copy() for pai in pai_list]
    result = []
    if all_pai.count(all_pai[0]) < 3:
        # 沒刻子拔
        p = all_pai[0].copy()
        pp = p.next()
        ppp = pp.next()
        if p.type != support.token_paitype_dict[tokens.zuu] and pp in all_pai and ppp in all_pai:
            mentsu = Mentsu(tokens.shuntsu, [p, pp, ppp])
            all_pai.remove(p)
            all_pai.remove(pp)
            all_pai.remove(ppp)
            ll = create_mentsu_list(all_pai)
            result += [[mentsu] + l for l in ll] if not ll is None else [[mentsu]]
    else:
        if not first_koutsu_deny:
            # 先拔刻子
            p = all_pai[0].copy()
            mentsu = Mentsu(tokens.koutsu, [p, p.copy(), p.copy()])
            del all_pai[0]
            del all_pai[0]
            del all_pai[0]
            ll = create_mentsu_list(all_pai)
            result += [[mentsu] + l for l in ll] if not ll is None else [[mentsu]]

            # 再拔順子
            all_pai = [pai.copy() for pai in pai_list]
            p = all_pai[0].copy()
            pp = p.next()
            ppp = pp.next()
            if p.type != support.token_paitype_dict[tokens.zuu] and pp in all_pai and ppp in all_pai:
                mentsu = Mentsu(tokens.shuntsu, [p, pp, ppp])
                all_pai.remove(p)
                all_pai.remove(pp)
                all_pai.remove(ppp)
                ll = create_mentsu_list(all_pai, True) # 遞迴的第一張不能當刻子(前面拔過了，會撞)
                result += [[mentsu] + l for l in ll] if not ll is None else [[mentsu]]
        else:
            # 第一張不能當刻子
            # 拔順子
            p = all_pai[0].copy()
            pp = p.next()
            ppp = pp.next()
            if p.type != support.token_paitype_dict[tokens.zuu] and pp in all_pai and ppp in all_pai:
                mentsu = Mentsu(tokens.shuntsu, [p, pp, ppp])
                all_pai.remove(p)
                all_pai.remove(pp)
                all_pai.remove(ppp)
                ll = create_mentsu_list(all_pai, True) # (True or False 都沒差了)(如果同種牌只有四張)
                result += [[mentsu] + l for l in ll] if not ll is None else [[mentsu]]
    return result

def get_agari_comb_list(pai_list: list[Pai]) -> list[AgariComb]:
    """分割胡牌組合 可傳入 2 5 8 11 14 張"""

    result = []
    all_pai = [p.copy() for p in pai_list]
    all_pai.sort(key = lambda p: p.int_sign())

    # extrack akadora
    akadora_list = []
    for p in all_pai:
        if p.is_akadora:
            akadora_list.append(p.copy())
            p.is_akadora = False

    # 七對子型
    double: list[Pai]
    double = []
    for p in all_pai:
        if all_pai.count(p) >= 2 and not p in double:
            double.append(p)
    if len(double) == 0:
        return result # 暫無無對子之胡牌型
    if len(double) == 7:
        comb = AgariComb(toitsu_list=[Toitsu(p) for p in double], hoora_type=tokens.chiitoitsu_agari_type, akadora_list=akadora_list)
        result.append(comb)

    # 國士無雙型
    if all(p in all_pai for p in yaochuu_list):
        yaochuu_list_copy = yaochuu_list.copy()
        yaochuu_list_copy.remove(double[0])
        comb = AgariComb(toitsu_list=[Toitsu(double[0])], tanhai_list=yaochuu_list_copy, hoora_type=tokens.kokushimusou_agari_type, akadora_list=akadora_list)
        result.append(comb)
        return result # no other possible type

    # 普通型
    a1 = all_pai.copy()
    # comb_list = []
    for x in double:
        a1.remove(x)
        a1.remove(x)
        if len(a1) == 0:
            comb = AgariComb([], [Toitsu(pai_list=[x.copy(), x.copy()])], [], tokens.normal_agari_type, akadora_list)
            result.append(comb)
            break
        mentsu_list = create_mentsu_list(a1)
        if mentsu_list is None:
            mentsu_list = []
        for l in mentsu_list:
            comb = AgariComb(l, [Toitsu(pai_list=[x.copy(), x.copy()])], [], hoora_type=tokens.normal_agari_type, akadora_list=akadora_list)
            result.append(comb)
        # 重製
        a1 = all_pai.copy()

    # 古役
    if BaseRules.is_koyaku:
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
    def __init__(self, pai_list: list[Pai] | list[str]):
        if not isinstance(pai_list, list):
            raise TypeError(f"pai_list must be a list or str, not {type(pai_list).__name__}")
        pai_list = [Pai(p) if isinstance(p, str) else p.copy() for p in pai_list]
        self.pai_list = pai_list  # len = 1 4 7 10 13
        self.furo_list: list[FuroType] = []
        self.penuki_list: list[Pai] = []
    
    def __str__(self) -> str:
        output = ""
        output += " ".join([p.__str__() for p in self.pai_list])
        output += " | "
        output += " ".join([f.__str__() for f in self.furo_list])
        return output

    def sort(self):
        self.pai_list.sort(key = lambda p: p.int_sign())
    
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

    def is_able_to_chii(self, pai: Pai) -> bool:
        if pai.type == support.token_paitype_dict[tokens.zuu]:
            return False
        if any((pai.next() in self.pai_list and pai.next().next() in self.pai_list, 
                pai.previous() in self.pai_list and pai.next() in self.pai_list, 
                pai.previous() in self.pai_list and pai.previous().previous() in self.pai_list)):
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

class Param:
    def __init__(self, 
                 riichi_junme: int | None, 
                 agari_junme: int, 
                 agari_type: Literal["ron", "tsumo"], 
                 break_junme: bool, 
                 is_chyankan: bool, 
                 remaining_pai_num: int, 
                 menfon: int, 
                 chanfon: int, 
                 is_rinshanpai_agari: bool, 
                 dora_pointers: list[Pai], 
                 uradora_pointers: list[Pai] | None = None) -> None:
        if agari_type not in ("ron", "tsumo"):
            raise ValueError("agari_type must be 'ron' or 'tsumo'")
        
        self.riichi_junme = riichi_junme # 打出立直牌後的巡目
        self.agari_junme = agari_junme
        self.agari_type: Literal["ron", "tsumo"] = agari_type
        self.break_junme: bool = break_junme
        self.is_chyankan = is_chyankan
        self.remaining_pai_num = remaining_pai_num
        self.menfon = menfon
        self.chanfon = chanfon
        self.is_rinshanpai_agari = is_rinshanpai_agari
        self.dora_pointers = dora_pointers
        self.uradora_pointers = uradora_pointers if uradora_pointers is not None else []

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
    if len(tehai.get_tehai_comb_list()) == 0: # no ten
        raise RuntimeError("get_agari_result_list no ten error")
    available_tehai_comb_list: list[TehaiComb] = []
    for tc in tehai.get_tehai_comb_list():
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
        if BaseRules.is_aotenjyou or not is_yakuman: # calculate dora
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
    # if not BaseRules.is_aotenjyou: # 非青天井則役滿不計符數
    #     if yaku_list[0].is_yakuman: # 役滿以上
    #         return None
    if tehai_comb.tenpai_type == tokens.chiitoitsutanmenmachi: # 七對子
        return 25
    if BaseRules.is_koyaku:
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
        if p in yaochuu_list:
            fu += 8
        else:
            fu += 4
    for p in minkan_pai:
        if p in yaochuu_list:
            fu += 16
        else:
            fu += 8
    for p in ankan_pai:
        if p in yaochuu_list:
            fu += 32
        else:
            fu += 16

    return round_up(fu, 1)
    
def round_up(n: int, ndigits: int) -> int:
    mod = 10**ndigits
    return (n//mod + (n % mod != 0)) * mod

def get_tensuu(hansuu: int, fusuu: int, is_yakuman: bool, param: Param) -> tuple[int, tuple[int] | tuple[int, int], int]:
    basic_tensuu: int
    if BaseRules.is_aotenjyou or hansuu < 3 or (hansuu == 4 and fusuu <= 30) or (hansuu == 3 and fusuu <= 60):
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
            result.append(token_yaku_dict[tokens.dabururiichi].copy())
        else:
            result.append(token_yaku_dict[tokens.riichi].copy())
        if not param.break_junme:
            if param.agari_type == 'tsumo' and param.agari_junme == param.riichi_junme: # 一發自摸
                result.append(token_yaku_dict[tokens.ippatsu].copy())
            elif param.agari_type == 'ron' and param.agari_junme == param.riichi_junme: # 一發榮和
                result.append(token_yaku_dict[tokens.ippatsu].copy())

    # 搶槓
    if param.is_chyankan:
        result.append(token_yaku_dict[tokens.chyankan].copy())

    # 海底撈月、河底撈魚
    if param.remaining_pai_num == 0:
        if param.agari_type == 'tsumo':
            result.append(token_yaku_dict[tokens.haiteiraoyue].copy())
        elif param.agari_type == 'ron':
            result.append(token_yaku_dict[tokens.houteiraoyui].copy())
    
    # 斷么九
    if all((p not in yaochuu_list) for p in all_pai):
        if not BaseRules.is_kuitan and not is_menchin:
            pass 
        else:
            result.append(token_yaku_dict[tokens.tanyaochuu].copy())
        
    # 役牌
    for mentsu in koutsu_list:
        if mentsu.pai_list[0].type == support.token_paitype_dict[tokens.zuu]:
            pai_name = mentsu.pai_list[0].name
            # 三元牌
            if pai_name == support.token_yakuhai_painame_dict[tokens.yakuhai_haku]:
                result.append(token_yaku_dict[tokens.yakuhai_haku].copy())
            elif pai_name == support.token_yakuhai_painame_dict[tokens.yakuhai_hatsu]:
                result.append(token_yaku_dict[tokens.yakuhai_hatsu].copy())
            elif pai_name == support.token_yakuhai_painame_dict[tokens.yakuhai_chun]:
                result.append(token_yaku_dict[tokens.yakuhai_chun].copy())
            # 自風牌
            if support.token_yakuhai_painame_dict[support.fonwei_token_tsufon_yaku_dict[param.menfon]] == pai_name:
                result.append(token_yaku_dict[support.fonwei_token_tsufon_yaku_dict[param.menfon]].copy())
            # 場風牌
            if support.token_yakuhai_painame_dict[support.fonwei_token_chanfon_yaku_dict[param.chanfon]] == pai_name:
                result.append(token_yaku_dict[support.fonwei_token_chanfon_yaku_dict[param.chanfon]].copy())

    # 門清役
    if is_menchin: # 門清
        # 自摸
        if param.agari_type == 'tsumo':
            result.append(token_yaku_dict[tokens.tsumo].copy())

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
            result.append(token_yaku_dict[tokens.pinfu].copy())

        # 一盃口、二盃口
        if len(shuntsu_list) >= 2:
            shuntsu_set = [x for i, x in enumerate(shuntsu_list) if x not in shuntsu_list[:i]]
            peekoosuu = sum([shuntsu_list.count(m) == 2 for m in shuntsu_set])
            if peekoosuu >= 1:
                result.append(token_yaku_dict[tokens.iipeekoo].copy())
            if peekoosuu >= 2:
                result.append(token_yaku_dict[tokens.ryanpeekoo].copy())

        # 四暗刻
        if len(koutsu_list) == 4:
            if tehai_comb.tenpai_type == tokens.soohoomachi and param.agari_type == 'tsumo':
                result.append(token_yaku_dict[tokens.suuankoo].copy())
            elif tehai_comb.tenpai_type == tokens.tankimachi:
                result.append(token_yaku_dict[tokens.suuankootanki].copy())
 
        # 國士、國士十三
        if tehai_comb.tenpai_type == tokens.kokushimusoutanmenmachi:
            result.append(token_yaku_dict[tokens.kokushimusou].copy())
        elif tehai_comb.tenpai_type == tokens.kokushimusoujuusanmenmachi:
            result.append(token_yaku_dict[tokens.kokushimusoujuusanmen].copy())

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
                        result.append(token_yaku_dict[tokens.junseichuurenpouton].copy())
                    else:
                        result.append(token_yaku_dict[tokens.chuurenpouton].copy())

    # 嶺上開花
    if param.agari_type == 'tsumo' and param.is_rinshanpai_agari:
        result.append(token_yaku_dict[tokens.rinshankaihou].copy())

    # 七對子
    if tehai_comb.tenpai_type == tokens.chiitoitsutanmenmachi:
        result.append(token_yaku_dict[tokens.chiitoitsu].copy())

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
                result.append(token_yaku_dict[tokens.sanshokudoujun].copy())
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
                result.append(token_yaku_dict[tokens.ikkitsuukan].copy())
                break

    # 混全、純全
    if all(t.pai_list[0] in yaochuu_list for t in toitsu_list):
        if all(any(p in yaochuu_list for p in m.pai_list) for m in mentsu_furo_list):
            if all(t.pai_list[0] in chinroutoupai_list for t in toitsu_list) and all(any(p in chinroutoupai_list for p in m.pai_list) for m in mentsu_furo_list):
                result.append(token_yaku_dict[tokens.junchantaiyaochuu].copy())
            else:
                result.append(token_yaku_dict[tokens.honchantaiyaochuu].copy())

    # 對對和
    if len(koutsu_list) == 4:
        result.append(token_yaku_dict[tokens.toitoihoo].copy())

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
            result.append(token_yaku_dict[tokens.sanankoo].copy())

    # 混老頭、清老頭
    if all(p in yaochuu_list for p in all_pai):
        if all(p in chinroutoupai_list for p in all_pai):
            result.append(token_yaku_dict[tokens.chinroutou].copy())
        elif all(p.type != support.token_paitype_dict[tokens.zuu] for p in all_pai):
            result.append(token_yaku_dict[tokens.honroutou].copy())

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
                result.append(token_yaku_dict[tokens.sanshokudookoo].copy())
                break

    # 三槓子、四槓子
    if len(tehai_comb.furo_list) >= 3:
        kantsu_number = sum([f.type in (tokens.minkan, tokens.ankan, tokens.kakan) for f in tehai_comb.furo_list])
        if kantsu_number == 4:
            result.append(token_yaku_dict[tokens.sankantsu].copy())
            result.append(token_yaku_dict[tokens.suukantsu].copy())
        elif kantsu_number == 3:
            result.append(token_yaku_dict[tokens.sankantsu].copy())

    # 小三元
    if toitsu_list[0].pai_list[0] in sanyuanpai_list:
        list_copy = sanyuanpai_list.copy()
        list_copy.remove(toitsu_list[0].pai_list[0])
        for m in koutsu_list:
            pai = m.pai_list[0]
            if pai in list_copy:
                list_copy.remove(pai)
        if len(list_copy) == 0:
            result.append(token_yaku_dict[tokens.shousangen].copy())

    # 混一色、清一色、字一色
    type_set = {p.type for p in all_pai}
    if len(type_set) <= 2:
        if support.token_paitype_dict[tokens.zuu] in type_set:
            if len(type_set) == 1: # 字一色
                result.append(token_yaku_dict[tokens.tsuuiisoo].copy())
            else: # 混一色
                result.append(token_yaku_dict[tokens.honiisoo].copy())
        elif len(type_set) == 1: # 清一色
            result.append(token_yaku_dict[tokens.chiniisoo].copy())
    
    # 天地和
    if param.agari_type == 'tsumo' and param.agari_junme == 0:
        # 天和
        if param.menfon == support.fonwei_tuple[0]:
            result.append(token_yaku_dict[tokens.tenhou].copy())
        # 地和
        else:
            result.append(token_yaku_dict[tokens.chiihou].copy())

    # 大三元
    if len(koutsu_list) >= 3:
        sanyuanpai_list_copy = sanyuanpai_list.copy()
        for m in koutsu_list:
            if m.pai_list[0] in sanyuanpai_list_copy:
                sanyuanpai_list_copy.remove(m.pai_list[0])
        if len(sanyuanpai_list_copy) == 0:
            result.append(token_yaku_dict[tokens.daisangen].copy())

    # 小四喜
    if len(koutsu_list) >= 3 and toitsu_list[0].pai_list[0] in suushiipai_list:
        suushiipai_list_copy = suushiipai_list.copy()
        suushiipai_list_copy.remove(toitsu_list[0].pai_list[0])
        for m in koutsu_list:
            if m.pai_list[0] in suushiipai_list_copy:
                suushiipai_list_copy.remove(m.pai_list[0])
        if len(suushiipai_list_copy) == 0:
            result.append(token_yaku_dict[tokens.shousuushii].copy())

    # 綠一色
    if all(p in ryuuiisoopai_list for p in all_pai):
        result.append(token_yaku_dict[tokens.ryuuiisoo].copy())

    # 大四喜
    if len(koutsu_list) >= 4:
        suushiipai_list_copy = suushiipai_list.copy()
        for m in koutsu_list:
            if m.pai_list[0] in suushiipai_list_copy:
                suushiipai_list_copy.remove(m.pai_list[0])
        if len(suushiipai_list_copy) == 0:
            result.append(token_yaku_dict[tokens.daisuushii].copy())

    # 古役
    if BaseRules.is_koyaku:
        pass 

    # 處理複合役
    koumokukoukan_dict: dict[int, tuple[Yaku, ...]] = {}
    koumokukoukan_dict.update(yaku.koumokukoukan_token_dict)
    if BaseRules.is_koyaku:
        koumokukoukan_dict.update(yaku.koumokukoukan_koyaku_token_dict)
    if BaseRules.is_aotenjyou: # 青天井
        # 加入古役用複合役
        koumokukoukan_dict.update(yaku.oatenjyou_koumokukoukan_token_dict)
        if BaseRules.is_koyaku:
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
