#!/usr/bin/env python
#
#  query_2d_cross_section.py
#

### Import Packages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import xarray as xr
import argparse
from pyproj import Geod

# Import initiation functions
from Initiation import init_ctm
from Value_check import check_inbounds_values
from test_plot import test_plot
from calculate_geodesic_track import calculate_geodesic_track
from write_csv_output import write_csv_output

## query the model along a vertical cross-section between lon/lat pairs
#  - inputs: start longitude and latitude, end longitude and latitude, start and end depth, and model name; optional plotting
#  - returns: DataFrame with temperature at these points; optional figure
def query_2D_vertical_cross_section(lat_start, lon_start, lat_end, lon_end, z_start, z_end, modelname, modelpath, plot = False):
    
    # initialize dataset
    xdata = init_ctm(modelname, modelpath)

    # check validity of query
    check_inbounds_values(xdata, {"longitude[°]": [lon_start, lon_end], 
                                  "latitude[°]": [lat_start, lat_end], 
                                  "depth[m]": [z_start, z_end]})

    # calculate lon/lat points along a track
    ntrack = 121
    glons, glats = calculate_geodesic_track(lon_start, lat_start, lon_end, lat_end, ntrack)
    
    # define depth range
    ndep = 61
    zvals = np.linspace(z_start, z_end, ndep)

    # interpolate along track and vertically
    xi = xdata.interp({"longitude[°]": xr.DataArray(glons, dims="track index"), 
                  "latitude[°]": xr.DataArray(glats, dims="track index"),
                  "depth[m]": zvals})

    
    # define dataframe to return
    df = xi.to_dataframe().reset_index()
    df = df[["longitude[°]", "latitude[°]", "depth[m]", "temperature[°C]"]]

    # return
    if plot: # optional plot
        fig = test_plot(xi, "2D_vertical")
        return df, fig
    else:
        return df

# Make a function to allow batch mode
def call_func():
    
    par = argparse.ArgumentParser()
    par.add_argument('--lat_start', type = float, required = True)    # Add argument of starting latitude (°)
    par.add_argument('--lon_start', type = float, required = True)    # Add argument of starting longitude (°)
    par.add_argument('--lat_end', type = float, required = True)      # Add argument of ending latitude (°)
    par.add_argument('--lon_end', type = float, required = True)      # Add argument of ending longitude (°)
    par.add_argument('--z_start', type = float, required = True)      # Add arugment of starting depth (m)
    par.add_argument('--z_end', type = float, required = True)        # Add arugment of ending depth (m)
    par.add_argument('--modelname', type = str, required = True)      # Add argument of model name: Lee_2025 or Shinevar_2018
    par.add_argument('--modelpath', type = str, required = True)      # Add argument of input model path
    par.add_argument('--outpath', type = str, required = True)        # Add argument of output file path and file name
    
    args = par.parse_args()                                           # Extract arguments
    
    # Call the function
    df = query_2D_vertical_cross_section(
         args.lat_start,
         args.lon_start,
         args.lat_end,
         args.lon_end,
         args.z_start,
         args.z_end,
         args.modelname,
         args.modelpath)

    # Call the function to write the output csv file
    write_csv_output(df, args.outpath, '2D_vertical', args.modelname)

# Make sure the following is not calling when it is being imported, only runs the following when directly run at command prompt
if __name__ == "__main__":
    # Call the query function
    call_func()

