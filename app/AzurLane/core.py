from app.app_package import *
from app.app_module.core import module

from time import sleep

class azurlane(module):
    def __init__(self):
        super().__init__(app_name="AzurLane")
        self.LOOP()

    def LOOP(self):
        def OPEN__SIDEMENU():
            g.LS.VOMIT_LOG(msg=LOG_LOOP_PRESET+"OPEN SIDEMENU")
            self.TAP_SCREEN(x=17, y=293, t=3)
        def GET_ITEMS_IN_SIDEMENU():
            g.LS.VOMIT_LOG(msg=LOG_LOOP_PRESET+"GET ITEMS IN SIDEMENU")
            Y = 80
            for i in range(3):
                self.TAP_SCREEN(x=177+215*i, y=Y, t=0.5)
            sleep(1)
            self.TAP_SCREEN(x=960, y=540, t=1.5)
        def GET_ITEMS_IN_MISSION():
            g.LS.VOMIT_LOG(msg=LOG_LOOP_PRESET+"GET ITEMS IN MISSION")
            self.SEARCH_AND_TAP(btn_name="HOME__MISSIONS", t=3)
            self.TAP_SCREEN(x=1340, y=36, t=1.5)
            self.TAP_SCREEN(x=71, y=66, t=1.5)
            while self.SEARCH_AND_TAP(btn_name="MISSIONS__BACK", t=1.5):
                self.TAP_SCREEN(x=66, y=66, t=1)

        LOG_LOOP_PRESET = f"/*n|*//*<{self.app_name}-LOOP>*/ "
        g.LS.VOMIT_LOG(msg=LOG_LOOP_PRESET+"START")
#        OPEN__SIDEMENU()
#        GET_ITEMS_IN_SIDEMENU()
        GET_ITEMS_IN_MISSION()