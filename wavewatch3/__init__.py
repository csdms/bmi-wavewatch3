from ._version import __version__
from .bmi import BmiWaveWatch3
from .downloader import WaveWatch3Downloader
from .url import WaveWatch3URL
from .errors import ChoiceError, WaveWatch3Error

__all__ = [
    "__version__",
    "BmiWaveWatch3",
    "ChoiceError",
    "WaveWatch3Downloader",
    "WaveWatch3Error",
    "WaveWatch3URL",
]
