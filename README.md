[![Python interface to WAVEWATCH III data][logo]][github-link]


# WAVEWATCH III data in Python

[![Documentation status][rtd-badge]][rtd-link]
[![Code-style: Black][black-badge]][black-link]
[![Testing status][testing-badge]][testing-link]
![Flake8][flake8-badge]


## About


<!-- start-abstract -->

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

<!-- end-abstract -->

[**See the bmi-wavewatch3 documentation for more information**](https://bmi-wavewatch3.readthedocs.io/en/latest/).

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


[install bmi-wavewatch3 from source]: https://bmi-wavewatch3.readthedocs.io/en/master/install/developer_install.html
[installation instructions]: https://bmi-wavewatch3.readthedocs.io/en/master/installation.html
[multigrid data]: https://polar.ncep.noaa.gov/waves/hindcasts/multi_1/
[singlegrid data]: https://polar.ncep.noaa.gov/waves/hindcasts/nww3/
[wavewatch iii]: https://polar.ncep.noaa.gov/waves
[wavewatch iii description]: https://polar.ncep.noaa.gov/waves/wavewatch/
[wavewatch iii hindcasts]: http://polar.ncep.noaa.gov/waves/hindcasts/
[wavewatch iii thredds]: https://www.ncei.noaa.gov/thredds-ocean/catalog/ncep/nww3/catalog.html


[black-badge]: https://github.com/csdms/bmi-wavewatch3/workflows/Black/badge.svg
[black-link]: https://github.com/ambv/black
[flake8-badge]: https://github.com/csdms/bmi-wavewatch3/workflows/Flake8/badge.svg
[github-link]: https://github.com/csdms/bmi-wavewatch3
[logo]: https://github.com/csdms/bmi-wavewatch3/raw/main/docs/source/_static/bmi-wavewatch3-logo-light.svg
[rtd-badge]: https://readthedocs.org/projects/bmi-wavewatch3/badge/?version=latest
[rtd-link]: https://bmi-wavewatch3.readthedocs.io/en/latest/?badge=latest
[testing-badge]: https://github.com/csdms/bmi-wavewatch3/actions/workflows/test.yml/badge.svg
[testing-link]: https://github.com/csdms/bmi-wavewatch3/actions/workflows/test.yml
[ww3-global-image]: https://raw.githubusercontent.com/csdms/bmi-wavewatch3/main/docs/source/_static/ww3_global_swh-light.png
