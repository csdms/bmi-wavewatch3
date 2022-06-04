wavewatch3: Python interface to WAVEWATCH III
=============================================

.. image:: https://github.com/csdms/bmi-wavewatch3/workflows/Build/Test%20CI/badge.svg

.. image:: https://github.com/csdms/bmi-wavewatch3/workflows/Flake8/badge.svg

.. image:: https://github.com/csdms/bmi-wavewatch3/workflows/Black/badge.svg


About
-----

The *wavewatch3* Python package provides both a command line interface and a programming interface
for downloading and working with `WAVEWATCH III`_ data.

*wavewatch3* provides access to the following raster data sets,
* 30 year wave hindcast `Phase 1`_
* 30 year wave hindcast `Phase 2`_
* Production hindcast NWW3_
* Production hindcast Multigrid_


Installation
------------

*wavewatch* can be installed by running `pip install wavewatch3`. It requires Python >= 3.8 to run.

If you simply can't wait for the latest release, you can install *wavewatch3*
directly from GitHub,

.. code-block:: bash

   $ pip install git+https://github.com/csdms/bmi-wavewatch3

*wavewatch3* is also available through *conda*, `conda install wavewatch3 -c conda-forge`.


Usage
-----

To get started, you can download *WAVEWATCH III* data by date with the *ww3* command,

..code-block:: bash

    $ ww3 fetch 2010-05-22

You can also do this through Python,

..code-block:: python

    >>> from wavewatch3 import WaveWatch3
    >>> WaveWatch3.fetch("2010-05-22")

Use `ww3 --help` to print a brief message.

Input Files
-----------

.. _WAVEWATCH III: https://polar.ncep.noaa.gov/waves
.. _Phase 1: https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase1.php
.. _Phase 2: https://polar.ncep.noaa.gov/waves/hindcasts/nopp-phase2.php
.. _Multigrid: https://polar.ncep.noaa.gov/waves/hindcasts/prod-multi_1.php
.. _NWW3: https://polar.ncep.noaa.gov/waves/hindcasts/prod-nww3.php

https://polar.ncep.noaa.gov/waves/wavewatch/
http://polar.ncep.noaa.gov/waves/hindcasts/

https://www.ncei.noaa.gov/thredds-ocean/catalog/ncep/nww3/catalog.html


https://polar.ncep.noaa.gov/waves/hindcasts/nww3/
https://polar.ncep.noaa.gov/waves/hindcasts/multi_1/



