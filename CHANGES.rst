Release Notes
=============

.. towncrier release notes start

0.2.0 (2022-06-17)
------------------

New Features
````````````

- Added a new subcommand, *plot*, to the *ww3* command-line program.
  ``ww3 plot`` with download (if the data files are not already cached) and
  create a plot of the requested data. (`#13 <https://github.com/csdms/bmi-wavewatch3/issues/13>`_)


Bug Fixes
`````````

- Fixed a bug in the reporting of an error caused by an invalide datatime
  string. (`#13 <https://github.com/csdms/bmi-wavewatch3/issues/13>`_)


0.1.1 (2022-06-10)
------------------

Other Changes and Additions
```````````````````````````

- Set up GitHub Action to create a source distribution and push it to
  *TestPyPI*. This action is only run if the version tag is a prerelease version
  (i.e. the version string ends with ``[ab][0-9]+``). (`#10 <https://github.com/csdms/bmi-wavewatch3/issues/10>`_)
- Set up GitHub Action to create a source distribution and push it to
  *PyPI*. This action is only run if the version tag is a release version
  (i.e. the version string doesn't end with ``[ab][0-9]+``). (`#11 <https://github.com/csdms/bmi-wavewatch3/issues/11>`_)


0.1.1b1 (2022-06-09)
--------------------

New Features
````````````

- Added ``ww3`` command line interface to download WaveWatch III data by date,
  region and quantity (significant wave height, wind speed, etc.). (`#1 <https://github.com/csdms/bmi-wavewatch3/issues/1>`_)
- Added ``WaveWatch3`` class, which is the main access point for users of this package.
  This class downloads WaveWatch III data files (if not already cached) and provides a
  view of the data as an xarray Dataset. Users can then advance through the data
  month-by-month, downloading additional data as necessary. (`#3 <https://github.com/csdms/bmi-wavewatch3/issues/3>`_)
- Added the ``ww3 clean`` subcommand that removes cached data files. (`#4 <https://github.com/csdms/bmi-wavewatch3/issues/4>`_)
- Added ``BMIWaveWatch3`` class to provide a Basic Model Interface for the
  *wavewatch3* package. (`#5 <https://github.com/csdms/bmi-wavewatch3/issues/5>`_)
- Added additional WaveWatch III data sources from which users can fraw data
  from. (`#6 <https://github.com/csdms/bmi-wavewatch3/issues/6>`_)
- Added ``fetch`` method to WaveWatch3 to mimic the command line program
  ``ww3 fetch``. (`#7 <https://github.com/csdms/bmi-wavewatch3/issues/7>`_)
- Added additional data sources from which to retreive data from. Available
  data sources now include: Phase 1, Phase 2, Multigrid, Multigrid-extended,
  and Multigrid-thredds. (`#7 <https://github.com/csdms/bmi-wavewatch3/issues/7>`_)
- Added ``ww3 info`` command to print information (e.g. available grids, quantities,
  etc.) about data sources. (`#7 <https://github.com/csdms/bmi-wavewatch3/issues/7>`_)
- Added a ``step`` property to ``WaveWatch3`` to track the current time slice
  of the data cube. This property is also settable so that a user can use it to
  advance throught the data (additional data are downloaded in the background as
  needed). (`#8 <https://github.com/csdms/bmi-wavewatch3/issues/8>`_)
- Dates can now be specified as iso-formatted date/time strings. For example,
  "1944-06-06T06:30". (`#8 <https://github.com/csdms/bmi-wavewatch3/issues/8>`_)
- Rename package to ``bmi_wavewatch3``. This follows the convention used by other
  CSDMS data components. (`#9 <https://github.com/csdms/bmi-wavewatch3/issues/9>`_)


Documentation Enhancements
``````````````````````````

- Added package description, installation, usage, and an example to the
  documentation. (`#8 <https://github.com/csdms/bmi-wavewatch3/issues/8>`_)


Other Changes and Additions
```````````````````````````

- Set up continuous integration using GitHub actions. This includes tests to
  ensure that the code is styled according to *black*, is free of lint, and
  passes all unit tests. (`#2 <https://github.com/csdms/bmi-wavewatch3/issues/2>`_)
- Added more unit tests, particularly for data sources. (`#7 <https://github.com/csdms/bmi-wavewatch3/issues/7>`_)
- Added a GitHub action to build the sphinx-based documentation as part of the
  continuous integration. (`#8 <https://github.com/csdms/bmi-wavewatch3/issues/8>`_)
- Better error reporting for the command line interface for HTTP errors when
  retreiving data as well as input validation. (`#8 <https://github.com/csdms/bmi-wavewatch3/issues/8>`_)
- Set up GitHub Action to create a source distribution and push it to
  *TestPyPI*. This action is only run if the version tag is a prerelease version
  (i.e. the version string ends with ``[ab][0-9]+``). (`#10 <https://github.com/csdms/bmi-wavewatch3/issues/10>`_)
