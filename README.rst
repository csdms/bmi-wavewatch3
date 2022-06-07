wavewatch3: Python interface to WAVEWATCH III
=============================================

.. image:: https://github.com/csdms/bmi-wavewatch3/workflows/Build/Test%20CI/badge.svg

.. image:: https://github.com/csdms/bmi-wavewatch3/workflows/Flake8/badge.svg

.. image:: https://github.com/csdms/bmi-wavewatch3/workflows/Black/badge.svg


About
-----

The *wavewatch3* Python package provides both a command line interface and a programming interface
for downloading and working with `WAVEWATCH III`_ data.

*wavewatch3* provides access to the following raster data sources,
* 30 year wave hindcast `Phase 1`_
* 30 year wave hindcast `Phase 2`_
* Production hindcast Singlegrid_
* Production hindcast Multigrid_

All data sources provide both global and regional grids.

Installation
------------

*wavewatch3* can be installed by running `pip install wavewatch3`. It requires Python >= 3.8 to run.

If you simply can't wait for the latest release, you can install *wavewatch3*
directly from GitHub,

.. code-block:: bash

   $ pip install git+https://github.com/csdms/bmi-wavewatch3

*wavewatch3* is also available through *conda*, `conda install wavewatch3 -c conda-forge`.


Usage
-----

To get started, you can download *WAVEWATCH III* data by date with the *ww3* command
(use `ww3 --help` to print a brief message),

..code-block:: bash

    $ ww3 fetch 2010-05-22

You can also do this through Python,

..code-block:: python

    >>> from wavewatch3 import WaveWatch3
    >>> WaveWatch3.fetch("2010-05-22")

The *wavewatch3* package provides the ``WaveWatch3`` class for downloading data and
presenting it as an *xarray* *Dataset*.

.. code-block:: python

   >>> from wavewatch3 import WaveWatch3
   >>> ww3 = WaveWatch3("2010-05-22")
   >>> ww3.data
   <xarray.Dataset>
   ...

Use the ``inc`` method to advance in time month-by-month,

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



