```{image} https://github.com/csdms/bmi-wavewatch3/raw/main/docs/source/_static/bmi-wavewatch3-logo-light.svg
:alt: Python interface to WAVEWATCH III data
:target: https://github.com/csdms/bmi-wavewatch3
```

# WAVEWATCH III data in Python

```{image} https://github.com/csdms/bmi-wavewatch3/actions/workflows/test.yml/badge.svg
:alt: Test status
:target: https://github.com/csdms/bmi-wavewatch3/actions/workflows/test.yml
```

```{image} https://github.com/csdms/bmi-wavewatch3/workflows/Flake8/badge.svg
```

```{image} https://github.com/csdms/bmi-wavewatch3/workflows/Black/badge.svg
```

## About

% start-abstract

The *bmi_wavewatch3* Python package provides both a command line interface and
a programming interface for downloading and working with [WAVEWATCH III] data.

*bmi_wavewatch3* provides access to the following raster data sources,

- 30 year wave hindcast [Phase 1]
- 30 year wave hindcast [Phase 2]
- Production hindcast [Singlegrid]
- Production hindcast [Multigrid]

All data sources provide both global and regional grids.

[phase 1]: https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase1.php
[phase 2]: https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase2.php
[singlegrid]: https://polar.ncep.noaa.gov/waves/hindcasts/prod-nww3.php
[multigrid]: https://polar.ncep.noaa.gov/waves/hindcasts/prod-multi_1.php

% end-abstract

## Installation

To install the latest release of *bmi-wavewatch3* using *pip*, simply run the following
in your terminal of choice:

```bash
pip install bmi-wavewatch3
```

For a full description of how to install *bmi-wavewatch3*, including using *mamba*/*conda*,
please see the documentation for our [installation instructions].

## Source code

If you would like to modify or contribute code to *bmi-wavewatch3* or use the very
latest development version, please see the documentation that describes how to
[install bmi-wavewatch3 from source].

## Usage

% start-usage

To get started, you can download *WAVEWATCH III* data by date with the *ww3* command
(use `ww3 --help` to print a brief message),

```bash
ww3 fetch "2010-05-22"
```

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

## Example

### Plot data from the command line

Running the following from the command line will plot the variable
*significant wave height* from the WAVEWATCH III *at_4m* grid. Note that the time of
day (in this case, 15:00) is separated from the date with a `T` (i.e. times can be
given as `YYYY-MM-DDTHH`)

```bash
ww3 plot --grid=at_4m --data-var=swh "2010-09-15T15"
```

```{image} https://raw.githubusercontent.com/csdms/bmi-wavewatch3/main/docs/source/_static/hurricane_julia-light.png
:align: center
:alt: Hurricane Julia
:class: only-light
:width: 100%
```

```{image} https://raw.githubusercontent.com/csdms/bmi-wavewatch3/main/docs/source/_static/hurricane_julia-dark.png
:align: center
:alt: Hurricane Julia
:class: only-dark
:width: 100%
```

% end-usage

### Plot data from Python

% start-plotting

This example is similar to the previous but uses the *bmi_wavewatch3* Python interface.

```pycon
>>> from bmi_wavewatch3 import WaveWatch3
>>> ww3 = WaveWatch3("2009-11-08")
```

The data can be accessed as an *xarray* *Dataset* through the `data` attribute.

```pycon
>>> ww3.data
<xarray.Dataset>
Dimensions:     (step: 241, latitude: 311, longitude: 720)
Coordinates:
    time        datetime64[ns] 2009-11-01
  * step        (step) timedelta64[ns] 0 days 00:00:00 ... 30 days 00:00:00
    surface     float64 1.0
  * latitude    (latitude) float64 77.5 77.0 76.5 76.0 ... -76.5 -77.0 -77.5
  * longitude   (longitude) float64 0.0 0.5 1.0 1.5 ... 358.0 358.5 359.0 359.5
    valid_time  (step) datetime64[ns] dask.array<chunksize=(241,), meta=np.ndarray>
Data variables:
    dirpw       (step, latitude, longitude) float32 dask.array<chunksize=(241, 311, 720), meta=np.ndarray>
    perpw       (step, latitude, longitude) float32 dask.array<chunksize=(241, 311, 720), meta=np.ndarray>
    swh         (step, latitude, longitude) float32 dask.array<chunksize=(241, 311, 720), meta=np.ndarray>
    u           (step, latitude, longitude) float32 dask.array<chunksize=(241, 311, 720), meta=np.ndarray>
    v           (step, latitude, longitude) float32 dask.array<chunksize=(241, 311, 720), meta=np.ndarray>
Attributes:
    GRIB_edition:            2
    GRIB_centre:             kwbc
    GRIB_centreDescription:  US National Weather Service - NCEP
    GRIB_subCentre:          0
    Conventions:             CF-1.7
    institution:             US National Weather Service - NCEP
    history:                 2022-06-08T16:08 GRIB to CDM+CF via cfgrib-0.9.1...
```

The `step` attribute points to the current time slice into the data (i.e number of
three hour increments since the start of the month),

```pycon
>>> ww3.step
56
>>> ww3.data.swh[ww3.step, :, :].plot()
```

```{image} https://raw.githubusercontent.com/csdms/bmi-wavewatch3/main/docs/source/_static/ww3_global_swh-light.png
:align: center
:alt: Significant wave height
:class: only-light
:target: https://bmi-wavewatch3.readthedocs.org/
:width: 100%
```

```{image} https://raw.githubusercontent.com/csdms/bmi-wavewatch3/main/docs/source/_static/ww3_global_swh-dark.png
:align: center
:alt: Significant wave height
:class: only-dark
:target: https://bmi-wavewatch3.readthedocs.org/
:width: 100%
```

% end-plotting

[install bmi-wavewatch3 from source]: https://bmi-wavewatch3.readthedocs.io/en/master/install/developer_install.html
[installation instructions]: https://bmi-wavewatch3.readthedocs.io/en/master/installation.html
[multigrid data]: https://polar.ncep.noaa.gov/waves/hindcasts/multi_1/
[singlegrid data]: https://polar.ncep.noaa.gov/waves/hindcasts/nww3/
[wavewatch iii]: https://polar.ncep.noaa.gov/waves
[wavewatch iii description]: https://polar.ncep.noaa.gov/waves/wavewatch/
[wavewatch iii hindcasts]: http://polar.ncep.noaa.gov/waves/hindcasts/
[wavewatch iii thredds]: https://www.ncei.noaa.gov/thredds-ocean/catalog/ncep/nww3/catalog.html
