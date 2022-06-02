import datetime
import pathlib
import urllib

from .errors import ChoiceError


class WaveWatch3URL:
    SCHEME = "https"
    NETLOC = "www.ncei.noaa.gov"
    PREFIX = "/thredds-ocean/fileServer/ncep/nww3"

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
    QUANTITIES = {"wind", "hs", "tp", "dp"}

    def __init__(self, date, quantity, region="glo_30m"):
        self._date = datetime.date.fromisoformat(date)
        self._quantity = None
        self._region = None

        self.quantity = quantity
        self.region = region

    def __str__(self):
        prefix = pathlib.PosixPath(f"{self.year}/{self.month:02d}")
        prefix /= self.region if self.year < 2017 else "gribs"

        return urllib.parse.urlunparse(
            [
                WaveWatch3URL.SCHEME,
                WaveWatch3URL.NETLOC,
                str(WaveWatch3URL.PREFIX / prefix / self.filename),
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
        if region not in WaveWatch3URL.REGIONS:
            raise ChoiceError(region, WaveWatch3URL.REGIONS)
        self._region = region

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        if quantity not in WaveWatch3URL.QUANTITIES:
            raise ChoiceError(quantity, WaveWatch3URL.QUANTITIES)
        self._quantity = quantity

    @property
    def year(self):
        return self._date.year

    @property
    def month(self):
        return self._date.month

    @property
    def filename(self):
        return f"multi_1.{self.region}.{self.quantity}.{self.year}{self.month:02d}.grb2"
