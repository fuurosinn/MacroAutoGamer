# ============================================================================.
#
# -*- coding: utf-8 -*-
#
# ============================================================================.

from subprocess import run, PIPE
import os

from glov import glov_core as g
from glov import glov_log as gL
from glov import glov_img as gI

from json import load
import cv2
import numpy as np

from time import sleep

class controll():
    def __init__(self):
        self.SETUP()

    def SETUP(self):
        pass
#        g.SYSTEM_BOOT_DIR



# ============================================================================.
# < START > | コマンド関連.


    def cmd(self, command:str=""):
        if gL.LOG_DEBUG_ADB:
            g.LS.VOMIT_LOG(msg=f"/*n|*//*<NOX_ADB>*/ \033[31m{command}\033[0m")
        result = run(command, stdout=PIPE, shell=True, cwd=g.SYSTEM_NOX_DIR, text=True, encoding="utf-8", timeout=10)
        return result.stdout


# テキストファイルからADB command実行.
    def EXE_ADB_IN_TXT(self, txt_dir:str=""):
        with open(txt_dir, mode="r") as f:
            CMDS = load(f)
        for cmd in CMDS:
            self.cmd(command=cmd)


# < END > | コマンド関連.
# ============================================================================.



# ============================================================================.
# < START > | スクショ.


    def GET_SCREENCAP(self, region:tuple=((0, 1920), (0, 960))): # スクショ撮影.
        self.cmd(command=f"nox_adb shell screencap -p {g.SYSTEM_NOX_SCREENCAP_DIR}")
        self.cmd(command=f"nox_adb pull {g.SYSTEM_NOX_SCREENCAP_DIR} {g.APP_SCREENSHOT_PATH}")
        gI.IMG_SCREENSHOT = cv2.imread(g.APP_SCREENSHOT_IMG_PATH)
        gI.IMG_SCREENSHOT_GRAY = cv2.cvtColor(gI.IMG_SCREENSHOT, cv2.COLOR_BGR2GRAY)


# < END > | スクショ.
# ============================================================================.



# ============================================================================.
# < START > | 画像読み込み.


    def LOAD_TEMPLATE_IMG(self, addr:str=""):
        """
addr : 探索したいアイテム名, ボタン名, etc...
.pngは付けてもいいが, 省略しても.pngを自動的に付与するので問題無い.
        """
        gI.TEMP_NAME = addr
        if all(len(addr) < len(ext) or addr[-len(ext):] != ext for ext in gI.IMG_EXTENSION): # 拡張子が省略されているか判断.
            addr += ".png"

        if gL.LOG_DEBUG_IMREAD:
            g.LS.VOMIT_LOG(msg=f"/*n|*//*<gC>*/ IMREAD TEMPLATE, {addr}")
        gI.TEMP_MATCH = cv2.imread(os.path.join(g.APP_IMGS_DIR, addr))
        gI.TEMP_MATCH_GRAY = cv2.cvtColor(gI.TEMP_MATCH, cv2.COLOR_BGR2GRAY)


# < END > | 画像読み込み.
# ============================================================================.



# ============================================================================.
# < START > | 画像の座標探索.


    def SEARCH_TEMPLATE_IMG(self, acc:float=0.8):
        """
タップまではしない.
ただ単に画像の存在位置(中心)を探すだけ.

事前にGET_SCREENCAP()でスクショ撮影->読み込みと, LOAD_TEMPLATE_IMG()で探索対象の画像を取り込む必要がある.

acc < float > : 精確性, 閾値.
        """
        # gI.IMG_SCREENSHOT_GRAY.
        TEMP_HEIGHT, TEMP_WIDTH = gI.TEMP_MATCH_GRAY.shape[:2]
        RES = cv2.matchTemplate(gI.IMG_SCREENSHOT_GRAY, gI.TEMP_MATCH_GRAY, cv2.TM_CCOEFF_NORMED)
        LOC = np.where(RES >= acc)
        try:
            gI.MATCH_TEMPLATE_RES_X = LOC[1][0] + TEMP_WIDTH / 2
            gI.MATCH_TEMPLATE_RES_Y = LOC[0][0] + TEMP_HEIGHT / 2
        except:
            gI.MATCH_TEMPLATE_RES_X = -1
            gI.MATCH_TEMPLATE_RES_Y = -1


# < END > | 画像の座標探索.
# ============================================================================.
# < START > | 実際の操作.


    def TAP_SCREEN(self, t:int|float=0.5):
        self.cmd(command=f"nox_adb shell input touchscreen tap {gI.MATCH_TEMPLATE_RES_X} {gI.MATCH_TEMPLATE_RES_Y}")
        sleep(t)

# < END > | 実際の操作.