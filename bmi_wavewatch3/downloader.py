import gzip
import pathlib
import urllib
import urllib.request


class WaveWatch3Downloader:
    def __init__(self, url, force=False):
        self._url = url
        self._force = force
        self._filepath = None

    @staticmethod
    def url_file_part(url):
        return pathlib.Path(urllib.parse.urlparse(url).path).name

    @staticmethod
    def retreive(url, filename=None, reporthook=None, force=False):
        if filename is None:
            filename = WaveWatch3Downloader.url_file_part(url)
        if not pathlib.Path(filename).is_file() or force:
            filepath, _ = urllib.request.urlretrieve(
                url, reporthook=reporthook, data=None, filename=filename
            )
        else:
            filepath = filename

        filepath = pathlib.Path(filepath)
        if filepath.suffix == ".gz":
            filepath = WaveWatch3Downloader.unzip(filepath)
        return pathlib.Path(filepath).absolute()

    @staticmethod
    def unzip(filepath):
        filepath = pathlib.Path(filepath)
        with gzip.open(filepath, "rb") as zip_file:
            with open(filepath.stem, "wb") as fp:
                fp.write(zip_file.read())
        return pathlib.Path(filepath.stem)

    @property
    def filepath(self):
        return self._filepath

    @property
    def url(self):
        return self._url
