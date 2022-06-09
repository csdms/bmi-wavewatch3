import datetime
import itertools
import random
import urllib

import pytest

import bmi_wavewatch3 as ww3


def url_exists(url):
    try:
        with urllib.request.urlopen(url) as resp:
            status_code = resp.status
    except (urllib.error.HTTPError, urllib.error.URLError):
        return False
    else:
        return status_code == 200


def random_date(lower, upper):
    lower = datetime.date.fromisoformat(lower)
    upper = datetime.date.fromisoformat(upper)

    range = (upper - lower).days

    return (lower + datetime.timedelta(random.randrange(range))).isoformat()


@pytest.mark.parametrize(
    "source,grid,quantity",
    [
        (_source,) + _grid_and_quantity
        for _source in ww3.SOURCES.values()
        for _grid_and_quantity in itertools.product(_source.GRIDS, _source.QUANTITIES)
    ],
)
def test_url(source, grid, quantity):
    date = datetime.date.fromisoformat(source.MIN_DATE)
    url = source(date.isoformat(), quantity, grid=grid)
    assert url.year == date.year
    assert url.month == date.month
    assert url.quantity == quantity
    assert url.grid == grid
    assert f"{grid}.{quantity}.{date.year}{date.month:02}.grb" in url.filename


@pytest.mark.parametrize(
    "source,grid,quantity",
    [
        (
            _source,
            random.choice(list(_source.GRIDS)),
            random.choice(list(_source.QUANTITIES)),
        )
        for _source in itertools.filterfalse(
            lambda cls: cls in (ww3.SOURCES["phase1"], ww3.SOURCES["singlegrid"]),
            ww3.SOURCES.values(),
        )
    ],
)
def test_url_exists(source, grid, quantity):
    """Spot check that urls exist"""
    for date in [
        source.MIN_DATE,
        source.MAX_DATE,
        random_date(source.MIN_DATE, source.MAX_DATE),
    ]:
        url = source(date, quantity, grid=grid)
        assert url_exists(str(url))


@pytest.mark.parametrize("source", ww3.SOURCES.values())
def test_date_ranges(source):
    for date in [
        source.MIN_DATE,
        source.MAX_DATE,
        random_date(source.MIN_DATE, source.MAX_DATE),
    ]:
        date = datetime.datetime.fromisoformat(date)

        url = source(date.isoformat(), random.choice(list(source.QUANTITIES)))
        assert url.date == date.isoformat(timespec="hours")

        url = source(
            date.isoformat(timespec="hours"), random.choice(list(source.QUANTITIES))
        )
        assert url.date == date.isoformat(timespec="hours")


@pytest.mark.parametrize(
    "source,quantity",
    [
        (_source, _quantity)
        for _source in ww3.SOURCES.values()
        for _quantity in _source.QUANTITIES
    ],
)
def test_url_default_grid(source, quantity):
    url = source(source.MIN_DATE, quantity)
    assert url.grid in source.GRIDS


@pytest.mark.parametrize("source", ww3.SOURCES.values())
def test_url_str(source):
    url = source(source.MIN_DATE, "wind")
    assert str(url).startswith(source.SCHEME)


@pytest.mark.parametrize("source", ww3.SOURCES.values())
def test_url_repr(source):
    import bmi_wavewatch3  # noqa

    url = source(source.MIN_DATE, "tp")
    assert eval(repr(url)) == url


@pytest.mark.parametrize("source", ww3.SOURCES.values())
def test_url_quantity_setter(source):
    url = source(source.MIN_DATE, "tp")
    url.quantity = "dp"
    assert url.quantity == "dp"
    assert url == source(source.MIN_DATE, "dp")

    with pytest.raises(ww3.ChoiceError):
        url.quantity = "foo"


@pytest.mark.parametrize("source", ww3.SOURCES.values())
def test_url_grid_setter(source):
    url = source(source.MIN_DATE, "tp")
    for grid in source.GRIDS:
        url.grid = grid
        assert url == source(source.MIN_DATE, "tp", grid=grid)

    with pytest.raises(ww3.ChoiceError):
        url.grid = "bar"
