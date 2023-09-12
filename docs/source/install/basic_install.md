(basic-install)=

# Installation

:::{important}
The following commands will install *bmi-wavewatch3* into your current environment.
Although not necessary, we **highly recommend** you install bmi-wavewatch3 into its
own {ref}`virtual environment <virtual-environments>`.
:::

In order to use *bmi-wavewatch3* you will first need Python. While not
necessary, we recommend using the
[Anaconda Python distribution](https://www.anaconda.com/distribution/)
as it provides a large number of third-party packages useful for
scientific computing.

To install *bmi-wavewatch3*, simply run the following in your terminal of choice:

````{tab} mamba
```bash
conda install mamba -c conda-forge
mamba install bmi-wavewatch3 -c nodefaults -c conda-forge
```
````

````{tab} conda
```bash
conda install bmi-wavewatch3 -c nodefaults -c conda-forge
```
````

````{tab} pip
```bash
pip install bmi-wavewatch3
```
````

:::{important}
Due to an issue with the *eccodes* package, **Windows users and users of newer
versions of Python** may see an error when trying to run *bmi-wavewatch3* that has
been installed from PyPI (i.e. using the *pip* method above). If you encounter this
problem, try installing using *conda*/*mamba*.
:::

If you would like the very latest development version of *bmi-wavewatch3* or want to
modify or contribute code to the *bmi-wavewatch3* project, you will need to do a
{ref}`developer installation <install>` of *bmi-wavewatch3* from source.
