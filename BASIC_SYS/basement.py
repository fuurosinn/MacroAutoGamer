### ==========================================================================.
#
#
#   基本機能のさらに中枢部分.
#
#
### ==========================================================================.


### ==========================================================================.
# import.

from loader import LOADER
from glov.glov_core import LS
from json import load, dump
import os

from GET_TIME import GET_TIME

### ==========================================================================.


### ==========================================================================.
# BASEMENT.

class BASEMENT():
    def __init__(self, PARENT:str="NOTHING", DATA_ID:str=""):
        """
基底データ読み込み.

PARENT : 親クラスのログ上での名称. <gC> とか.

GAME_INFO_DIR : ゲームの様々な情報が記述されたファイルが格納されたディレクトリ.
GAME_INFO_NAME : 使用するファイルの名称.

GAME_DIR : ゲーム名ごとのデータ保管ディレクトリ.
DATA_ID : データ名.
        """
        self.PARENT = PARENT

        # =====================================.

        with open("./CONFIG/DATA_DIR.json") as f:
            self.DATA_DIR = load(f)[self.PARENT]

        self.GAME_INFO_DIR = self.DATA_DIR["GAME_INFO_DIR"] # この2変数でゲームの様々な情報を読み込む.
        self.GAME_INFO_NAME = self.DATA_DIR["GAME_INFO_NAME"]

        self.GAME_DIR = self.DATA_DIR["GAME_DIR"] # この2変数でセーブデータの情報を読み込む.
        self.DATA_ID = DATA_ID
        self.SAVE_DIR = os.path.join(self.GAME_DIR, self.DATA_ID) # セーブデータが格納されているディレクトリ.

        # =====================================.

        with open(f"./game_info/{self.PARENT}/sys.json", mode="r") as f:
            self.SYSTEM = load(f) # ゲームシステム関連.

        self.SYSTEM_CHARA = self.SYSTEM["CHARA"] # キャラが存在するかどうか.
        self.SYSTEM_CHARA_EXIST = self.SYSTEM_CHARA["EXIST"]
        if self.SYSTEM_CHARA_EXIST:
            self.SYSTEM_CHARA_CAPA_LIMIT = self.SYSTEM_CHARA["CAPA_LIMIT"] # キャラの所持数上限があるかどうか.
            self.SYSTEM_CHARA_EXP = self.SYSTEM_CHARA["EXP"] # 経験値システムがあるか. 一気にレベルアップじゃなくて, 100expまで溜まったらレベルアップみたいなの.

        if self.SYSTEM_CHARA_EXIST:
            self.SYSTEM_GACHA = self.SYSTEM["CACHA"] # ガチャ.

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


        # ======================================.


        RES, self.INFO = LOADER(DIR=self.GAME_INFO_DIR, NAME=self.GAME_INFO_NAME)
        if RES: # ゲーム情報読み込み.
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ | GAME INFO LOADED SUCCESSFULLY.")
        else:
            LS.VOMIT_LOG(msg="/*n|*//*<STORAGE>*/ | /*e*/FAILED TO LOAD GAME INFO./*e_*/")


    def LOG_RECORD(self, matter:str="", cate:str="LOG", show:bool=True, l:int=1):
        """
なんかあったらログに記録する.
matter ; str : 内容.
cate ; str : <>の内部.
show ; bool : Trueならログにも表示.
l ; int : 改行数. 通常は1.
        """
        FLAG_CATE_IS_EXIST = False if cate in ("", None) else True
        NEW_LINE_TEMP = "\n" * l
        with open(os.path.join(self.SAVE_DIR, "logs.txt", mode="w"), encoding="utf-8") as f:
            if FLAG_CATE_IS_EXIST:
                f.write(f"{GET_TIME()} | {cate} : {matter}" + NEW_LINE_TEMP)
            else:
                f.write(f"{GET_TIME()} : {matter}" + NEW_LINE_TEMP)
        if show:
            if FLAG_CATE_IS_EXIST:
                LS.VOMIT_LOG(msg=f"/*n|*//*<{cate}>*/ | {matter}" + NEW_LINE_TEMP)
            else:
                LS.VOMIT_LOG(msg=f"/*n|*/ | {matter}" + NEW_LINE_TEMP)

    def LOG_IO(self, MODE:str="LOG"):
        """
MODEにLOGINかLOGOUTを記述.
        """
        self.LAST_LOG_DATA = LOADER(DIR=self.SAVE_DIR, NAME="log.json")
        self.LAST_LOG_DATA["LAST_"+MODE] = GET_TIME()
        with open(os.path.join(self.SAVE_DIR, "log.json"), mode="w", encoding="unicode-escape") as f:
            dump(self.LAST_LOG_DATA, f, indent=4, ensure_ascii=False)
        self.LOG_RECORD(matter=MODE, cate="SYSTEM", l=5)