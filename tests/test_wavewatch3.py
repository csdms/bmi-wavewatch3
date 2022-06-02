from wavewatch3 import WaveWatch3


def test_wavewatch3():
    ww3 = WaveWatch3("2010-05-22")
    assert ww3.date == "2010-05-22"
    assert ww3.year == 2010
    assert ww3.month == 5
    assert ww3.region == "glo_30m"


def test_wavewatch3_inc():
    ww3 = WaveWatch3("2010-03-14")
    assert ww3.date == "2010-03-14"

    ww3.inc()
    assert ww3.date == "2010-04-14"
    assert (ww3.month, ww3.year) == (4, 2010)

    ww3.inc(12)
    assert ww3.date == "2011-04-14"
    assert (ww3.month, ww3.year) == (4, 2011)

    ww3.inc(-2)
    assert ww3.date == "2011-02-14"
    assert (ww3.month, ww3.year) == (2, 2011)


def test_wavewatch3_date():
    ww3 = WaveWatch3("2001-01-01")
    assert ww3.date == "2001-01-01"

    ww3.date = "1973-03-14"
    assert ww3.date == "1973-03-14"
    assert (ww3.month, ww3.year) == (3, 1973)


def test_repr():
    ww3 = WaveWatch3("2008-12-31")
    assert eval(repr(ww3)) == ww3


def test_equivalent():
    assert WaveWatch3("2008-12-31") == WaveWatch3("2008-12-31", region="glo_30m")
    assert WaveWatch3("2008-12-31", region="ak_4m") != WaveWatch3(
        "2008-12-31", region="glo_30m"
    )
    assert WaveWatch3("2009-12-31") != WaveWatch3("2008-12-31")
    assert WaveWatch3("2009-12-31") == WaveWatch3("2009-12-01")
