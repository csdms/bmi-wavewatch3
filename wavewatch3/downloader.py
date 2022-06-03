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
        return pathlib.Path(filepath).absolute()

    @property
    def filepath(self):
        return self._filepath

    @property
    def url(self):
        return self._url
