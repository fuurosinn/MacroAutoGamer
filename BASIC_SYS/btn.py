### ==========================================================================.
#
#
#   ああああああああああ.
#
#
### ==========================================================================.


### ==========================================================================.
# import.

from copy import deepcopy
from BASIC_SYS.cord_loc import CORD_LOC

### ==========================================================================.
# BTN.

class BTN():
    def __init__(self):
        self.DEBUG_FLAG:bool
        self.DIM_BTNS:dict
        self.btn_dest:dict
        self.BTN_RESET()
        self.destination_list()

    def BTN_RESET(self):
        self.btn_dest = {}

    def __BTN_LOC(self, cord:dict={}) -> list:
        """
ボタンがどこに存在するのか, ボタンの大きさなどを解析.
cord ; dict : ボタンの位置データ, xywhでもx0y0x1y1でも自動で判断する.
        """
        cord_keys:list = cord.keys()
        if all(i in cord_keys for i in ("x", "y", "w", "h")):
            x0 = cord["x"]
            y0 = cord["y"]
            w = cord["w"]
            h = cord["h"]
            if any(i == None for i in (x0, y0, w, h)):
                return []
            x1 = x0 + w
            y1 = y0 + h
        elif all(i in cord_keys for i in ("x0", "y0", "x1", "y0")):
            x0 = cord["x0"]
            y0 = cord["y0"]
            x1 = cord["x1"]
            y1 = cord["y1"]
            if any(i == None for i in (x0, y0, x1, y1)):
                return []
        else:
            return []
        return [x0, y0, x1, y1]

    def destination_list(self):
        self.BTN_CORDS = {} # ボタンの位置情報.
        self.BTN_FUNCTIONS = {} # ボタンの機能.
        for k, d in zip(self.DIM_BTNS.keys(), self.DIM_BTNS.values()):
            cord_loc = self.__BTN_LOC(cord=d["cord"])
            if cord_loc == []:
                continue
            self.BTN_CORDS |= {k:cord_loc}

            func = d["FUNC"]
            self.BTN_FUNCTIONS |= {k:[]}
#            self.commands = [] # 記述されている処理の解析結果.

            for com in func: # そういや同じキーが2個以上は存在できないけど, 同じキーを2回以上使いたい場合はこっち側を仕様変更しないといけなくないか?.
                # comはdict型.
                # "FUNC":{"FUNC":"DRILL", "DATA":{"DESTINATION":"", "MEM":false}, {"FUNC":"JUMP", "DATA":{"RUNWAY":"", "MEM":false}}, {"FUNC":"DRILL", "DATA":{}}}.
                # "FUNC":[{"CMD":"FRILL", "DESTINATION":"", "MEM":false}]
                # "FUNC":["CMD":"USE", "LIST":["ITEM_NAME":AMOUNT(as int)]].
                if com == {}:
                    continue
                try:
                    cmd = com["CMD"] # command.
                except:
                    print(func)
                    raise
                res = []

                match cmd:
                    case "DRILL": # ボタン押して単純な遷移(すぐ下の階層に遷移)する場合に使用. DIVEはボタンで複雑な遷移をする場合に使用する.
                        destination:str = com["DESTINATION"] # 目的地.
#                        self.commands += [f">|{destination}"]
                        mem:bool = com["MEM"] # 記憶するかどうか.
                        res += [f">:{destination}"]

                    case "DIVE": # 複数階層に渡って遷移する場合.
                        # "FUNC":[{"CMD":"DIVE", "DESTINATION":""}]
                        dive_destination:str = com["DESTINATION"]

                        dive_dests = []
                        i = 0
                        while True:
                            ia = dive_destination.find("/", i)
                            if ia == -1:
                                break
                            dive_dests += [dive_destination[i:ia]]

                            i = ia + 1 # RESET.
                            ia = -1
                        dive_dests += [f"{dive_destination[i:]}"]

                        for dd in dive_dests:
                            res += [f">:{dd}"]
                    case "JUMP":
                        runway = com["RUNWAY"] # 複数の命令を入れる場合はlist型に入れておくこと.
                        if type(runway) == str:
                            runway = [runway]

                        mem:bool = com["MEM"]
                        
                        for run in runway:
                            if run[0] == "*": # * は絶対階層指定での移動.
                                match run[1]:
                                    case ".": # 階層上昇.
                                        if len(run) == 2:
                                            res += [".:1"]
                                        elif run[2] == ":":
                                            if len(run) == 3:
                                                res += [".:1"]
                                            else:
                                                if run[3:].isdigit():
                                                    res += [f".:{run[3:]}"]
                                                else:
                                                    raise BTN_EXCEPTION(f"日本語 : 階層指定の部分で *.: の後は正の整数じゃないとエラー。 例えば *.:12345 なら問題無いけど *.:three みたいなのはエラー。\nEnglisch : The third and subsequent characters of cmd must be able to recognized as positive digit. run == {run} ; (Usage) *.:[positive int] ")
                                        else:
                                            raise BTN_EXCEPTION(f"階層指定は正しくは *.:[positive int] だけど、 {run} で3文字目が : になっていない。 :を付けるか、上昇する階層数が1層のみならば *. のように省略もできる。ちなみに *.: でも1階層上昇扱いになる。")
                                    case "<": # 階層上昇(位置指定).
                                        if len(run) == 2:
                                            res += ["<:@base"] # @base は基底を表す. 略称は@B.
                                        elif run[2] == ":": # *<:
                                            jump_destination = run[3:]
                                            if jump_destination == "@B":
                                                res += [f"<:@base"]
                                            else:
                                                res += [run]
                            else:
                                pass
                    case "USE": # アイテム使用.
                        item_list = com["LIST"]
                        temp = "I-:" # Item -(==decrease).
#                        if any(not self.STOCK_CONFIRMATION_NAME(NAME=item, num=amount) for item, amount in zip(item_list.keys(), item_list.values())):
#                            pass
                        for item, amount in zip(item_list.keys(), item_list.values()):
                            temp += f"{item};{amount}:"
                        temp = temp[:-1]
                        res += [temp]
#                        print(f"DEBUG : USE ; temp == {temp}")
                    case "GET": #ゲッチュ!!.
                        item_list = com["LIST"]
                        temp = "I+:" # Item +(increase).
                        for item, amount in zip(item_list.keys(), item_list.values()):
                            temp += f"{item};{amount}:"
                        temp = temp[:-1]
                        res += [temp]
#                        print(f"DEBUG : GET ; temp == {temp}")
                self.BTN_FUNCTIONS[k] += deepcopy(res)

"""
note.

"PAGE":
{
    "BTNS":{},
    "PAGE":{},
    "FRAME_PAGE":{},
    "VARIBLE":
    [
        "$lova.sys:temp.json",
    ]
}

$lova.[mode];[file name] : load var.
[mode]
+-sys : システム全体共有.
+-gam : アプリ全体共有.
+-acc : 垢固有. 指定しない場合は自動的にこいつ扱い.

変数名
sys -> s_[file name]
gam -> g_[file name]
acc -> a_[file name]

$v, $var --> 読み込み済みの変数群の一部を参照.
$v:[var name]

$vt, $vtp, $vtemp, $vartemp --> 一時変数宣言.
$vt:[temp var's name] データ元の指定部分考える.

"""




class BTN_EXCEPTION(Exception):
    """
This is the exception for the btn.BTN .
    """
    pass