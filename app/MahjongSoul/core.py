from app.app_package import *
from app.app_module.core import module

from time import sleep

class mahjongsoul(module):
    def __init__(self):
        super().__init__(app_name="MahjongSoul")
        self.LOOP()

    def LOOP(self):
        pass