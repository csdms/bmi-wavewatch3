import itertools
import os
import pathlib
import sys
import urllib
from functools import partial
from multiprocessing import Pool, RLock

import click
from tqdm.auto import tqdm
from .downloader import WaveWatch3Downloader
from .url import WaveWatch3URL


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
    type=click.Choice(sorted(WaveWatch3URL.REGIONS)),
    default="glo_30m",
    help="Region to download",
)
@click.option(
    "--quantity",
    "-q",
    type=click.Choice(sorted(WaveWatch3URL.QUANTITIES)),
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
    quantity = ctx.parent.params["quantity"] or sorted(WaveWatch3URL.QUANTITIES)

    for d in date:
        for q in quantity:
            print(WaveWatch3URL(d, q, region=region))


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
    quantity = ctx.parent.params["quantity"] or sorted(WaveWatch3URL.QUANTITIES)

    if file:
        date += file.read().splitlines()

    urls = []
    for d in date:
        for q in quantity:
            urls.append(str(WaveWatch3URL(d, q, region=region)))

    if not silent and verbose:
        for url in urls:
            out(url)

    if not dry_run:
        local_files = _retreive_urls(urls, disable=silent, force=force)
        for local_file in local_files:
            print(local_file.absolute())


@ww3.command()
@click.option("--dry-run", is_flag=True, help="only display what would have been done")
@click.option(
    "--cache-dir",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
    help="cache folder to clean",
    default="~/.wavewatch3/data",
)
@click.option("--yes", is_flag=True, help="remove files without prompting")
# @click.confirmation_option(prompt="Are you sure you want to remove all cached files?")
@click.pass_context
def clean(ctx, dry_run, cache_dir, yes):
    verbose = ctx.parent.params["verbose"]
    silent = ctx.parent.params["silent"]

    region = "*"
    quantity = "*"
    date = "*"
    pattern = f"multi_1.{region}.{quantity}.{date}.grb2"

    cache_dir = cache_dir.expanduser()
    cache_files = list(
        itertools.chain(cache_dir.glob(pattern), cache_dir.glob(pattern + ".*.idx"))
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
        if dry_run:
            out(f"rm {cache_file}")
        else:
            cache_file.unlink()

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
        ) as t:
            WaveWatch3Downloader.retreive(url, filename=name, reporthook=t.update_to)
            t.total = t.n
    else:
        out(f"cached: {name}")

    return pathlib.Path(name).absolute()


class TqdmUpTo(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        return self.update(b * bsize - self.n)  # also sets self.n = b * bsize
