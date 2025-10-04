### ==========================================================================.
#
#
#   基本機能のさらに中枢部分.
#
#
### ==========================================================================.


### ==========================================================================.
# import.

from BASIC_SYS.loader import LOADER
from glov import glov_core as g
from glov.glov_core import LS
from json import load, dump
import os

from GET_TIME import GET_TIME

### ==========================================================================.


### ==========================================================================.
# BASEMENT.

class BASEMENT:
    def __init__(self, PARENT:str="NOTHING", DATA_ID:str=""):
        """
基底データ読み込み.

PARENT : 親クラスのログ上での名称. <gC> とか.

GAME_INFO_DIR : ゲームの様々な情報が記述されたファイルが格納されたディレクトリ.
GAME_INFO_NAME : 使用するファイルの名称.

GAME_DIR : ゲーム名ごとのデータ保管ディレクトリ.
DATA_ID : データ名.
        """
        self.VL_BASEMENT_PRESET = "/*n|*//*<BASEMENT>*/ : " # VOMIT_BASEMENT_LOGで繰り返し使用する最初の部分.
        LS.VOMIT_LOG(msg=self.VL_BASEMENT_PRESET+"/*st*/ACTIVE/*st_*/")
        self.PARENT = PARENT
        self.FLAG_SET_DATA_ID:bool = False if DATA_ID == "" else True
        self.LOAD_INFO()
        LS.VOMIT_LOG(msg=self.VL_BASEMENT_PRESET+"/*st*/LAUNCHED/*st_*/")

    def LOAD_INFO(self):
        with open("./CONFIG/DATA_DIR.json") as f:
            self.DATA_DIR = load(f)[self.PARENT]

        self.GAME_INFO_DIR = self.DATA_DIR["GAME_INFO_DIR"] # この2変数でゲームの様々な情報を読み込む.
        self.GAME_INFO_NAME = self.DATA_DIR["GAME_INFO_NAME"]
        self.GAME_DIR = self.DATA_DIR["GAME_DIR"] # この2変数でセーブデータの情報を読み込む.
        self.BOOKLET_DIR = self.DATA_DIR["BOOKLET_DIR"]
        self.LOAD_SYSTEM()

#    def TRANS_ID2NAME(self, ID:str="") -> str:
#        LS.VOMIT_LOG(msg=self.VL_BASEMENT_PRESET+"/*e*/TRANS_ID2NAME HAS NOT YET BEEN OVERRIDDEN/*e_*/")
#        TEMP = ID
#        return

    def LOAD_DELTA_TIME(self):
        """
オーバーライドされること前提のクラス.
オーバーライドしてもBASEMENT.LOAD_DELTA_TIME(self)を先に実行する必要がある.
ある行動をしてからの時間を知りたい場合に利用する.
例 : スターシードの作戦報酬獲得の貯蔵量を計算.
        """
        LS.VOMIT_LOG(msg=self.VL_BASEMENT_PRESET+"LOAD_DELTA_TIME ; START LOADING...")
        with open(os.path.join(self.SAVE_DIR, "log.json"), mode="r", encoding="unicode-escape") as f:
            self.LAST_LOG_DATA = load(f)
        self.LAST_LOGIN = self.LAST_LOG_DATA["LAST_LOGIN"]
        self.LAST_LOGOUT = self.LAST_LOG_DATA["LAST_LOGOUT"]
        LS.VOMIT_LOG(msg=self.VL_BASEMENT_PRESET+"LOAD_DELTA_TIME ; LOADED")

    def SET_DATA_ID(self, ID:str=""):
        NAME = self.TRANS_ID2NAME(ID=ID)
        if NAME == None: # account_bookletを実装後に「ID参照しても存在しない場合」に変更. <--- しました.
            LS.VOMIT_LOG(msg=self.VL_BASEMENT_PRESET+"/*c*/SET_DATA_ID() ; INVALID ID/*c_*/")
            self.FLAG_SET_DATA_ID:bool = False
            self.DATA_ID = "" # <--- 有効なDATA_IDが指定済みでも, 無効なIDを指定しまうと指定が解除されることに注意.
            self.SAVE_NAME = ""
            self.SAVE_DIR = ""
            return
        self.FLAG_SET_DATA_ID:bool = True
        self.DATA_ID = ID
        self.SAVE_NAME = NAME
        self.SAVE_DIR = os.path.join(self.GAME_DIR, self.SAVE_NAME) # セーブデータが格納されているディレクトリ.

        self.LOAD_DELTA_TIME()

        LS.VOMIT_LOG(msg=self.VL_BASEMENT_PRESET+f"SET_DATA_ID() ; SET ID == {ID}")


    def LOAD_SYSTEM(self):
        with open(f"./game_info/{self.PARENT}/sys.json", mode="r") as f:
            self.SYSTEM = load(f) # ゲームシステム関連.

        self.SYSTEM_CHARA = self.SYSTEM["CHARA"] # キャラが存在するかどうか.
        self.SYSTEM_CHARA_EXIST = self.SYSTEM_CHARA["EXIST"]
        if self.SYSTEM_CHARA_EXIST:
            self.SYSTEM_CHARA_CAPA_LIMIT = self.SYSTEM_CHARA["CAPA_LIMIT"] # キャラの所持数上限があるかどうか.
            self.SYSTEM_CHARA_EXP = self.SYSTEM_CHARA["EXP"] # 経験値システムがあるか. 一気にレベルアップじゃなくて, 100expまで溜まったらレベルアップみたいなの.

        self.SYSTEM_GACHA = self.SYSTEM["GACHA"] # ガチャ.
        self.SYSTEM_GACHA_EXIST = self.SYSTEM_GACHA["EXIST"]

        self.SYSTEM_STORAGE = self.SYSTEM["STORAGE"] # 倉庫関連.
        self.SYSTEM_STORAGE_EXIST = self.SYSTEM_STORAGE["EXIST"] # 倉庫システムが存在するかどうか.
        if self.SYSTEM_STORAGE_EXIST:
            self.SYSTEM_STORAGE_CAPA_LIMIT = self.SYSTEM_STORAGE["CAPA_LIMIT"] # 容量上限が存在するかどうか.

        self.SYSTEM_MONEY = self.SYSTEM["MONEY"] # 金.
        self.SYSTEM_MONEY_EXIST = self.SYSTEM_MONEY["EXIST"] # 金がシステム上存在するかどうか.
        if self.SYSTEM_MONEY_EXIST:
            self.SYSTEM_MONEY_NAME = self.SYSTEM_MONEY["NAME"] # 名称.
            self.SYSTEM_MONEY_IS_ITEM = self.SYSTEM_MONEY["IS_ITEM"] # アイテムとして存在するかどうか.
            self.SYSTEM_MONEY_LIMIT = self.SYSTEM_MONEY["LIMIT"] # 貯蔵量上限. nullなら存在しない.

        self.SYSTEM_STAMINA = self.SYSTEM["STAMINA"] # スタミナ.
        self.SYSTEM_STAMINA_EXIST = self.SYSTEM_STAMINA["EXIST"]
        if self.SYSTEM_STAMINA_EXIST:
            self.SYSTEM_STAMINA_NAME = self.SYSTEM_STAMINA["NAME"]
            self.SYSTEM_STAMINA_IS_ITEM = self.SYSTEM_STAMINA["IS_ITEM"]
            self.SYSTEM_STAMINA_LIMIT = self.SYSTEM_STAMINA["LIMIT"]

        self.SYSTEM_JEM = self.SYSTEM["JEM"] # 意図的にjemの綴りにした. ガチャ石.
        self.SYSTEM_JEM_EXIST = self.SYSTEM_JEM["EXIST"]
        if self.SYSTEM_JEM_EXIST:
            self.SYSTE_JEM_NAME = self.SYSTEM_JEM["NAME"]
            self.SYSTEM_JEM_IS_ITE = self.SYSTEM_JEM["IS_ITEM"]
            self.SYSTEM_JEM_LIMIT = self.SYSTEM_JEM["LIMIT"]

        RES, self.INFO = LOADER(DIR=self.GAME_INFO_DIR, NAME=self.GAME_INFO_NAME)
        if RES: # ゲーム情報読み込み.
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ | GAME INFO LOADED SUCCESSFULLY.")
        else:
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ | /*e*/FAILED TO LOAD GAME INFO./*e_*/")


    def LOGIN(self):
        self.BTN_EXECUTOR(btn_name="SIGNIN") # ホーム画面に移動.
        self.LOG_IO(MODE="LOGIN")

    def LOGOUT(self):
        self.LOG_IO(MODE="LOGOUT")
        self.DATA_ID = ""
        self.SAVE_NAME = ""
        self.SAVE_DIR = ""

    def LOG_RECORD(self, matter:str="", cate:str="LOG", show:bool=True, l:int=1):
        """
なんかあったらログに記録する.
matter ; str : 内容.
cate ; str : <>の内部.
show ; bool : Trueならログにも表示.
l ; int : 改行数. 通常は1.
        """
        if not self.FLAG_SET_DATA_ID:
            raise
        FLAG_CATE_IS_EXIST = False if cate in ("", None) else True
        NEW_LINE_TEMP = "\n" * l
        with open(os.path.join(self.SAVE_DIR, "logs.txt"), encoding="utf-8", mode="a") as f:
            if FLAG_CATE_IS_EXIST:
                f.write(f"{GET_TIME()} | < {cate} > : {matter}" + NEW_LINE_TEMP)
            else:
                f.write(f"{GET_TIME()} : {matter}" + NEW_LINE_TEMP)
        if show:
            if FLAG_CATE_IS_EXIST:
                LS.VOMIT_LOG(msg=f"/*n|*//*<{cate}>*/ | {matter}")
            else:
                LS.VOMIT_LOG(msg=f"/*n|*/ | {matter}")

    def LOG_IO(self, MODE:str="LOG"):
        """
MODEにLOGINかLOGOUTを記述.
        """
        if not self.FLAG_SET_DATA_ID:
            raise
        self.LAST_LOG_DATA["LAST_"+MODE] = str(GET_TIME())
        with open(os.path.join(self.SAVE_DIR, "log.json"), mode="w", encoding="utf-8") as f:
            dump(self.LAST_LOG_DATA, f, indent=4, ensure_ascii=False)
        match MODE:
            case "LOGIN":
                self.LOG_RECORD(matter=f"{MODE} ; BOOT == {g.SYSTEM_BOOT_MODE}", cate=self.PARENT, l=1)
            case "LOGOUT":
                self.LOG_RECORD(matter=MODE, cate=self.PARENT, l=1)