### Import Packages
import xarray as xr

## initalize Xarray Dataset from netCDF file
#  - inputs: model name (Lee_2025 or Shinevar_2018) and model path
#  - returns: Xarray Dataset corresponding to the model
def init_ctm(modelname, modelpath):
    
    # open dataset
    xdata = xr.open_dataset(modelpath)

    if modelname == 'Lee_2025':
        # configure: change unit to meters and rename all variables
        xdata = xdata.assign_coords({"depth": xdata.depth * 1000.0})
        xdata = xdata.rename_dims({"longitude": "longitude[°]", 
                                   "latitude": "latitude[°]",
                                   "depth": "depth[m]"})
        
        xdata = xdata.rename_vars({"longitude": "longitude[°]", 
                                   "latitude": "latitude[°]",
                                   "depth": "depth[m]",
                                   "temperature_diffused": "temperature[°C]"})

        xdata['depth[m]'] = xdata['depth[m]'] * 1000

    elif modelname == 'Shinevar_2018':
        # configure: rename all variables
        xdata = xdata.rename_dims({"longitude": "longitude[°]", 
                                   "latitude": "latitude[°]",
                                   "depth": "depth[m]"})
        
        xdata = xdata.rename_vars({"longitude": "longitude[°]", 
                                   "latitude": "latitude[°]",
                                   "depth": "depth[m]",
                                   "temperature": "temperature[°C]"})

    elif modelname == 'Boyd_2019':
        # configure: rename all variables
        xdata = xdata.rename_dims({"dimk": "longitude[°]", 
                                   "dimj": "latitude[°]",
                                   "diml": "depth[m]"})
        
        xdata = xdata.rename_vars({"Longitude": "longitude[°]", 
                                   "Latitude": "latitude[°]",
                                   "Depth": "depth[m]",
                                   "Temperature": "temperature[°C]"})
        
        xdata = xdata.set_coords(['longitude[°]', 'latitude[°]', 'depth[m]'])

    elif modelname == 'Suietal_2025':
        # configure: rename all variables
        xdata = xdata.rename_dims({'dimk': 'longitude[°]', 
                                   'dimj': 'latitude[°]',
                                   'diml': 'depth[m]'})
        
        xdata = xdata.rename_vars({'Longitude': 'longitude[°]', 
                                   'Latitude': 'latitude[°]',
                                   'Depth': 'depth[m]',
                                   'Temperature': 'temperature[°C]'})
        
        xdata = xdata.set_coords(['longitude[°]', 'latitude[°]', 'depth[m]'])
        xdata = xdata.assign_coords({'depth[m]': xdata['depth[m]'] * 1000.0})
        
        
    # return
    return xdata
