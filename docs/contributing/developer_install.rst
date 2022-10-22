.. _developer_install:

=================
Developer Install
=================

.. important::

  The following commands will install *bmi-wavewatch3* into your current environment. Although
  not necessary, we **highly recommend** you install *bmi-wavewatch3* into its own
  :ref:`virtual environment <virtual_environments>`.

If you will be modifying code or contributing new code to *bmi-wavewatch3*, you will first
need to get *bmi-wavewatch3*'s source code and then install *bmi-wavewatch3* from that code.

--------------
Source Install
--------------

*bmi-wavewatch3* is actively being developed on GitHub, where the code is freely available.
If you would like to modify or contribute code, you can either clone our
repository

.. code-block:: bash

  git clone git://github.com/csdms/bmi-wavewatch3.git

or download the `tarball <https://github.com/csdms/bmi-wavewatch3/tarball/master>`_
(a zip file is available for Windows users):

.. code-block:: bash

  curl -OL https://github.com/csdms/bmi-wavewatch3/tarball/master

Once you have a copy of the source code, you can install it into your current
Python environment,


.. tab:: pip

  .. code-block:: bash

    cd bmi-wavewatch3
    pip install -e .

.. tab:: mamba

  .. code-block:: bash

    cd bmi-wavewatch3
    mamba install --file=requirements.txt
    pip install -e .

.. tab:: conda

  .. code-block:: bash

    cd bmi-wavewatch3
    conda install --file=requirements.txt
    pip install -e .
