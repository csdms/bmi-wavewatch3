.. image:: https://github.com/csdms/bmi-wavewatch3/raw/main/docs/source/_static/wavewatch3_logo.png
   :target: https://github.com/csdms/bmi-wavewatch3
   :alt: Python interface to WAVEWATCH III data

WAVEWATCH III data in Python
============================

.. image:: https://github.com/csdms/bmi-wavewatch3/actions/workflows/test.yml/badge.svg
   :target: https://github.com/csdms/bmi-wavewatch3/actions/workflows/test.yml
   :alt: Test status

.. image:: https://github.com/csdms/bmi-wavewatch3/workflows/Flake8/badge.svg

.. image:: https://github.com/csdms/bmi-wavewatch3/workflows/Black/badge.svg


About
-----

The *bmi_wavewatch3* Python package provides both a command line interface and a programming interface
for downloading and working with `WAVEWATCH III`_ data.

*bmi_wavewatch3* provides access to the following raster data sources,

* 30 year wave hindcast `Phase 1`_
* 30 year wave hindcast `Phase 2`_
* Production hindcast Singlegrid_
* Production hindcast Multigrid_

All data sources provide both global and regional grids.

Installation
------------

*bmi_wavewatch3* can be installed by running ``pip install bmi-wavewatch3``. It requires Python >= 3.8 to run.

If you simply can't wait for the latest release, you can install *bmi_wavewatch3*
directly from GitHub,

.. code-block:: bash

   $ pip install git+https://github.com/csdms/bmi-wavewatch3

*bmi_wavewatch3* is also available through *conda*, ``conda install bmi-wavewatch3 -c conda-forge``.


Usage
-----

To get started, you can download *WAVEWATCH III* data by date with the *ww3* command
(use `ww3 --help` to print a brief message),

.. code-block:: bash

    $ ww3 fetch "2010-05-22"

You can also do this through Python,

.. code-block:: python

    >>> from bmi_wavewatch3 import WaveWatch3
    >>> WaveWatch3.fetch("2010-05-22")

The *bmi_wavewatch3* package provides the ``WaveWatch3`` class for downloading data and
presenting it as an *xarray* *Dataset*.

.. code-block:: python

   >>> from bmi_wavewatch3 import WaveWatch3
   >>> ww3 = WaveWatch3("2010-05-22")
   >>> ww3.data
   <xarray.Dataset>
   ...

Use the ``inc`` method to advance in time month-by-month,

.. code-block:: python

   >>> ww3.date
   '2010-05-22'
   >>> ww3.inc()
   '2010-06-22'
   >>> ww3.data.time
   <xarray.DataArray 'time' ()>
   array('2010-06-01T00:00:00.000000000', dtype='datetime64[ns]')
   ...

This will download new datasets as necessary and load the new data into the ``data`` attribute.

.. note::

   If the new data are not cached on you computer, you will notice a delay while the new
   data are download. If the ``lazy`` flag is set, the download will only occur once you
   try to access the data (i.e. ``ww3.data``), otherwise the data are downloaded
   as soon as the date is set.

Example
-------


.. code:: python

   >>> from bmi_wavewatch3 import WaveWatch3
   >>> ww3 = WaveWatch3("2009-11-08")

The data can be accessed as an *xarray* *Dataset* through the ``data`` attribute.

.. code:: python

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

The ``step`` attribute points to the current time slice into the data (i.e number of three hour increments
since the start of the month),

.. code:: python

   >>> ww3.step
   56
   >>> ww3.data.swh[ww3.step, :, :].plot()

.. image:: https://raw.githubusercontent.com/csdms/bmi-wavewatch3/main/docs/source/_static/ww3_global_swh.png
  :width: 100%
  :alt: Significant wave height

.. _WAVEWATCH III: https://polar.ncep.noaa.gov/waves
.. _Phase 1: https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase1.php
.. _Phase 2: https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase2.php
.. _Multigrid: https://polar.ncep.noaa.gov/waves/hindcasts/prod-multi_1.php
.. _Singlegrid: https://polar.ncep.noaa.gov/waves/hindcasts/prod-nww3.php
.. _WAVEWATCH III description: https://polar.ncep.noaa.gov/waves/wavewatch/
.. _WAVEWATCH III hindcasts: http://polar.ncep.noaa.gov/waves/hindcasts/
.. _WAVEWATCH III thredds: https://www.ncei.noaa.gov/thredds-ocean/catalog/ncep/nww3/catalog.html
.. _Singlegrid data: https://polar.ncep.noaa.gov/waves/hindcasts/nww3/
.. _Multigrid data: https://polar.ncep.noaa.gov/waves/hindcasts/multi_1/



