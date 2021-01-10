import pandas as pd
import xarray as xr
import numpy as np

print("xarray ", xr.__version__)
print("pandas ", pd.__version__)

t = np.arange(0, 1, 0.1)
print(t)

s = pd.Series(data=list("abcdefghij"), index=t)
print(s)

# print(s.loc[0.6])

print(s.loc[0.8])

print(t[6])

print(s.loc[t[6]])

print(s.loc[0.6: 0.8])

print(s.loc[0.6: 0.6])

print(s.loc[0.4: 0.6])

print(s.loc[0.55: 0.85])

a = xr.DataArray(data=range(10), coords=[("t", t)])
print(a)

print()
print(a.sel(t=0.6, method='nearest'))

print()
a.loc[dict(t=slice(0.59, 0.81))] = 17
print(a)