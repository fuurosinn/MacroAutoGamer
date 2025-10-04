### ==========================================================================.
#
#
#   ある時刻が既に過ぎているかどうか.
#
#
### ==========================================================================.


### ==========================================================================.
# import.

import datetime
from BASIC_SYS.TRANS_STR2DATETIME import TRANS_STR2DATETIME
from GET_TIME import GET_TIME

### ==========================================================================.

class ALARM():
    def __init__(self, scheduled_time:str|datetime.timedelta=""):
        self.SET_ALARM(scheduled_time=scheduled_time)
        self.LAST_CHECK = None # 最後に問い合わせがあった時刻.
        self.TIME_OVER:bool = self.PASSED_CHECK() # 既に経過したかどうか.
        self.REMAINING_TIME = None # 最終問い合わせ時刻時点での残り時間.

    def SET_ALARM(self, scheduled_time:str|datetime.timedelta=""):
        if type(scheduled_time) == str:
            self.st = TRANS_STR2DATETIME(TIME=scheduled_time)
        elif type(scheduled_time) == datetime.datetime:
            self.st = scheduled_time

    def PASSED_CHECK(self) -> bool:
        """
もう既に設定時刻を過ぎたかどうか.
        """
        self.LAST_CHECK = GET_TIME()
        self.REMAINING_TIME = self.st - self.LAST_CHECK
        if self.REMAINING_TIME.total_seconds() > 0:
            return False
        else:
            return True