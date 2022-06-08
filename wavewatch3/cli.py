import inspect
import itertools
import os
import pathlib
import sys
import textwrap
import urllib
from collections import namedtuple
from functools import partial
from multiprocessing import Pool, RLock

import click
from tqdm.auto import tqdm
from .downloader import WaveWatch3Downloader
from .errors import ChoiceError, DateValueError
from .source import SOURCES


out = partial(click.secho, bold=True, file=sys.stderr)
err = partial(click.secho, fg="red", file=sys.stderr)


DownloadResult = namedtuple("DownloadResult", ["remote", "local", "success", "status"])


def validate_date(ctx, param, value):
    source = SOURCES[ctx.parent.params["source"]]

    for date_str in value:
        try:
            source.validate_date(date_str)
        except DateValueError as error:
            raise click.BadParameter(error)
    return value


def validate_quantity(ctx, param, value):
    source = SOURCES[ctx.parent.params["source"]]
    if not value:
        return sorted(source.QUANTITIES)

    for quantity in value:
        try:
            source.validate_quantity(quantity)
        except ChoiceError as error:
            raise click.BadParameter(error)
    return value


def validate_grid(ctx, param, value):
    source = SOURCES[ctx.parent.params["source"]]
    if not value:
        return inspect.signature(source).parameters["grid"].default

    try:
        source.validate_grid(value)
    except ChoiceError as error:
        raise click.BadParameter(error)
    return value


@click.group(chain=True)
@click.version_option()
@click.option(
    "--cd",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True),
    help="chage to directory, then execute",
)
@click.option(
    "-s",
    "--silent",
    is_flag=True,
    help="Suppress status status messages, including the progress bar.",
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Also emit status messages to stderr."
)
@click.option(
    "--source",
    type=click.Choice(sorted(SOURCES)),
    default="multigrid",
    help="WAVEWATCH III data source",
)
def ww3(cd, silent, verbose, source) -> None:
    """Download WAVEWATCH III data.

    \b
    Examples:

      Download WAVEWATCH III data by date,

        $ ww3 fetch 2010-05-22 2010-05-22
    """
    os.chdir(cd)


@ww3.command()
@click.option("--all", is_flag=True, help="info on all sources")
@click.pass_context
def info(ctx, all):
    source = ctx.parent.params["source"]
    sources = SOURCES if all else {source: SOURCES[source]}

    sections = []
    for name, source in sources.items():
        endpoint = urllib.parse.urlunparse(
            [source.SCHEME, source.NETLOC, source.PREFIX, "", "", ""]
        )
        sections.append(
            textwrap.dedent(
                f"""
                [wavewatch3.sources.{name}]
                grids = {sorted(source.GRIDS)!r}
                quantities = {sorted(source.QUANTITIES)!r}
                min_date = {source.MIN_DATE!r}
                max_date = {source.MAX_DATE!r}
                endpoint = {endpoint!r}"""
            ).lstrip()
        )

    print((2 * os.linesep).join(sections))


@ww3.command()
@click.argument("date", nargs=-1, callback=validate_date)
@click.option("--grid", default=None, help="Grid to download", callback=validate_grid)
@click.option(
    "--quantity",
    "-q",
    multiple=True,
    help="Quantity to download",
    callback=validate_quantity,
)
@click.pass_context
def url(ctx, date, grid, quantity):
    """Construct URLs from which to download WAVEWATCH III data."""
    Source = SOURCES[ctx.parent.params["source"]]

    for d in date:
        for q in quantity:
            print(Source(d, q, grid=grid))


@ww3.command()
@click.argument("date", nargs=-1, callback=validate_date)
@click.option("--dry-run", is_flag=True, help="do not actually download data")
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="force download even if local file already exists",
)
@click.option("--file", type=click.File("r", lazy=False), help="read dates from a file")
@click.option("--grid", default=None, help="Grid to download", callback=validate_grid)
@click.option(
    "--quantity",
    "-q",
    multiple=True,
    help="Quantity to download",
    callback=validate_quantity,
)
@click.pass_context
def fetch(ctx, date, dry_run, force, file, grid, quantity):
    """Download WAVEWATCH III data by date."""
    verbose = ctx.parent.params["verbose"]
    silent = ctx.parent.params["silent"]
    Source = SOURCES[ctx.parent.params["source"]]

    if file:
        date += file.read().splitlines()

    urls = [str(Source(d, q, grid=grid)) for q in quantity for d in date]

    if not silent and verbose:
        for url in urls:
            out(url)

    if not dry_run:
        results = _retreive_urls(urls, disable=silent, force=force)

        if not silent:
            [
                out(f"{result.status}: {result.local}")
                for result in results
                if result.success and result.status
            ]
        [
            err(f"{result.status}: {result.remote}")
            for result in results
            if not result.success
        ]

        [print(result.local) for result in results if result.success]


@ww3.command()
@click.option("--dry-run", is_flag=True, help="only display what would have been done")
@click.option(
    "--cache-dir",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
    help="cache folder to clean",
    default="~/.wavewatch3/data",
)
@click.option("--yes", is_flag=True, help="remove files without prompting")
@click.pass_context
def clean(ctx, dry_run, cache_dir, yes):
    """Remove cached date files."""
    verbose = ctx.parent.params["verbose"]
    silent = ctx.parent.params["silent"]

    source = "multi_*"
    grid = "*"
    quantity = "*"
    date = "*"

    cache_dir = cache_dir.expanduser()
    cache_files = list(
        itertools.chain(
            cache_dir.glob(f"{source}.{grid}.{quantity}.{date}.grb2"),
            cache_dir.glob(f"{source}.{grid}.{quantity}.{date}.grb2.gz"),
            cache_dir.glob(f"{source}.{grid}.{quantity}.{date}.grb2.*.idx"),
            cache_dir.glob(f"{grid}.{quantity}.{date}.grb"),
            cache_dir.glob(f"{grid}.{quantity}.{date}.grb.*.idx"),
        )
    )

    total_bytes = sum([cache_file.stat().st_size for cache_file in cache_files])

    if not silent and not dry_run:
        for cache_file in cache_files:
            out(f"{cache_file}")
        out(f"Total size: {total_bytes // 2**20} MB")

    if not dry_run and len(cache_files):
        yes = yes or click.confirm(
            "Are you sure you want to remove all files?", abort=True
        )

    for cache_file in cache_files:
        cache_file.unlink() if not dry_run else out(f"rm {cache_file}")

    if not dry_run and (verbose and not silent):
        out(f"Removed {len(cache_files)} files ({total_bytes} bytes)")


def _retreive_urls(urls, disable=False, force=False):
    tqdm.set_lock(RLock())
    p = Pool(initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),))
    return p.map(
        partial(_retreive, disable=disable, force=force), list(enumerate(urls))
    )


def _retreive(position_and_url, disable=False, force=False):
    position, url = position_and_url
    name = pathlib.Path(urllib.parse.urlparse(url).path).name

    if not pathlib.Path(name).is_file() or force:
        with TqdmUpTo(
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            miniters=1,
            desc=name,
            position=position,
            disable=disable,
            leave=False,
        ) as t:
            try:
                WaveWatch3Downloader.retreive(
                    url, filename=name, reporthook=t.update_to, force=force
                )
            except (urllib.error.HTTPError, urllib.error.URLError) as error:
                success, status = False, str(error)
            else:
                t.total = t.n
                success, status = True, f"downloaded {t.total} bytes"
    else:
        success, status = True, "cached"

    return DownloadResult(
        local=pathlib.Path(name).absolute(), remote=url, success=success, status=status
    )


class TqdmUpTo(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize
