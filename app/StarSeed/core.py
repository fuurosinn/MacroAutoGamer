from app.app_package import *
from app.app_module.core import module

from time import sleep



class starseed(module):
    def __init__(self):
        super().__init__(app_name="StarSeed", DATA_ID=0)
        self.LOOP()

    def MOVE_BATTLE(self):
        pass

    def DAILY_MISSION(self):
        pass

    def LOOP(self):
        LOG_LOOP_PRESET = f"/*n|*//*<{self.app_name}-LOOP>*/ "
        g.LS.VOMIT_LOG(msg=LOG_LOOP_PRESET+"START")