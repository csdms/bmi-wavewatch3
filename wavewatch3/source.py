import datetime
import pathlib
import urllib

from .errors import ChoiceError


class _WaveWatch3Source:
    SCHEME = "https"
    NETLOC = ""
    PREFIX = ""

    GRIDS = {
        "glo_30m",
        "ao_30m",
        "at_10m",
        "wc_10m",
        "ep_10m",
        "ak_10m",
        "at_4m",
        "wc_4m",
        "ak_4m",
    }
    QUANTITIES = {"wind", "hs", "tp", "dp"}
    MIN_DATE = None
    MAX_DATE = None

    def __init__(self, date, quantity, grid="glo_30m"):
        self._date = None
        self._quantity = None
        self._grid = None

        self.date = date
        self.quantity = quantity
        self.grid = grid

    @property
    def path(self):
        raise NotImplementedError("path")

    @property
    def filename(self):
        raise NotImplementedError("filename")

    def __str__(self):
        return urllib.parse.urlunparse(
            [
                self.SCHEME,
                self.NETLOC,
                str(self.path),
                "",
                "",
                "",
            ]
        )

    def __repr__(self):
        date = self._date.isoformat()
        return f"{self.__class__.__module__}.{self.__class__.__name__}({date!r}, {self.quantity!r}, grid={self.grid!r})"

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, grid):
        if grid not in self.GRIDS:
            raise ChoiceError(grid, self.GRIDS)
        self._grid = grid

    @property
    def date(self):
        return self._date.isoformat()

    @date.setter
    def date(self, date):
        if self.MIN_DATE and date < self.MIN_DATE:
            raise ValueError("date is less than minimum date for this dataset")
        if self.MAX_DATE and date > self.MAX_DATE:
            raise ValueError("date is greater than maximum date for this dataset")
        self._date = datetime.date.fromisoformat(date)

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        if quantity not in self.QUANTITIES:
            raise ChoiceError(quantity, self.QUANTITIES)
        self._quantity = quantity

    @property
    def year(self):
        return self._date.year

    @year.setter
    def year(self, year):
        self._date = datetime.date(year, self.month, self._date.day)

    @property
    def month(self):
        return self._date.month

    @month.setter
    def month(self, month):
        self._date = datetime.date(self.year, month, self._date.day)


class WaveWatch3SourcePhase1(_WaveWatch3Source):
    """
    https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase1.php
    """

    SCHEME = "https"
    NETLOC = "polar.ncep.noaa.gov"
    PREFIX = "/waves/hindcasts/nopp-phase1"

    GRIDS = {
        "ak_4m",
        "ak_10m",
        "ecg_4m",
        "ecg_10m",
        "glo_30m_ext",
        "med_10m",
        "nsb_4m",
        "nsb_10m",
        "nwio_10m",
        "oz_4m",
        "oz_10m",
        "pi_10m",
        "wc_4m",
        "wc_10m",
    }

    MIN_DATE = "1979-01-01"
    MAX_DATE = "2009-12-31"

    def __init__(self, date, quantity, grid="glo_30m_ext"):
        super().__init__(date, quantity, grid=grid)

    @property
    def path(self):
        path = (
            self.PREFIX / pathlib.PurePosixPath(f"{self.year}{self.month:02d}") / "grib"
        )
        return path / self.filename

    @property
    def filename(self):
        return f"multi_reanal.{self.grid}.{self.quantity}.{self.year}{self.month:02d}.grb2.gz"


class WaveWatch3SourcePhase2(_WaveWatch3Source):
    """
    https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase2.php
    """

    SCHEME = "https"
    NETLOC = "polar.ncep.noaa.gov"
    PREFIX = "/waves/hindcasts/nopp-phase2"

    GRIDS = {
        "ak_4m",
        "ak_10m",
        "ecg_4m",
        "ecg_10m",
        "glo_30m_ext",
        "med_10m",
        "nsb_4m",
        "nsb_10m",
        "nwio_10m",
        "oz_4m",
        "oz_10m",
        "pi_10m",
        "wc_4m",
        "wc_10m",
    }

    MIN_DATE = "1979-01-01"
    MAX_DATE = "2009-12-31"

    def __init__(self, date, quantity, grid="glo_30m_ext"):
        super().__init__(date, quantity, grid=grid)

    @property
    def path(self):
        path = (
            self.PREFIX
            / pathlib.PurePosixPath(f"{self.year}{self.month:02d}")
            / "gribs"
        )
        return path / self.filename

    @property
    def filename(self):
        return (
            f"multi_reanal.{self.grid}.{self.quantity}.{self.year}{self.month:02d}.grb2"
        )


class WaveWatch3SourceMultigrid(_WaveWatch3Source):
    """
    https://polar.ncep.noaa.gov/waves/hindcasts/prod-multi_1.php
    """

    SCHEME = "https"
    NETLOC = "polar.ncep.noaa.gov"
    PREFIX = "/waves/hindcasts/multi_1"

    MIN_DATE = "2005-02-01"
    MAX_DATE = "2019-05-31"

    @property
    def path(self):
        path = (
            self.PREFIX
            / pathlib.PurePosixPath(f"{self.year}{self.month:02d}")
            / "gribs"
        )
        return path / self.filename

    @property
    def filename(self):
        return f"multi_1.{self.grid}.{self.quantity}.{self.year}{self.month:02d}.grb2"


class WaveWatch3SourceMultigridExt(_WaveWatch3Source):
    """
    https://polar.ncep.noaa.gov/waves/hindcasts/prod-multi_1.php
    """

    SCHEME = "https"
    NETLOC = "polar.ncep.noaa.gov"
    PREFIX = "/waves/hindcasts/multi_1"

    GRIDS = {
        "glo_30m",
        "ao_30m",
        "at_10m",
        "wc_10m",
        "ep_10m",
        "ak_10m",
        "at_4m",
        "wc_4m",
        "ak_4m",
    }
    QUANTITIES = {"wind", "hs", "tp", "dp", "phs", "ptp", "pdir"}  # added 2017 onward

    MIN_DATE = "2017-02-01"
    MAX_DATE = "2019-05-31"

    @property
    def path(self):
        path = (
            self.PREFIX
            / pathlib.PurePosixPath(f"{self.year}{self.month:02d}")
            / "gribs"
        )
        return path / self.filename

    @property
    def filename(self):
        return f"multi_1.{self.grid}.{self.quantity}.{self.year}{self.month:02d}.grb2"


class WaveWatch3SourceThredds(_WaveWatch3Source):
    SCHEME = "https"
    NETLOC = "www.ncei.noaa.gov"
    PREFIX = "/thredds-ocean/fileServer/ncep/nww3"

    MIN_DATE = "2005-02-01"
    MAX_DATE = "2019-05-31"

    @property
    def path(self):
        path = self.PREFIX / pathlib.PurePosixPath(f"{self.year}", f"{self.month:02d}")
        path /= self.grid if self.year < 2017 else "gribs"
        return path / self.filename

    @property
    def filename(self):
        return f"multi_1.{self.grid}.{self.quantity}.{self.year}{self.month:02d}.grb2"


class WaveWatch3SourceNww3(_WaveWatch3Source):
    """
    https://polar.ncep.noaa.gov/waves/hindcasts/prod-nww3.php
    """

    SCHEME = "https"
    NETLOC = "polar.ncep.noaa.gov"
    PREFIX = "/waves/hindcasts/nww3"

    GRIDS = {"akw", "enp", "nah", "nph", "nww3", "wna"}

    MIN_DATE = "1999-07-01"
    MAX_DATE = "2006-09-30"

    def __init__(self, date, quantity, grid="nww3"):
        super().__init__(date, quantity, grid=grid)

    @property
    def path(self):
        return pathlib.PurePosixPath(self.PREFIX) / self.filename

    @property
    def filename(self):
        return f"{self.grid}.{self.quantity}.{self.year}{self.month:02d}.grb"


SOURCES = {
    "multigrid": WaveWatch3SourceMultigrid,
    "multigrid-extended": WaveWatch3SourceMultigridExt,
    "multigrid-thredds": WaveWatch3SourceThredds,
    "phase1": WaveWatch3SourcePhase1,
    "phase2": WaveWatch3SourcePhase2,
}
