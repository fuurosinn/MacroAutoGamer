### ==========================================================================.
#
#
#   ゲーム内での現在地までの経路を記録する.
#   例えば現在地が倉庫なら, ホーム画面 -> 倉庫がまず考えられる.
#   しかしホーム画面 -> キャラクター一覧 -> 特定のキャラ -> 倉庫という経路もあり得る.
#   このように同じ位置にいるけど経路が違うから, 戻るボタンを押したときに戻る場所が異なることが考えられる.
#   その問題を解決するための機能.
#
#
### ==========================================================================.


### ==========================================================================.
# import.

import os
from json import load
from copy import deepcopy

from glov import glov_core as g

from BASIC_SYS.loader import LOADER
from BASIC_SYS.btn import BTN, BTN_EXCEPTION
from BASIC_SYS.frame import FRAME

from glov.glov_controll import CONT

### ==========================================================================.
# dimensionar.

# ./game_info/~~~/dim.json.

# "BTN_NAME":{"cord":{"x":x座標, "y":y座標}, "DRILL":"転移先, 転移しないならnull", "MEM":"転移後に記憶されるかどうか", "FUNC":"機能を持つかどうか"}
# FUNCの内容.
# "DRILL":{"DESTINATION":"目的地", "MEM":True or False}. 1つ下の階層に降りる.
# "JUMP":{"RUNWAY":["目的地までの/移動経路を/記述する"], "MEM":True or False}.
# RUNWAYは"*.:(数値)"で指定された数値の次元数分だけ上昇する.
# "*."のように上昇する次元数が1の場合は省略可能.
# "*<"は基底を表す.
# 同じ地点に2か所以上から接続できる場合は... 後で考える. (基本は自分が進んできた場所からのほうが優先?).
# MEMはTrueにすると移動先で戻るボタンを押したときに記憶された場所まで戻ってくる判定とみなすようになる.


# "FRAME":{"フレーム名称":{"RECT":{表示範囲}, "PAL":{平行部分}}}
# "SLIDE":{} スライドする.
# "SLIDE":{"size":{"width":int, "height":int}}

# LIST:{"RECT":{}, "SIZE":{"width":null, "height":null}}
# width, height : リストの縦, 横それぞれの要素数. nullなら変化する値扱い.

# BTNのFUNCの記述.
# "POPP" -> ポップアップでミニウィンドウ表示. 
# "RECT":{"x":null, "y":null, "w":null, "h":null}
# x, y : 左上の座標.
# w, h : 横幅, 縦幅.


# ボタン, ポップアップはx, y, w, h.
# フレームはx0, y0, x1, y1.

# "POPP"の"FUNC"内では"CLOSE":"POPP"で"POPP"が閉じる.

# BTNS内部のSET_FUNCはボタン類がほぼ同じ挙動を示す場合に使用する.
# 読み込む場合はUSE_FUNC=true.


# weather.jsonはその時々のゲームの情報が記述されている.

LOG_OUTPUT_PAGE_LIST:bool = False
LOG_OUTPUT_FRAME_LIST:bool = False
LOG_OUTPUT_DESCENT:bool = False
LOG_OUTPUT_ANALYZED:bool = False

class DIMENSIONAR(BTN): # BASEMENTを継承することにしていたけど、MROのエラー出たから消した.
    def __init__(self):
        self.DEBUG_FLAG = False
        self.VL_DIMS_PRESET = "/*n|*//*<DIMS>*/ : "
        g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+"/*st*/ACTIVE/*st_*/")
        # =====================================.
        self.PARENT:str

        self.GAME_INFO_DIR:str
        self.GAME_INFO_NAME:str

        self.GAME_DIR:str
        self.DATA_ID:str
        self.DATA_DIR:dict

        self.FLAG_SET_DATA_ID:bool
        self.FLAG_DIMENTION_LOADED:bool = False # 既に次元の構造を読み込んでいるかどうか, 垢を切り替える時に再度読み込む処理を飛ばせる.
        # =====================================.
        self.HOME_DEFAULT = "TITLE" # デフォの基底次元の設定.
        self.RESET_DIMENSION()

        self.SET_DIMENTION()
        self.ARROW = g.LS.COLOUR_WITH_CODE(RGB="FFD700")+"<"+g.LS.COLOUR_WITH_CODE()
        g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+"/*st*/LAUNCHED/*st_*/")

    def SET_DIMENTION(self):
        """
階層設定.
        """
        if self.FLAG_SET_DATA_ID:
#            print(f"DEBUG : GAME_INFO_DIR == {self.GAME_INFO_DIR}, DATA_DIR[] == " + str(self.DATA_DIR["GAME_INFO_DIMENSION"]))
#            _, self.DIM_STRUC = LOADER(DIR=self.GAME_INFO_DIR, NAME=self.DATA_DIR["GAME_INFO_DIMENSION"])
#            print(f"DEBUG : _ == {_}, DIM_STRUC == {self.DIM_STRUC}")
            if not self.FLAG_DIMENTION_LOADED:
                with open(os.path.join(self.GAME_INFO_DIR, self.DATA_DIR["GAME_INFO_DIMENSION"]), mode="r", encoding="unicode-escape") as f:
                    self.DIM_STRUC = load(f)
                self.FLAG_DIMENTION_LOADED = True
                g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+"STRUCTURE ; /*st*/VALID/*st_*/") # 次元の構造読み込み済みのログ出力.

            self.RESET_DIMENSION()
            self.DIMENTION_ANALYZE()

            self.BTN_RESET()
            BTN.__init__(self)
        else:
            g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+"STRUCTURE ; /*st*/INVALID/*st_*/")

    def RESET_DIMENSION(self):
        self.HOME = self.HOME_DEFAULT # base.
        if self.FLAG_DIMENTION_LOADED:
            self.WAY = [self.HOME] # 現在地までの道のり.
            self.ROOT = [self.DIM_STRUC[self.HOME]] # 現在地までに使用した階層の情報. 例えば{"a":{"b":{~}}}なら, [{"b":{~}}, {~}]となる.
            self.VARIABLES = []
        else:
            self.WAY = []
            self.ROOT = []

            self.VARIABLES = [] # self.WAYとself.ROOTと同じ消去を発生させるんだからね///.

        self.DIM_FORK = None
        self.DIM_BTNS = None
        self.btn_cord = None
        self.btn_cord_center_x = None
        self.btn_cord_center_y = None
        self.frame_info = {} # フレーム操作の記録.

    def SET_HOME(self, NEW_HOME:str=""):
        """
基底階層を変更する.
ただし現在地までの通り道で通過した階層しか設定できない.
        """
        if NEW_HOME not in self.WAY:
            raise

        g.LS.LOGGING(msg=self.VL_DIMS_PRESET+"HOME CHANGED")
        temp_len = g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET, out=False, ret_len=True) - 1
        g.LS.LOGGING(msg=" "*temp_len+f" {self.HOME}")
        g.LS.LOGGING(msg=" "*temp_len+ g.LS.COLOUR_WITH_CODE(RGB="FFFF00") + f" [{NEW_HOME}] " + g.LS.COLOUR_WITH_CODE() + self.ARROW)
        self.HOME = NEW_HOME
        g.LS.PUSH()
        del self.WAY[:self.WAY.index(NEW_HOME)]
        self.DIMENTION_ANALYZE()

    def TAP_BTN(self):
        """
ボタンタップ.
事前にself.btn_cordに座標が格納されていないといけない.
g.SYSTEM_BOOT_MODE == DEBUG なら実際にタップはせずに, 座標を出力する.

のちのち画像認識と連携して, 本当にそこにボタンが存在するのか確認する処理を追加したい.
        """
        if g.SYSTEM_BOOT_MODE == "DEBUG":
            g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+f"TAP_BTN ; x == {self.btn_cord_center_x}, y == {self.btn_cord_center_y}")
        else:
            CONT.TAP_WITH_CORD(x=self.btn_cord_center_x, y=self.btn_cord_center_y)

    def BTN_CENTER_POINT(self, btn_name:str=None):
        """
ボタンの中心座標を計算する処理.
必要な個所で自動で呼び出すように記述済み.

btn_nameを省略したら既にbtn_cord指定済みに扱いになる.
        """
        if btn_name != None:
            self.btn_cord = self.BTN_CORDS[btn_name]
        self.btn_cord_center_x = (self.btn_cord[0]+self.btn_cord[2]) / 2
        self.btn_cord_center_y = (self.btn_cord[1] + self.btn_cord[3]) / 2

    def DIMENTION_ANALYZE(self):
        """
存在する階層の構造を調べる.
別階層に移動したらこの関数を実行する必要がある.
        """
#        print(f"DEBUG : self.ROOT == {self.ROOT}")
        FLAG_EXIST_BTNS:bool = "BTNS" in self.ROOT[-1].keys()
        FLAG_EXIST_PAGE:bool = "PAGE" in self.ROOT[-1].keys()
        FLAG_EXIST_FRAME:bool = "FRAME" in self.ROOT[-1].keys() # FRAME_PAGEの実装を忘れないこと. *REF_POINTはREFERENCE POINTで基準点の意味.
        FLAG_EXIST_VARIABLE:bool = "VARIABLE" in self.ROOT[-1].keys()

        if LOG_OUTPUT_ANALYZED:
            temp_len = g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET, out=False, ret_len=True)
            g.LS.LOGGING(msg=[self.VL_DIMS_PRESET+"ANALYZED",\
                              " "*temp_len+f"< BTNS > : {FLAG_EXIST_BTNS}",\
                              " "*temp_len+f"< PAGE > : {FLAG_EXIST_PAGE}",\
                              " "*temp_len+f"< FRAME > : {FLAG_EXIST_FRAME}",\
                              ""])
            g.LS.PUSH()

        if FLAG_EXIST_PAGE: # 接続された階層が存在しない場合.
            self.DIM_FORK = self.ROOT[-1]["PAGE"] # 分岐先.

            # ==== < ログ出力しているだけ > ====.
            if LOG_OUTPUT_PAGE_LIST:
                g.LS.LOGGING(msg=self.VL_DIMS_PRESET+f"{len(self.DIM_FORK.keys())} forks exist.")
                temp_len = g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET, out=False, ret_len=True)
                temp_page_num = len(self.DIM_FORK.keys())

                g.LS.LOGGING(msg=" "*(temp_len-1)+g.LS.COLOUR_WITH_CODE(RGB="FFFF00") + f"[{self.WAY[-1]}] " + g.LS.COLOUR_WITH_CODE() + self.ARROW)
                temp_len += len(self.WAY[-1]) // 2 + 1
                for num, f in enumerate(self.DIM_FORK.keys()):
                    temp_msg = " " * temp_len
                    if temp_page_num == num + 1:
                        temp_msg += "┗ "
                    else:
                        temp_msg += "┣ "
                    temp_msg += f"{num}. {f}"
                    g.LS.LOGGING(msg=temp_msg)
                g.LS.PUSH()
            # ==== < ここまで > ====.

        self.frame_info = {}
        if FLAG_EXIST_FRAME:
            self.SUB_DIM_FORK = self.ROOT[-1]["FRAME"]
            self.SUB_FORK_INFO = FRAME(frame_data=self.SUB_DIM_FORK)


            for k in self.SUB_FORK_INFO.dest.keys():
                temp = list(self.SUB_FORK_INFO.dest[k].keys())[1] # [0]は*frame_cordなので[1].
                self.frame_info |= {k:temp}

            # ==== < ログ出力 > ====. ここに致命的な無限ループバグが存在. <-- なんか普通に動いたんだが???.
            if LOG_OUTPUT_FRAME_LIST:
#                print("DEBUG : CHECK LOG OUTPUT")
                g.LS.LOGGING(msg=self.VL_DIMS_PRESET+f"{len(self.SUB_DIM_FORK.keys())} subforks exist.")

                temp_len = g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET, out=False, ret_len=True)
                temp_page_num = len(self.SUB_DIM_FORK.keys())

                g.LS.LOGGING(msg=" "*(temp_len-1)+g.LS.COLOUR_WITH_CODE(RGB="FFFF00") + f"[{self.WAY[-1]}] " + g.LS.COLOUR_WITH_CODE() + self.ARROW)
                temp_len += len(self.WAY[-1]) // 2 + 1
                for num, f in enumerate(self.SUB_DIM_FORK.keys()):
#                    print(f"DEBUG num == {num}")
                    temp_msg = " " * temp_len
                    if temp_page_num == num + 1:
                        temp_msg += "┗ "
                    else:
                        temp_msg += "┣ "
                    temp_msg += f"{num}. {f}"
                    g.LS.LOGGING(msg=temp_msg)
                g.LS.PUSH()
            # ==== < ここまで > ====.

        if not FLAG_EXIST_PAGE and not FLAG_EXIST_FRAME:
            g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+"NO CONNECTED SPACE BELOW CURRENT LOCATION")

        if FLAG_EXIST_VARIABLE:
            pass

        if FLAG_EXIST_BTNS:
            self.DIM_BTNS = deepcopy(self.ROOT[-1]["BTNS"]) # ボタン. # CHECK 1.
        else:
            g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+"NO BUTTONS")


    def PUSH_BUTTON(self, btn_name:str=""):
        """
ボタンを押す.
記述されている関数も実行されることに注意.
        """
        pass


    def __SELECT_BUTTON(self, dest:str=None, push:bool=True):
        """
もう使っていない関数.

ボタン選択.
遷移方法に複数の候補が存在する場合も対処.

dest ; str=None : destination, 遷移先.
push ; bool=True : ボタンを自動で押すかどうか.
        """
        if dest not in self.btn_dest.keys():
            print(f"dest == {dest}")
            print(f"destination list == {self.btn_dest}")
            raise
        if dest not in self.DIM_FORK.keys():
            raise
        candi = self.btn_dest[dest]
        if type(candi) == list:
            pass
        elif type(candi) == dict:
            self.btn_data = candi
            self.btn_name = list(self.btn_data.keys())[0]
            self.btn_cord = list(self.btn_data.values())[0]
        self.BTN_CENTER_POINT()
        g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+"SELECT_BUTTON ; /*st*/SUCCEED/*st_*/")

        if push:
            self.TAP_BTN()
            self.DESCENT(PAGE_NAME=dest) # NAME = self.btn_nameにすると, ボタンの名称が遷移先のページの名前とは限らないのでエラー出る場合がある.

    def SELECT_FRAME(self, fname:str=None, pal_name:str=None, push:bool=True):
        """
フレームの選択.

fname ; str=None : Frame NAME, 選択するフレーム名. rとnを間違えないように注意.
push ; bool=True : 自動で押すかどうか.
        """
        if fname not in self.SUB_FORK_INFO.dest.keys():
            raise
        if fname not in self.SUB_DIM_FORK.keys():
            raise

        frame_candi = self.SUB_FORK_INFO.dest[fname]
        if pal_name not in frame_candi.keys():
            raise

        frame_base_cord = frame_candi["*frame_cord"] # x0, y0, x1, y1.
        candi = frame_candi[pal_name]
        relative_cord = candi["*r_btn_cord"]
        self.btn_cord = relative_cord
#        self.btn_cord = [frame_base_cord[0]+relative_cord[0],\
#                         frame_base_cord[1]+relative_cord[1],\
#                         frame_base_cord[0]+relative_cord[2],\
#                         frame_base_cord[1]+relative_cord[3]]
#        self.btn_cord = [i + ia for i, ia in zip(frame_base_cord, relative_cord)]

#        print(f"DEBUG : frame_base_cord == {frame_base_cord}")
#        print(f"DEBUG : relative_cord == {relative_cord}")
#        print(f"DEBUG : btn_cord == {self.btn_cord}")
        self.BTN_CENTER_POINT()

        if push:
            self.TAP_BTN()
            self.frame_info[fname] = pal_name


    def ASCENT(self, t:int=1):
        """
上の階層に戻る時の処理.
t ; int=1 : 上昇する階層数.

自動でself.DIMENTION_ANALYZE()を呼び出して次の階層の解析をする.
        """
        if t >= 2:
            raise # まだ作っていない定期.
        if self.WAY[-1] == self.HOME:
            raise
        del self.WAY[-1]
        del self.ROOT[-1]
        g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+"SPATIAL TRANSITION ; " + g.LS.COLOUR_WITH_CODE(RGB="4169E1") + "ASCENT" + g.LS.COLOUR_WITH_CODE())
        self.DIMENTION_ANALYZE()
        self.destination_list()

    def DESCENT(self, PAGE_NAME:str="", FRAME_NAME:str=""):
        """
下の階層に降りた時の処理.
PAGE_NAME ; str : 指定する階層.

自動でself.DIMENTION_ANALYZE()を呼び出して次の階層の解析をする.
        """

        if LOG_OUTPUT_DESCENT:
            g.LS.LOGGING(msg=self.VL_DIMS_PRESET+"SPATIAL TRANSITION ; " + g.LS.COLOUR_WITH_CODE(RGB="EE82EE") + "DESCENT" + g.LS.COLOUR_WITH_CODE())
            temp_len = g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET, out=False, ret_len=True)
            g.LS.LOGGING(msg=" "*temp_len+f"{self.WAY[-1]}")
            temp_len += len(self.WAY[-1]) // 2 + 1
            temp_page_num = len(self.DIM_FORK.keys())
            for num, f in enumerate(self.DIM_FORK.keys()):
                temp_msg = " " * temp_len
                if temp_page_num == num + 1:
                    temp_msg += "┗"
                else:
                    temp_msg += "┣"
                if f == PAGE_NAME:
                    temp_msg += g.LS.COLOUR_WITH_CODE(RGB="FFFF00") + f" [{f}] " + g.LS.COLOUR_WITH_CODE() + self.ARROW
                else:
                    temp_msg += f" {f}"
                g.LS.LOGGING(msg=temp_msg)
        else:
            g.LS.LOGGING(msg=self.VL_DIMS_PRESET+"SPATIAL TRANSITION ; " + g.LS.COLOUR_WITH_CODE(RGB="EE82EE") + "DESCENT" + g.LS.COLOUR_WITH_CODE() + f" TO {PAGE_NAME}")
        g.LS.PUSH()

        # ==== < ここまでがくそながログ関連 > ====.

        self.WAY.append(PAGE_NAME)
        self.ROOT.append(self.ROOT[-1]["PAGE"][PAGE_NAME])
        self.DIMENTION_ANALYZE()
        self.destination_list()

    def BTN_EXECUTOR(self, btn_name:str):
        self.destination_list() # 一旦効率は考えないようにしよう.
        if btn_name not in self.BTN_FUNCTIONS.keys():
            raise BTN_EXCEPTION(f"btn_nameとして指定された {btn_name} はボタン名称として存在しない.")

        self.BTN_CENTER_POINT(btn_name=btn_name)
        self.TAP_BTN()

        funcs = self.BTN_FUNCTIONS[btn_name]
        for f in funcs:
            match f[0]:
                case ".":
                    t = int(f[2:])
                    if t <= 0:
                        raise BTN_EXCEPTION(f"cmd == {f}, 階層の上昇回数として指定された {f[2:]}は1以上にしなければならない.")
                    self.ASCENT(t=t)
                case "<":
                    d = f[2:] # Destination.
                    if d == "@base":
                        d = self.HOME
                    t = [num for num, i in enumerate(self.WAY) if i == d]
                    if t == []:
                        raise BTN_EXCEPTION(f"cmd == {f}, 指定された階層がself.WAY内部に存在しない.")
                    t = [-1] # 名称が重複していた場合は階層が低い方に飛ぶ. 現在の階層の名称と指定された階層の名称が同じ場合の挙動って...階層変わらないよね?.
                    del self.WAY[t+1:]
                    del self.ROOT[t+1:]
                    self.DIMENTION_ANALYZE()
                case ">":
                    d = f[2:] # Destination.
                    self.DESCENT(PAGE_NAME=d)
                case "I": # アイテム関連.
                    match f[1]:
                        case "-":
                            if f[2] != ":":
                                raise # I-:, I-まではあっているけど:ではない場合.
                            requested_item_dict_in_str:str = f[3:]
                            FLAG_ALL_ITEMS_STOCKED_ENOUGH:bool = True
                            requested_item_dict:dict = {}
                            i = 0
                            ia = 0
                            while True:
                                i = requested_item_dict_in_str.find(":")
                                ia = requested_item_dict_in_str.find(";")
#                                print(f"DEBUG : {f}, i == {i}, ia == {ia}")
                                if i != -1 and ia != -1:
                                    item_name = requested_item_dict_in_str[:ia]
                                    item_amount = int(requested_item_dict_in_str[ia+1:i])
                                    if not self.CONFIRM_STOCK(item_name=item_name, item_amount=item_amount): # これ同じアイテムを複数回要求される場合, アイテムが足りなくなってバグるパターンあるな... .
                                        temp = self.STORAGE[item_name]["AMOUNT"]
                                        g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET+f"{item_name} is shortage. Requested {item_amount}, but {temp} in storage.")
                                        FLAG_ALL_ITEMS_STOCKED_ENOUGH = False
                                        break # 例えばAの在庫が5個で, 最初にAを5個要求されて, 次にAを1個要求されたら合計は6個だけど, 個々の確認では通ってしまう.
                                    requested_item_dict |= {item_name:item_amount}
                                    requested_item_dict_in_str = requested_item_dict_in_str[i+1:]
                                elif i == -1 and ia != -1: # 想定どうりのループ終了.
                                    item_name = requested_item_dict_in_str[:ia]
                                    item_amount = int(requested_item_dict_in_str[ia+1:])
                                    requested_item_dict |= {item_name:item_amount}
                                    break
                                elif ia == -1: # エレエレエレエレ!!.
                                    break
                                else:
                                    raise
                            if FLAG_ALL_ITEMS_STOCKED_ENOUGH:
                                temp_len = g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET, out=False, ret_len=True)
                                temp_preset = " " * temp_len
                                g.LS.LOGGING(msg=["", temp_preset+"< CONSUMED ITEMS >"])
                                for item_name, item_amount in zip(requested_item_dict.keys(), requested_item_dict.values()):
                                    g.LS.LOGGING(msg=temp_preset+f"{item_name} : -{item_amount}   |   "+str(self.STORAGE[item_name]["AMOUNT"]-item_amount)+" left")
                                    self.CONSUME_STOCK(item_name=item_name, item_amount=item_amount)
                                g.LS.LOGGING(msg="")
                                g.LS.PUSH()
                            else:
                                raise
                        case "+":
#                            print(f"DEBUG : f == {f}")
                            if f[2] != ":":
                                raise
                            got_item_dict_in_str:str = f[3:]
                            got_item_dict:dict = {}
                            i = 0
                            ia = 0
                            while True:
                                i = got_item_dict_in_str.find(":")
                                ia = got_item_dict_in_str.find(";")
                                if i != -1 and ia != -1:
                                    item_name = got_item_dict_in_str[:ia]
                                    item_amount = int(got_item_dict_in_str[ia+1:i])
                                    got_item_dict |= {item_name:item_amount}
                                    got_item_dict_in_str = got_item_dict_in_str[i+1:]
                                elif i == -1 and ia != -1:
                                    item_name = got_item_dict_in_str[:ia]
                                    item_amount = int(got_item_dict_in_str[ia+1:])
                                    got_item_dict |= {item_name:item_amount}
                                    break
                                elif  ia == -1:
                                    break
                                else:
                                    print(f"DEBUG : i == {i}, ia == {ia}")
                                    raise
                            temp_len = g.LS.VOMIT_LOG(msg=self.VL_DIMS_PRESET, out=False, ret_len=True)
                            temp_preset = " " * temp_len
                            g.LS.LOGGING(msg=["", temp_preset+"< GOT ITEMS >"])
                            for item_name, item_amount in zip(got_item_dict.keys(), got_item_dict.values()):
#                                print(f"DEBUG : item_name == {item_name}, item_amount == {item_amount}")
                                g.LS.LOGGING(msg=temp_preset+f"{item_name} : +{item_amount}   |   "+str(self.STORAGE[item_name]["AMOUNT"]+item_amount)+" left")
                                self.GET_ITEM(item_name=item_name, item_amount=item_amount)
                            g.LS.LOGGING(msg="")
                            g.LS.PUSH()
                        case _:
                            pass