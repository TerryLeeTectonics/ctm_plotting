#!/usr/bin/env python
#
#  query_0d_point.py
#


### Import Packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xarray as xr
import argparse

# Import initiation functions
from Initiation import init_ctm
from Value_check import check_inbounds_values

## query the model at a single point
#  - inputs: latitude, longitude, depth to query model, modelname
#  - returns: DataFrame with temperature at this point
def query_0D_point(lat, lon, dep, modelname, modelpath):

    # initialize dataset
    xdata = init_ctm(modelname, modelpath)

    # check validity of query
    check_inbounds_values(xdata, {"longitude[°]": [lon], "latitude[°]": [lat], "depth[m]": [dep]})

    # interpolate a single point
    temp = float(xdata.interp({"longitude[°]": lon, "latitude[°]": lat, "depth[m]": dep})["temperature[°C]"])

    # return in DataFrame format
    return pd.DataFrame({"longitude[°]": [lon], "latitude[°]": [lat], "depth[m]": [dep], "temperature[°C]": [temp]})

def call_func():
    
    par = argparse.ArgumentParser()
    par.add_argument('--lat', type = float, required = True)          # Add argument of latitude (°)
    par.add_argument('--lon', type = float, required = True)          # Add argument of longitude (°)
    par.add_argument('--z', type = float, required = True)            # Add arugment of depth (m)
    par.add_argument('--modelname', type = str, required = True)      # Add argument of model name: Lee_2025 or Shinevar_2018
    par.add_argument('--modelpath', type = str, required = True)      # Add argument of input model path
    args = par.parse_args()                                           # Extract arguments
    
    # Call the function
    df = query_0D_point(
        args.lat,
        args.lon,
        args.z,
        args.modelname,
        args.modelpath)

    # Print query result
    print(df)

    # Return
    return df

# Make sure the following is not calling when it is being imported, only runs the following when directly run at command prompt
if __name__ == "__main__":
    # Call the query function
    df = call_func()


