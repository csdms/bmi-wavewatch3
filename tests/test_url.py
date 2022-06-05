import pytest

import wavewatch3 as ww3


@pytest.mark.parametrize("source", ["multigrid"])
@pytest.mark.parametrize("grid", ww3.SOURCES["multigrid"].GRIDS)
@pytest.mark.parametrize("quantity", ww3.SOURCES["multigrid"].QUANTITIES)
def test_url(source, grid, quantity):
    url = ww3.SOURCES[source]("2010-05-22", quantity, grid=grid)
    assert url.year == 2010
    assert url.month == 5
    assert url.quantity == quantity
    assert url.grid == grid
    assert url.filename == f"multi_1.{grid}.{quantity}.201005.grb2"


@pytest.mark.parametrize("source", ["multigrid"])
@pytest.mark.parametrize("quantity", ww3.SOURCES["multigrid"].QUANTITIES)
def test_url_default_grid(source, quantity):
    url = ww3.SOURCES[source]("2010-05-22", quantity)
    assert url.grid == "glo_30m"


@pytest.mark.parametrize("source", ww3.SOURCES)
def test_url_str(source):
    Source = ww3.SOURCES[source]
    url = Source(Source.MIN_DATE, "wind")
    assert str(url).startswith(Source.SCHEME)


@pytest.mark.parametrize("source", ww3.SOURCES)
def test_url_repr(source):
    import wavewatch3  # noqa

    Source = ww3.SOURCES[source]
    url = Source(Source.MIN_DATE, "tp")
    assert eval(repr(url)) == url


@pytest.mark.parametrize("source", ww3.SOURCES)
def test_url_quantity_setter(source):
    Source = ww3.SOURCES[source]
    url = Source(Source.MIN_DATE, "tp")
    url.quantity = "dp"
    assert url.quantity == "dp"
    assert url == Source(Source.MIN_DATE, "dp")

    with pytest.raises(ww3.ChoiceError):
        url.quantity = "foo"


@pytest.mark.parametrize("source", ww3.SOURCES)
def test_url_grid_setter(source):
    Source = ww3.SOURCES[source]

    url = Source(Source.MIN_DATE, "tp")
    for grid in Source.GRIDS:
        url.grid = grid
        assert url == Source(Source.MIN_DATE, "tp", grid=grid)

    with pytest.raises(ww3.ChoiceError):
        url.grid = "bar"
