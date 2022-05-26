import datetime
import os

import click
from .wavewatch3 import WaveWatch3Downloader


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
def ww3(cd, silent, verbose) -> None:
    os.chdir(cd)


@ww3.command()
@click.argument("date", nargs=-1)
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
def url(date, region, quantity):
    if not date:
        date = [datetime.datetime.today().isoformat()]
    if not quantity:
        quantity = sorted(WaveWatch3Downloader.QUANTITIES)
    for d in date:
        for q in quantity:
            print(WaveWatch3Downloader.data_url(date=d, quantity=q, region=region))


@ww3.command()
@click.argument("date", nargs=-1)
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
@click.option(
    "--dry-run",
    type=click.Choice(sorted(WaveWatch3Downloader.QUANTITIES)),
    multiple=True,
    help="Quantity to download",
)
@click.option("--dry-run", is_flag=True, help="do not actually download data")
def fetch(date, region, quantity, dry_run):
    if not date:
        date = ["2005-02-01"]
    if not quantity:
        quantity = sorted(WaveWatch3Downloader.QUANTITIES)
    downloaders = []
    for d in date:
        for q in quantity:
            downloaders.append(
                WaveWatch3Downloader(
                    WaveWatch3Downloader.data_url(date=d, quantity=q, region=region),
                    clobber=False,
                    lazy_load=True,
                )
            )

    for downloader in downloaders:
        print(downloader.url)
        if not dry_run:
            downloader.data
