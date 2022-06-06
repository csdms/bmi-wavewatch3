import datetime
import itertools

import pytest

import wavewatch3 as ww3


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
    import wavewatch3  # noqa

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
