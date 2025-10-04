### ==========================================================================.
#
#
#   スケジュール管理.
#   デイリーミッションやイベントとかの優先度調整.
#
#
### ==========================================================================.


### ==========================================================================.
# import.

import os
import datetime
from json import load

from BASIC_SYS.basement import BASEMENT
from BASIC_SYS.loader import LOADER
from BASIC_SYS.saver import SAVER

from glov import *
from glov import glov_core as g

from BASIC_SYS.TRANS_STR2DATETIME import TRANS_STR2DATETIME
from GET_TIME import GET_TIME
from BASIC_SYS.alarm import ALARM

### ==========================================================================.

def NEW_URGENCY(old:int=0, new:int=1):
    g.LS.LOGGING(msg=[g.LS.COLOUR_WITH_CODE(RGB="FFFF00"),\
                      "/" * 80 + "\n",\
                      "/*n|*/ NOW URGENCY",\
                      "",\
                      f"{old} ---> {new}",\
                      g.LS.COLOUR_WITH_CODE(RGB="FFFF00"),\
                      "/" * 80,\
                      g.LS.COLOUR_WITH_CODE(RGB="")])
    g.LS.PUSH()


class SECRETARY(SAVER):
    def __init__(self):
        self.VL_SECT_PRESET = "/*n|*//*<SECT>*/ : "
        g.LS.VOMIT_LOG(msg=self.VL_SECT_PRESET+"/*st*/ACTIVE/*st_*/")

        self.PARENT:str
        self.SAVE_DIR:str

        self.FLAG_SET_DATA_ID:bool

        self.SCHEDULE_DIR:str

        self.SET_SCHEDULE_DIR()
        g.SYSTEM_URGENCY = 2

        g.LS.VOMIT_LOG(msg=self.VL_SECT_PRESET+"/*st*/LAUNCHED/*st_*/")

    def DECLARE_NEW_URGENCY(self, new:int=0):
        """
本来は出力先をプログラムの中枢とゲーム内情報の2つ用意したいんだけどな---.
        """
        NEW_URGENCY(new=new, old=g.SYSTEM_URGENCY)

    def SET_SCHEDULE_DIR(self):
        if self.FLAG_SET_DATA_ID:
            self.SCHEDULE_DIR = os.path.join(self.SAVE_DIR, "schedule")
            g.LS.VOMIT_LOG(msg=self.VL_SECT_PRESET+f"SET_SCHEDULE_DIR ; self.SCHEDULE_DIR == {self.SCHEDULE_DIR}")
            self.LOAD_SCHEDULE()
        else:
            pass


    def LOAD_SCHEDULE(self):
        _, self.SCHEDULE = LOADER(DIR=self.SCHEDULE_DIR, NAME="schedule.json")

        if not _:
            return
        self.LOAD_LAST_TIME()
        self.LOAD_END_TIME()
        self.LOAD_ENTRUST_INFO()
        self.__LOAD_STAMP()

    def LOAD_LAST_TIME(self):
        """
最後に~~をした時刻.

委託関連みたいな, 一定時間経過で達成するような内容の終了時間は別の部分が担当.
        """
        self.SECT_LAST_TIME = self.SCHEDULE["LAST_TIME"]
        # FIXME : 本当はここでself.SECT_FIRST_LOGIN_IN_A_DAYを宣言したかった. そうなれば__SECT_LOGIN, __LOAD_STAMP, __SECT_LOGIN_STAMPの位置が変わるかも.
        # TODO : ログボのチェックが日付変更じゃないアプリを考慮して, ログボチェックを跨いでいるかどうかの処理ができる関数を作らないといけない.


    def LOAD_END_TIME(self):
        """
一定時間経過で達成するような事象を担当.
        """
        def END_TIME(KEY_NAME:str=""):
            return self.SECT_END_TIME[KEY_NAME]
        self.SECT_END_TIME = self.SCHEDULE["END_TIME"]

        self.SECT_END_TIME_ENTRUST = END_TIME(KEY_NAME="ENTRUST")


    def LOAD_ENTRUST_INFO(self):
        """
委託関連のデータ読み込み.
        """
        NOW = GET_TIME()
        self.ENTRUST_NUM = 0 # 委託を受領した件数.
        self.ENTRUST_END_NUM = 0 # 既に終了済みの委託の件数.
        self.ENTRUST_END = [] # 委託が終了しているかどうかのフラグ.

        g.LS.VOMIT_LOG(msg=self.VL_SECT_PRESET+"ENTRUST PROGRESS/*l*/")
        temp_len = g.LS.VOMIT_LOG(msg=self.VL_SECT_PRESET, out=False, ret_len=True)
        temp_msg_prefix = " " * temp_len

        def SHOW_ENTRUST_INFO() -> bool:
            """
委託の情報出力.
返り値は委託が完了済みかどうか.
            """
            FLAG_FINISHED = True if (END_DATETIME - NOW).total_seconds() <= 0 else False # 終わったかどうか.
            g.LS.LOGGING(msg=[temp_msg_prefix+f"NAME : {NAME}",\
                              temp_msg_prefix+f"START_TIME : {START_TIME}",\
                              temp_msg_prefix+f"REQUIRED_TIME : {REQUIRED_TIME}"])

            temp_end_time_msg = temp_msg_prefix+f"END_TIME : {END_TIME} "
            if FLAG_FINISHED:
                temp_end_time_msg += g.LS.COLOUR_WITH_CODE(RGB="FFFF00") + "| Completed" + g.LS.COLOUR_WITH_CODE()
            else:
                temp_end_time_msg += g.LS.COLOUR_WITH_CODE(RGB="B0C4DE") + "| Incomplete" + g.LS.COLOUR_WITH_CODE()
            g.LS.LOGGING(msg=temp_end_time_msg)

            if len(REWARD) > 0:
                temp_msg_prefix4reward = " " * (temp_len+9)
                for i, r in enumerate(REWARD):
                    if i == 0:
                        g.LS.LOGGING(msg=temp_msg_prefix+f"REWARD : {r}")
                    else:
                        g.LS.LOGGING(msg=temp_msg_prefix4reward+r)
            g.LS.LOGGING(msg="")
            g.LS.PUSH()
            return FLAG_FINISHED

        def SHOW_RESULT():
            """
委託全体の結果.
            """
            g.LS.LOGGING(msg=[temp_msg_prefix+"< RESULT>",\
                              temp_msg_prefix+f"{self.ENTRUST_END_NUM} / {self.ENTRUST_NUM} ({self.ENTRUST_END_NUM/self.ENTRUST_NUM*100:.1f}%)",\
                              ""])
            g.LS.PUSH()

        with open(os.path.join(self.SCHEDULE_DIR, "entrust.json"), mode="r", encoding="utf-8") as f:
            self.ENTRUST_DATA = load(f)
#        _, self.ENTRUST_DATA = LOADER(DIR=self.SCHEDULE_DIR, NAME="entrust.json")
#        if not _:
#            g.LS.VOMIT_LOG(msg=self.VL_SECT_PRESET+"SHOW_RESULT ; /*e*/FAILED TO LOAD/*e_*/")
#            return
        self.ENTRUST_SCHEDULE = self.ENTRUST_DATA["ENTRUST"]

        for e in self.ENTRUST_SCHEDULE:
            NAME = e["NAME"] # 件名.
            START_TIME = e["START_TIME"] # 開始時刻.
            START_DATETIME = TRANS_STR2DATETIME(TIME=START_TIME)
            REQUIRED_TIME = e["REQUIRED_SECONDS"] # 所要時間. ただし単位は秒.
            REQUIRED_SECONDS = datetime.timedelta(seconds=float(REQUIRED_TIME))
            END_TIME = e["END_TIME"] # 終了予定時刻.
            END_DATETIME = TRANS_STR2DATETIME(TIME=END_TIME)
            REWARD = e["REWARD"] # 報酬.

            RES = SHOW_ENTRUST_INFO()
            self.ENTRUST_NUM += 1
            if RES:
                self.ENTRUST_END_NUM += 1
                self.ENTRUST_END += [True]
            else:
                self.ENTRUST_END += [False]

        SHOW_RESULT()



    def __LOAD_STAMP(self):
        self.STAMP = self.SCHEDULE["STAMP"]

    def __SECT_LOGIN_STAMP(self):
        self.STAMP["COUNTER"] += 1
        self.LOGIN_STAMP_COUNTER = self.STAMP["COUNTER"]


    def RESET_LOGIN_STAMP(self):
        """
TODO : make this function.
        """
        pass


    def __SECT_LOGIN(self): # ログボ獲得処理.
        if self.SECT_NEXT_TIME["LOGIN_BONUS"] == "":
            g.LS.VOMIT_LOG(msg=self.VL_SECT_PRESET+"IN schedule.json, NEXT_TIME -> LOGIN_BONUS IS NONE")
            self.SECT_NEXT_TIME["LOGIN_BONUS"] = str(GET_TIME())
            g.LS.VOMIT_LOG(msg=self.VL_SECT_PRESET+"SET LOGIN_BONUS")
        self.SECT_NEXT_TIME_LOGIN_BONUS = TRANS_STR2DATETIME(TIME=self.SECT_NEXT_TIME["LOGIN_BONUS"])
        self.LOGIN_BONUS_TIMER = ALARM(scheduled_time=self.SECT_NEXT_TIME_LOGIN_BONUS)

        self.SECT_FIRST_LOGIN_IN_A_DAY = self.LOGIN_BONUS_TIMER.PASSED_CHECK()
        if self.SECT_FIRST_LOGIN_IN_A_DAY:
            g.LS.VOMIT_LOG(self.VL_SECT_PRESET+"RECEIVE LOGIN BONUS")
            self.SECT_NEXT_TIME["LOGIN_BONUS"] = str(self.SECT_NEXT_TIME_LOGIN_BONUS + datetime.timedelta(days=1)) # FIXME : 次のログボチェックを算出する関数を作る.
            self.__SECT_LOGIN_STAMP()

    def LOAD_NEXT_TIME(self):
        """
何かができるようになる日時.
        """
        self.SECT_NEXT_TIME = self.SCHEDULE["NEXT_TIME"]
        self.__SECT_LOGIN()


    def UPDATE_SYSTEM_URGENCY(self):
        i = 0
        while self.SCHEDULE_URGENCY_LIST[-i] == 0: # -i <- ここ重要.
            i += 1
        if g.SYSTEM_URGENCY != i:
            self.DECLARE_NEW_URGENCY(new=i)
            g.SYSTEM_URGENCY = i

    def MAKE_APPOINTMENT(self):
        self.SCHEDULE_LIST = [[] for i in range(16)]
        self.SCHEDULE_URGENCY_LIST = [0 for i in range(16)] # 緊急度ごとの作業件数. [重要 <--------> 重要でない] なことに注意.
        g.SYSTEM_URGENCY

    def SAVE_SCHEDULE(self):
        self.SAVE_SUB_DATA(DATA=self.SCHEDULE, SAVE_DIR=self.SCHEDULE_DIR, NAME="schedule.json")