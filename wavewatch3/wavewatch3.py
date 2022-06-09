import contextlib
import datetime
import os
import pathlib
from functools import partial
from multiprocessing import Pool

import numpy as np
import xarray as xr
from dateutil.relativedelta import relativedelta

from .downloader import WaveWatch3Downloader
from .errors import ChoiceError
from .source import SOURCES


class WaveWatch3:
    def __init__(
        self,
        date,
        grid="glo_30m",
        cache="~/.wavewatch3/data",
        lazy=True,
        source="multigrid",
    ):
        """Advance through WAVEWATCH III data, downloading new data as needed.

        Parameters
        ----------
        date : str
            Date as an isoformatted string ("YYYY-MM-DD").
        grid : str, optional
            WAVEWATCH III grid region.
        cache : str or path-like, optional
            Folder into which to cache downloaded data.
        lazy : bool, optional
            If ``True``, wait to download data until the xarray Dataset is first accessed.
        source : str, optional
            Source from which to download data from.
        """
        try:
            Source = SOURCES[source]
        except KeyError:
            raise ChoiceError(source, SOURCES)
        self._source = source
        self._cache = pathlib.Path(cache).expanduser()
        self._lazy = lazy
        self._data = None
        self._date = None
        self._step = 0

        self._urls = [
            Source(date, quantity=quantity, grid=grid) for quantity in Source.QUANTITIES
        ]
        self.date = date
        if not lazy:
            self._load_data()

    @property
    def data(self):
        """Current WAVEWATCH III data as an xarray.Dataset."""
        if self._data is None:
            self._load_data()
        return self._data

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, step):
        if step < 0:
            raise ValueError("step must be non-negative")

        if step < len(self.data.step):
            self._step = step
            self.date = str(
                (self.data.time + self.data.step[step]).values.astype("datetime64[h]")
            )
        else:
            remaining = step - len(self._data.step)
            self.inc()
            self.step = remaining

    @property
    def source(self):
        """Source from which data will be downloaded."""
        return self._source

    @property
    def grid(self):
        """The WAVEWATCH III grid region."""
        return self._urls[0].grid

    @property
    def date(self):
        """Current date as an isoformatted string."""
        return self._date.isoformat(timespec="hours")

    @date.setter
    def date(self, date):
        new_date = datetime.datetime.fromisoformat(date)
        if new_date != self._date:
            self._date = new_date
            for url in self._urls:
                url.month = new_date.month
                url.year = new_date.year
            self._data = None
            if not self._lazy:
                self._load_data()

    @property
    def year(self):
        """The current year."""
        return self._date.year

    @property
    def month(self):
        """The current month."""
        return self._date.month

    @property
    def day(self):
        return self._date.day

    @property
    def hour(self):
        return self._date.hour

    def inc(self, months=1):
        """Increment to current date by some number of months.

        Parameters
        ----------
        months : int, optional
            Number of months to increment the date by.
        """
        self.date = (self._date + relativedelta(months=months)).isoformat()

    def _load_data(self):
        """Load the current data into an xarray Dataset."""
        self._fetch_data()
        self._data = xr.open_mfdataset(
            [self._cache / url.filename for url in self._urls],
            engine="cfgrib",
            parallel=True,
        )
        self._step = np.searchsorted(
            self._data.step, np.datetime64(self.date, "ns") - self._data.time
        )

    def _fetch_data(self):
        """Download data in parallel."""
        self._cache.mkdir(parents=True, exist_ok=True)
        with as_cwd(self._cache):
            Pool().map(WaveWatch3Downloader.retreive, [str(url) for url in self._urls])

    def __repr__(self):
        """String representation of a WaveWatch3 instance."""
        return f"WaveWatch3({self.date!r}, grid={self.grid!r}, source={self.source!r})"

    def __eq__(self, other):
        """Test if two WaveWatch3 instances refer to the same data."""
        return (
            self.month == other.month
            and self.year == other.year
            and self.grid == other.grid
            and self.source == other.source
        )

    @staticmethod
    def fetch(date, folder=".", force=False, grid="glo_30m", source="multigrid"):
        """Fetch WAVEWATCH III data by date.

        Parameters
        ----------
        date : str or iterable of str
            Date or list of dates isoformat strings ("YYYY-MM-DD").
        folder : str or path-like, optional
            Destination folder into which to download data.
        force : bool, optional
            If ``True`` download the data even if the file to be downloaded
            already exists in the destination folder.
        grid : str, optional
            The WAVEWATCH III grid to download.

        Returns
        -------
        list of path-like
            The downloaded (or cached) data files.
        """
        dates = [date] if isinstance(date, str) else date
        folder = pathlib.Path(folder)

        try:
            Source = SOURCES[source]
        except KeyError:
            raise ChoiceError(source, SOURCES)

        urls = []
        for date in dates:
            urls += [
                Source(date, quantity=quantity, grid=grid)
                for quantity in Source.QUANTITIES
            ]

        with as_cwd(folder):
            Pool().map(
                partial(WaveWatch3Downloader.retreive, force=force),
                [str(url) for url in urls],
            )

        return sorted([folder / url.filename for url in urls])


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
