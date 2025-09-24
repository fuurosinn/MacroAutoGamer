### ==========================================================================.
#
#   core.
#
### ==========================================================================.


### ==========================================================================.
# import.

from app.app_package import *
from glov import *

import cv2
import numpy as np
import os
from json import load
from copy import deepcopy
from time import sleep

from BASIC_SYS.basement import BASEMENT
from BASIC_SYS.dimensionar import DIMENSIONAR
from BASIC_SYS.storage import STORAGE_MANAGER
from BASIC_SYS.shop import SHOP
from BASIC_SYS.btn import BTN

from BASIC_SYS.clerk import CLERK
from BASIC_SYS.saver import SAVER

from BASIC_SYS.secretary import SECRETARY

### ==========================================================================.

# CONFIG.DATA_DIRがGAME_INFO_DIR, GAME_INFO_NAMEなどの情報を含んでいる.
# ただしDATA_IDはセーブデータを表しているのでCONFIG内部には記述されない.

class module(BASEMENT, DIMENSIONAR, BTN, STORAGE_MANAGER, SECRETARY):
    def __init__(self, app_name:str="APP_MODULE", DATA_ID:int|str="0"):
        """
DATA_ID : セーブデータの番号.

SYSTEMにはゲームシステムなどに関する情報も含まれている.
例えば倉庫という概念が存在するのかどうかとか.
コインやスタミナなど、ホーム画面に常に表示されるような要素など.
        """
        self.app_name = app_name
        self.LOG_PRESET = f"/*n|*//*<{self.app_name}>*/ "
        self.ACTIVATED()
        self.LOAD_IMGS()

        self.SET_SAVE_NUM(DATA_ID=DATA_ID)

        BASEMENT.__init__(self, PARENT=self.app_name, DATA_ID=self.DATA_ID)
        DIMENSIONAR.__init__(self)
        BTN.__init__(self)
#        STORAGE_MANAGER.__init__(self) # 任意.
#        SHOP.__init__(self) # 任意.
        SECRETARY.__init__(self)

    def SET_SAVE_NUM(self, DATA_ID:int|str="0"):
        self.DATA_ID = str(DATA_ID) # DATA_IDと同義.

    def PUSH_BOOT_LOG(self):
        g.LS.VOMIT_LOG(msg=self.LOG_PRESET+"BOOTED")

    def ACTIVATED(self):
        self.PUSH_BOOT_LOG()
        g.SYSTEM_URGENCY = 1
        g.RESET_APPLICATION()
        g.SET_SCREENSHOT_PATH()
        gC.CONT.GET_SCREENCAP()
        if self.SEARCH_AND_TAP(btn_name="", t=3):
            self.LOG_IO(MODE="LOGIN") # 起動成功.
        else:
            pass # 起動失敗.

    def DEACTIVATED(self):
        self.LOG_IO(MODE="LOGOUT")
        g.SYSTEM_URGENCY = 0

    def TRY_ACTIVATE_APP(self):
        pass

    def MATCH(self, temp_addr:str=""):
        gC.CONT.GET_SCREENCAP() # gI.IMG_SCREENSHOT_GRAY 更新.
        gC.CONT.LOAD_TEMPLATE_IMG(addr=temp_addr) # gI.TEMP_MATCH_GRAY 更新.

    def WAIT_APP_BOOTUP(self):
        pass

    """
    def TAP_SCREEN(self, x:int=0, y:int=0, t:float=0.5):
        gC.CONT.cmd(command=f"nox_adb shell input touchscreen tap {x} {y}")
        sleep(t)
    """

    def LOAD_IMGS(self, addr:str="BTNS.json"):
        g.LS.VOMIT_LOG(msg=self.LOG_PRESET+f"LOADING IMGS ( {addr} )")
        with open(os.path.join(g.APP_CORE_PATH, addr)) as f:
            IMGS_LIST = load(f)
        LOADED_IMGS_DICT = {}

        TRIAL_LOADING_IMG = 0
        SUCCESSED = 0

        for DIR, NAME in zip(IMGS_LIST.keys(), IMGS_LIST.values()):
            TEMP_NAMES = []
            TEMP_IMGS = []
            for nam in NAME:
                LOADING_IMG_NAME = DIR + "__" + nam + ".png"
                TRIAL_LOADING_IMG += 1
                PATH = os.path.join(g.APP_IMGS_DIR, LOADING_IMG_NAME)
                if os.path.exists(path=PATH):
                    TEMP_IMGS.append(cv2.imread(PATH))
                    TEMP_NAMES.append(LOADING_IMG_NAME)
                    SUCCESSED += 1
                    g.LS.VOMIT_LOG(msg=" "*len(self.LOG_PRESET)+f"\033[36m[SUCCESS]\033[0m TO LOAD {LOADING_IMG_NAME}")
                else:
                    g.LS.VOMIT_LOG(msg=" "*len(self.LOG_PRESET)+f"/*e*/ FAILED TO LOAD {LOADING_IMG_NAME}")
            LOADED_IMGS_DICT.update(dict(zip(TEMP_NAMES, TEMP_IMGS)))
        gI.IMGS.update(LOADED_IMGS_DICT)
        g.LS.VOMIT_LOG(msg=self.LOG_PRESET+f"LOADED IMGS < {SUCCESSED} / {TRIAL_LOADING_IMG} >/*l*/")

    def SEARCH_AND_TAP(self, btn_name:str="", t:float=0.5):
        if btn_name == "":
            return False
        gC.CONT.GET_SCREENCAP()
        gI.TEMP_MATCH = gI.IMGS[btn_name+".png"]
        gI.TEMP_MATCH_GRAY = cv2.cvtColor(gI.TEMP_MATCH, cv2.COLOR_BGR2GRAY)
        gC.CONT.SEARCH_TEMPLATE_IMG(acc=0.8)
        if gI.MATCH_TEMPLATE_RES_X == -1 or gI.MATCH_TEMPLATE_RES_Y == -1:
            return False
        gC.CONT.TAP_SCREEN(t=t)
#        self.TAP_SCREEN(x=gI.MATCH_TEMPLATE_RES_X, y=gI.MATCH_TEMPLATE_RES_Y, t=t)
        return True



    def COMFIRM_ATTAIN_MISSION(self):
        """
任務の進捗などを加算.
        """
        pass

    def DAILY_MISSION(self):
        """
デイリーミッション実行.
        """
        pass

    def MISSION(self):
        self.DAILY_MISSION()

    def LOOP(self):
        self.MAKE_APPOINTMENT()
        pass