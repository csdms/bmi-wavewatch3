import datetime
import os
import pathlib
import sys
import urllib
from functools import partial
from multiprocessing import Pool, RLock

import click
import dask.bag as db
from tqdm.auto import tqdm
from .downloader import WaveWatch3Downloader

out = partial(click.secho, bold=True, file=sys.stderr)
err = partial(click.secho, fg="red", file=sys.stderr)


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
    "--region",
    type=click.Choice(sorted(WaveWatch3Downloader.REGIONS)),
    default="glo_30m",
    help="Region to download",
)
@click.option(
    "--quantity",
    "-q",
    type=click.Choice(sorted(WaveWatch3Downloader.QUANTITIES)),
    multiple=True,
    help="Quantity to download",
)
def ww3(cd, silent, verbose, region, quantity) -> None:
    os.chdir(cd)


@ww3.command()
@click.argument("date", nargs=-1)
@click.pass_context
def url(ctx, date):
    region = ctx.parent.params["region"]
    quantity = ctx.parent.params["quantity"]

    if not quantity:
        quantity = sorted(WaveWatch3Downloader.QUANTITIES)
    for d in date:
        for q in quantity:
            print(WaveWatch3Downloader.data_url(date=d, quantity=q, region=region))


@ww3.command()
@click.argument("date", nargs=-1)
@click.option("--dry-run", is_flag=True, help="do not actually download data")
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="force download even if local file already exists",
)
@click.option("--file", type=click.File("r", lazy=False), help="read url from a file")
@click.pass_context
def fetch(ctx, date, dry_run, force, file):
    verbose = ctx.parent.params["verbose"]
    silent = ctx.parent.params["silent"]
    region = ctx.parent.params["region"]
    quantity = ctx.parent.params["quantity"]

    if not quantity:
        quantity = sorted(WaveWatch3Downloader.QUANTITIES)

    if file:
        date += file.read().splitlines()

    urls = []
    for d in date:
        for q in quantity:
            urls.append(
                WaveWatch3Downloader.data_url(date=d, quantity=q, region=region)
            )

    if not silent and verbose:
        for url in urls:
            out(url)

    if not dry_run:
        local_files = _retreive_urls(urls, disable=silent, force=force)
        for local_file in local_files:
            print(local_file.absolute())


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
        ) as t:
            filepath = WaveWatch3Downloader.retreive(
                url, filename=name, reporthook=t.update_to
            )
            t.total = t.n
    else:
        out(f"cached: {name}")

    return pathlib.Path(name).absolute()


class TqdmUpTo(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize
