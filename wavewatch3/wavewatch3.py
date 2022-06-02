import contextlib
import datetime
import os
import pathlib
from multiprocessing import Pool

import xarray as xr
from dateutil.relativedelta import relativedelta

from .downloader import WaveWatch3Downloader
from .url import WaveWatch3URL


class WaveWatch3:
    def __init__(self, date, region="glo_30m", cache="~/.wavewatch3/data", lazy=True):
        self._cache = pathlib.Path(cache).expanduser()
        self._lazy = lazy
        self._data = None
        self._date = None

        self._urls = [
            WaveWatch3URL(date, quantity=quantity, region=region)
            for quantity in WaveWatch3URL.QUANTITIES
        ]
        self.date = date
        if not lazy:
            self._load_data()

    @property
    def data(self):
        if self._data is None:
            self._load_data()
        return self._data

    @property
    def region(self):
        return self._urls[0].region

    @property
    def date(self):
        return self._date.isoformat()

    @date.setter
    def date(self, date):
        new_date = datetime.date.fromisoformat(date)
        if new_date != self._date:
            self._date = new_date
            for url in self._urls:
                url.month = new_date.month
                url.year = new_date.year
            if not self._lazy:
                self._load_data()

    @property
    def year(self):
        return self._date.year

    @property
    def month(self):
        return self._date.month

    def inc(self, months=1):
        self.date = (self._date + relativedelta(months=months)).isoformat()

    def _load_data(self):
        self._fetch_data()
        self._data = xr.open_mfdataset(
            [self._cache / url.filename for url in self._urls],
            engine="cfgrib",
            parallel=True,
        )

    def _fetch_data(self):
        self._cache.mkdir(parents=True, exist_ok=True)
        with as_cwd(self._cache):
            Pool().map(WaveWatch3Downloader.retreive, [str(url) for url in self._urls])

    def __repr__(self):
        date = self._urls[0]._date.isoformat()
        region = self._urls[0].region
        return f"WaveWatch3({date!r}, region={region!r})"

    def __eq__(self, other):
        return (
            self.month == other.month
            and self.year == other.year
            and self.region == other.region
        )


@contextlib.contextmanager
def as_cwd(path):
    """Change directory context.

    Args:
        path (str): Path-like object to a directory.
    """
    prev_cwd = pathlib.Path.cwd()
    os.chdir(path)
    yield prev_cwd
    os.chdir(prev_cwd)
