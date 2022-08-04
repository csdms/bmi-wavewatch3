from ._version import __version__
from .bmi import BmiWaveWatch3
from .downloader import WaveWatch3Downloader
from .errors import ChoiceError, WaveWatch3Error
from .source import SOURCES
from .wavewatch3 import WaveWatch3


__all__ = [
    "__version__",
    "BmiWaveWatch3",
    "ChoiceError",
    "SOURCES",
    "WaveWatch3",
    "WaveWatch3Downloader",
    "WaveWatch3Error",
]
