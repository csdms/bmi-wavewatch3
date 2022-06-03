import datetime
import pathlib
import urllib

from .errors import ChoiceError


class WaveWatch3URLBase:
    SCHEME = "https"
    NETLOC = ""
    PREFIX = ""

    REGIONS = {
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
    QUANTITIES = {"wind", "hs", "tp", "dp"}  # phs, ptp, pdir added 2017 onward

    def __init__(self, date, quantity, region="glo_30m"):
        self._date = datetime.date.fromisoformat(date)
        self._quantity = None
        self._region = None

        self.quantity = quantity
        self.region = region

    def __str__(self):
        return urllib.parse.urlunparse(
            [
                self.SCHEME,
                self.NETLOC,
                str(self.path),
                # str(WaveWatch3URL.PREFIX / self.path / self.filename),
                "",
                "",
                "",
            ]
        )

    def __repr__(self):
        date = self._date.isoformat()
        return f"WaveWatch3URL({date!r}, {self.quantity!r}, region={self.region!r})"

    def __eq__(self, other):
        return str(self) == str(other)

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, region):
        if region not in self.REGIONS:
            raise ChoiceError(region, self.REGIONS)
        self._region = region

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


class WaveWatch3URL(WaveWatch3URLBase):
    SCHEME = "https"
    NETLOC = "polar.ncep.noaa.gov"
    PREFIX = "/waves/hindcasts/multi_1"

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
        return f"multi_1.{self.region}.{self.quantity}.{self.year}{self.month:02d}.grb2"


class WaveWatch3URLThredds(WaveWatch3URLBase):
    SCHEME = "https"
    NETLOC = "www.ncei.noaa.gov"
    PREFIX = "/thredds-ocean/fileServer/ncep/nww3"

    @property
    def path(self):
        path = self.PREFIX / pathlib.PurePosixPath(f"{self.year}", f"{self.month:02d}")
        path /= self.region if self.year < 2017 else "gribs"
        return path / self.filename

    @property
    def filename(self):
        return f"multi_1.{self.region}.{self.quantity}.{self.year}{self.month:02d}.grb2"


class WaveWatch3URLOld(WaveWatch3URLBase):
    SCHEME = "https"
    NETLOC = "polar.ncep.noaa.gov"
    PREFIX = "/waves/hindcasts/nww3"

    REGIONS = {"akw", "enp", "nah", "nph", "nww3", "wna"}

    def __init__(self, date, quantity, region="nww3"):
        super().__init__(date, quantity, region=region)

    @property
    def path(self):
        return pathlib.PurePosixPath(self.PREFIX) / self.filename

    @property
    def filename(self):
        return f"{self.region}.{self.quantity}.{self.year}{self.month:02d}.grb"
