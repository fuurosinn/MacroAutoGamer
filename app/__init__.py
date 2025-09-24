from app.VANITAS.core import VANITATUM # 起動時にglovでACTIVATE_APPLICATION_INSTANCEを埋めるための奴.
from app.app_module.core import module
from app.AzurLane.core import azurlane
from app.MahjongSoul.core import mahjongsoul
from app.StarSeed.core import starseed

__all__ = ["VANITATUM", "module", "azurlane", "mahjongsoul", "starseed"]