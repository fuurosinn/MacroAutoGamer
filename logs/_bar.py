class BAR():
    def __init__(self):
        pass

    def VECTOR(self, length:int=80, wrapper:dict[str:str]={"INITIAL":"[", "FINALLY":"]"}, vector:dict[str:str]={"BAR":"=", "EDGE":">", "VOID":" "}):
        """
進捗度合いなどを表す矢印を生成する.

length:int
矢印部分の長さ, wrapperは含まれていないことに注意.

wrapper:dict[str:str]
矢印を包む, \"INITIAL\"が\"[\", \"FINALLY\"が\"]\".
vector(矢印部分)と合わせると\"[=======>]\"のようになる.

vector:dict[str:str]
矢印部分, \"BAR\"が\"=\", \"EDGE\"が\">\", \"VOID\"が\" \".

        """
        pass

    def LOG_BLOCK(self, name:str="", wrapper:dict[str:str]={"INITIAL":" < ", "FINALLY":" > "}, wall:str="=", mode:str="CENTER", length:int=80) -> str:
        res = wrapper["INITIAL"] + name + wrapper["FINALLY"]
        res_len = len(res)
        wall_len = length - res_len
        match mode:
            case "CENTER":
                if wall_len % 2 == 1:
                    res = wall * (wall_len // 2 + 1) + res
            case "LEFT":
                pass
            case "RIGHT":
                pass
        res += wall * (length - len(res))
        return res

class BLOCK():
    def __init__(self):
        self.STACK = []

    def GROUP_TITLE(self, title:str="", BAR:bool=True, COLOUR:str="33"):
        """
title : グループ名
BAR : ===== <-を付けるかどうか
COLOUR : 色
        """
        temp = f" < {title} > "
        if BAR:
            temp += "=" * ( 80 - len(temp))
        temp = f"\033[{COLOUR}m" + temp + "\033[0m"
        self.STACK += [temp]