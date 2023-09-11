# Usage

## Command Line

To get started, you can download *WAVEWATCH III* data by date with the *ww3* command
(use `ww3 --help` to print a brief message),

```bash
ww3 fetch "2010-05-22"
```

## Python

You can also do this through Python,

```pycon
>>> from bmi_wavewatch3 import WaveWatch3
>>> WaveWatch3.fetch("2010-05-22")
```

The *bmi_wavewatch3* package provides the `WaveWatch3` class for downloading data and
presenting it as an *xarray* *Dataset*.

```pycon
>>> from bmi_wavewatch3 import WaveWatch3
>>> ww3 = WaveWatch3("2010-05-22")
>>> ww3.data
<xarray.Dataset>
...
```

Use the `inc` method to advance in time month-by-month,

```pycon
>>> ww3.date
'2010-05-22'
>>> ww3.inc()
'2010-06-22'
>>> ww3.data.time
<xarray.DataArray 'time' ()>
array('2010-06-01T00:00:00.000000000', dtype='datetime64[ns]')
...
```

This will download new datasets as necessary and load the new data into the `data`
attribute.

:::{note}
If the new data are not cached on you computer, you will notice a delay while the new
data are download. If the `lazy` flag is set, the download will only occur once you
try to access the data (i.e. `ww3.data`), otherwise the data are downloaded
as soon as the date is set.
:::
