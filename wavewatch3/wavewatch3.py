import pathlib
import shutil
import tempfile
import urllib
from datetime import datetime

import requests
import xarray as xr
from tqdm import tqdm


class WaveWatch3Downloader:
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

    def __init__(self, url, lazy_load=False, clobber=False):
        self._url = url
        self._clobber = clobber
        self._filepath = None
        self._data = None

        if not lazy_load:
            self.data

    @classmethod
    def from_params(cls, date=None, region="glo_30m", quantity="hs", **kwds):
        return cls(
            WaveWatch3Downloader.data_url(date=date, region=region, quantity=quantity),
            **kwds,
        )

    @staticmethod
    def data_url(date=None, region="glo_30m", quantity="hs"):
        if region not in WaveWatch3Downloader.REGIONS:
            raise ValueError(f"{region!r}: unknown region")
        if quantity not in WaveWatch3Downloader.QUANTITIES:
            raise ValueError(f"{quantity!r}: unknown quantity")

        date = datetime.today() if date is None else datetime.fromisoformat(date)

        prefix = pathlib.PosixPath(f"{date.year}/{date.month:02d}")
        prefix /= region if date.year < 2017 else "gribs"

        path = str(
            WaveWatch3Downloader.PREFIX
            / prefix
            / f"multi_1.{region}.{quantity}.{date.year}{date.month:02d}.grb2"
        )

        return urllib.parse.urlunparse(
            [WaveWatch3Downloader.SCHEME, WaveWatch3Downloader.NETLOC, path, "", "", ""]
        )

    @staticmethod
    def fetch(url, destination=None, clobber=True, progress_bar=True):
        destination = pathlib.Path("." if destination is None else destination)
        name = pathlib.Path(urllib.parse.urlparse(url).path).name
        progress = silent_progress_bar if progress_bar is None else tqdm

        if destination.is_dir():
            destination /= name

        if destination.is_file() and not clobber:
            raise ValueError(f"{destination}: file exists")

        resp = requests.get(url, stream=True)
        resp.raise_for_status()

        total_size_in_bytes = int(resp.headers.get("content-length", 0))
        with tempfile.TemporaryDirectory() as tmpdirname:
            filepath = pathlib.Path(tmpdirname) / name
            with open(filepath, "wb") as fp:
                with progress(total=total_size_in_bytes, leave=True) as pbar:
                    for chunk in resp.iter_content(chunk_size=1024):
                        fp.write(chunk)
                        pbar.update(len(chunk))
            shutil.move(filepath, destination)

        return destination.absolute()

    @staticmethod
    def load(filepath):
        return xr.load_dataset(filepath, engine="cfgrib")

    @property
    def data(self):
        if self._data is None:
            self._filepath = WaveWatch3Downloader.fetch(
                self._url, clobber=self._clobber
            )
            self._data = WaveWatch3Downloader.load(self._filepath)
        return self._data

    @property
    def filepath(self):
        return self._filepath

    @property
    def url(self):
        return self._url


class silent_progressbar(object):
    def __init__(self, **kwds):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        pass

    def update(self, inc):
        pass
