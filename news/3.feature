Added ``WaveWatch3`` class, which is the main access point for users of this package.
This class downloads WaveWatch III data files (if not already cached) and provides a
view of the data as an xarray Dataset. Users can then advance through the data
month-by-month, downloading additional data as necessary.

