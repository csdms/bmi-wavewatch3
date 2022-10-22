"""Download and cache a WAVEWATCH III data file."""
import gzip
import pathlib
import urllib
import urllib.request


class WaveWatch3Downloader:
    """Download a WAVEWATCH III data file from a URL."""

    def __init__(self, url, force=False):
        """Create a downloader.

        Parameters
        ----------
        url : str
            Location of the file to download.
        force : bool, optional
            Download the file even if a cached file already exists.
        """
        # self._url = url
        self._force = force
        # self._filepath = None

    @staticmethod
    def url_file_part(url):
        """Return the file part of a url."""
        return pathlib.Path(urllib.parse.urlparse(url).path).name

    @staticmethod
    def retreive(url, filename=None, reporthook=None, force=False):
        """Fetch a file from a URL.

        Parameters
        ----------
        url : str
            Location of the file to download.
        filename : str, optional
            Name of the local file to save the download file to. If not
            provided, use the name of the remote file.
        reporthook : func, optional
            Function used for reporting download status. The function
            signature is the same as that of :func:`urllib.request.urlretrieve`
        force : bool, optional
            Download the file even if a cached file already exists.

        Returns
        -------
        pathlib.Path
            Absolute path to the downloaded file.
        """
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
        """Unzip a file.

        Parameters
        ----------
        filepath : str or path-like
            Path to the file to unzip.

        Returns
        -------
        str
           Name of the unzipped file.
        """
        filepath = pathlib.Path(filepath)
        with gzip.open(filepath, "rb") as zip_file:
            with open(filepath.stem, "wb") as fp:
                fp.write(zip_file.read())
        return pathlib.Path(filepath.stem)

    # @property
    # def filepath(self):
    #     """Return the name of the local file."""
    #     return self._filepath

    # @property
    # def url(self):
    #     return self._url
