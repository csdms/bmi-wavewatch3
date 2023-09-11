(install)=

# Developer Install

:::{important}
The following commands will install *bmi-wavewatch3* into your current environment.
Although not necessary, we **highly recommend** you install bmi-wavewatch3 into its
own {ref}`virtual environment <virtual-environments>`.
:::

If you will be modifying code or contributing new code to *bmi-wavewatch3*, you will
first need to get *bmi-wavewatch3*'s source code and then install *bmi-wavewatch3*
from that code.

## Source Install

% start-install-source

*bmi-wavewatch3* is actively being developed on GitHub, where the code is freely
available. If you would like to modify or contribute code, you can either clone our
repository

```bash
git clone git://github.com/csdms/bmi-wavewatch3.git
```

or download the [zip file](https://github.com/csdms/bmi-wavewatch3/archive/refs/heads/main.zip):

```bash
curl -OL https://github.com/csdms/bmi-wavewatch3/archive/refs/heads/main.zip
```

Once you have a copy of the source code, you can install it into your current
Python environment,


````{tab} mamba
```bash
cd bmi-wavewatch3
mamba install --file=requirements-conda.in
pip install -e .
```
````

````{tab} conda
```bash
cd bmi-wavewatch3
conda install --file=requirements-conda.in
pip install -e .
```
````

````{tab} pip
```bash
cd bmi-wavewatch3
pip install -e .
```
````

% end-install-source
