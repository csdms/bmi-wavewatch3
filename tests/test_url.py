import pytest

from bmi_wavewatch3 import ChoiceError, WaveWatch3URL


@pytest.mark.parametrize("region", WaveWatch3URL.REGIONS)
@pytest.mark.parametrize("quantity", WaveWatch3URL.QUANTITIES)
def test_url(region, quantity):
    url = WaveWatch3URL("2010-05-22", quantity, region=region)
    assert url.year == 2010
    assert url.month == 5
    assert url.quantity == quantity
    assert url.region == region
    assert url.filename == f"multi_1.{region}.{quantity}.201005.grb2"


@pytest.mark.parametrize("quantity", WaveWatch3URL.QUANTITIES)
def test_url_default_region(quantity):
    url = WaveWatch3URL("2010-05-22", quantity)
    assert url.region == "glo_30m"


def test_url_str():
    url = WaveWatch3URL("2010-05-22", "wind")
    assert str(url).startswith(WaveWatch3URL.SCHEME)


def test_url_repr():
    url = WaveWatch3URL("2010-05-22", "tp")
    assert eval(repr(url)) == url


def test_url_quantity_setter():
    url = WaveWatch3URL("2010-05-22", "tp")
    url.quantity = "dp"
    assert url.quantity == "dp"
    assert url == WaveWatch3URL("2010-05-22", "dp")

    with pytest.raises(ChoiceError):
        url.quantity = "foo"


def test_url_region_setter():
    url = WaveWatch3URL("2010-05-22", "tp")
    url.region = "ak_4m"
    assert url == WaveWatch3URL("2010-05-22", "tp", region="ak_4m")

    with pytest.raises(ChoiceError):
        url.region = "bar"
