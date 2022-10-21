.. _workflow:

========
Workflow
========

This page describes the tooling used during development of this project. It also serves
as a reference for the various commands that you would use when working on this project.

--------
Overview
--------

This project uses the `GitHub Flow`_ for collaboration. The codebase contains primarily Python code.

- `nox`_ is used for automating development tasks.
- `sphinx-autobuild`_ is used to provide live-reloading pages when working on the docs.
- `pre-commit`_ is used for running the linters.

-------------
Initial Setup
-------------

To work on this project, you need to have Python 3.8+.

* Clone this project using git:

  .. code:: bash

    git clone https://github.com/csdms/bmi-wavewatch3.git
    cd bmi-wavewatch3

* Install the project's development workflow runner:

  .. code:: bash

    pip install nox

You're all set for working on this project.

--------
Commands
--------

Code Linting
============

.. code:: bash

    nox -s lint


Run the linters, as configured with `pre-commit`_.

Local Development Server
========================

.. code:: bash

    nox -s docs-live


Serve this project's documentation locally, using `sphinx-autobuild`_. This will open
the generated documentation page in your browser.

The server also watches for changes made to the documentation (`docs/source`), which
will trigger a rebuild. Once the build is completed, the server will
reload any open pages using *livereload*.

Documentation Generation
========================

.. code:: bash

    nox -s docs

Generate the documentation for *bmi-wavewatch3* into the `docs/build` folder. This (mostly)
does the same thing as ``nox -s docs-live``, except it invokes ``sphinx-build`` instead
of `sphinx-autobuild`_.


.. _GitHub Flow: https://guides.github.com/introduction/flow/
.. _nox: https://nox.readthedocs.io/en/stable/
.. _sphinx-autobuild: https://github.com/executablebooks/sphinx-autobuild
.. _pre-commit: https://pre-commit.com/
