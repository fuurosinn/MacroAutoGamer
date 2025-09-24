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

from BASIC_SYS.basement import BASEMENT
from BASIC_SYS.loader import LOADER
from BASIC_SYS.saver import SAVER

from glov import *

### ==========================================================================.


class SECRETARY(BASEMENT, SAVER):
    def __init__(self):
        self.PARENT:str
        self.SAVE_DIR:str
        self.SCHEDULE_DIR:str = os.path.join(self.SAVE_DIR, "schedule")
        self.LOAD_SCHEDULE()
        g.SYSTEM_URGENCY = 2

    def LOAD_SCHEDULE(self):
        self.SCHEDULE = LOADER(DIR=self.SCHEDULE_DIR, NAME="schedule.json")

    def UPDATE_SYSTEM_URGENCY(self):
        i = 0
        while self.SCHEDULE_URGENCY_LIST[-i] == 0: # -i <- ここ重要.
            i += 1
        g.SYSTEM_URGENCY = i

    def MAKE_APPOINTMENT(self):
        self.SCHEDULE_LIST = []
        self.SCHEDULE_URGENCY_LIST = [0 for i in range(16)] # 緊急度ごとの作業件数. [重要 <--------> 重要でない] なことに注意.
        g.SYSTEM_URGENCY