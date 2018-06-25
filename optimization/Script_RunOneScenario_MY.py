# -*- coding: utf-8 -*-
"""
Created on Thu May 17 12:59:12 2018

@author: Fan
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May 13 22:52:51 2018

@author: Fan
"""

# -*- coding: utf-8 -*-
"""
This is running/entrance script.

Last updated on February 19, 2019.
Comments checked and updated on May 2, 2018.

@author: Fan
"""

import numpy as np
from shutil import copy2
from Loop_Model import loop_model
import os

#%% File system settings

# Allowed value: 'npz', 'pkl'
# These two data files are equivalent but "pkl" is relatively more generic.

DATA_TYPE = 'pkl'

# Allowed value: 0, 1
PRINT_FIGURE = 1

# For Fan Tong's working directory
# Windows desktop: "D:/M/WORK/"
# Macbook: "/Users/FanMacbook/Downloads/Energy/WORK/"

directory_project = os.path.dirname(os.path.realpath(__file__))
directory_project = directory_project + '/'

directory_input = directory_project + "Input_Data/"
directory_output = directory_project + "Results/"

# %% Modeling preparations

# The time resolution is hourly.
# One year = 8760 hours. Maximum 30 years data is available.

HOUR_IN_1_YEAR = 8760
Day_In_1_YEAR = 365
HOUR_IN_1_DAY = 24
HOUR_IN_1_WEEK = 24*7

# -----------------------------------------------------------------------------

# %%

demand = np.load(directory_input + 'conus_real_demand.npy') * 1e3 # time series of demand in kW

wind_capacity_factor_reanalysis = \
    np.load(directory_input + 'United States of America_CFwind_area-weighted-mean.npy')
solar_capacity_factor_reanalysis = \
    np.load(directory_input + 'United States of America_CFsolar_area-weighted-mean.npy')

wind_capacity_factor = 0.345 / np.mean(wind_capacity_factor_reanalysis) * wind_capacity_factor_reanalysis # time series of wind capacity factor data
solar_capacity_factor = 0.222 / np.mean(solar_capacity_factor_reanalysis) * solar_capacity_factor_reanalysis  # time series of solar capacity factor data

# %% Technology assumptions

# FIXED assumptions

EPSILON = 1E-10

capital_charge_rate_power = 0.08
capital_charge_rate_storage = 0.08

#variable_OM_cost_power = np.array([2, 0, 0, 2.3])/1e3   # $/kWh
#fixed_OM_cost_power = np.array([10, 45, 20, 100])/1e3   # $/kW/yr

fixed_OM_cost_power = np.array([10.93, 46.71, 21.66, 99.65])       # $/kW/yr
variable_OM_cost_power = np.array([2e-3, EPSILON, EPSILON, 2.3e-3])     # $/kWh

fixed_OM_cost_storage = 0                               # $/kWh/yr
variable_OM_cost_storage = EPSILON                      # $/kWh (one-way cost)

nuclear_fuel_cost = 0.004                               # $/kWh
storage_fuel_cost = 0

efficiency_power = np.array([0.54, 1, 1, 0.33])         # Fraction

curtailment_cost = 0

# Note that this order is hard-coded and is expected to be maintained throughout the program.
power_tech_index = {
        "natural_gas":      0,
        "wind":             1,
        "solar":            2,
        "nuclear":          3}

#%% Scenario settings

# -----------------------------------------------------------------------------

# Cost

capital_cost_ngcc_array = np.array([969 * 2])              # $/kW
capital_cost_wind_array = np.array([1686])              # $/kW
capital_cost_solar_array = np.array([2277])             # $/kW
capital_cost_nuclear_array = np.array([5880])           # $/kWh

capital_cost_storage_array = np.array([1000])              # $/kWh
# np.array([0.01, 0.1, 1, 10, 100, 1000])          # $/kWh
                                        
storage_charging_efficiency_array = np.array([1**0.5])      # Fraction
storage_charging_duration_array = np.array([1])      # hour

ng_fuel_cost_array = np.array([3 * 2])                      # $/mmBTU
unmet_demand_cost_array = np.array([10])                # $/kWh

# -----------------------------------------------------------------------------

# Data selection

# Data selection

data_length = demand.size
simulation_start_array =  np.array([data_length - HOUR_IN_1_YEAR])
simulation_end_array =  np.array([data_length])

# -----------------------------------------------------------------------------

# Model selection

# core_model_file = 'Core_Model_FakeCurtailment'
core_model_file = 'Core_Model_StorageDuration'

# -----------------------------------------------------------------------------

# 19 technology assumption variables, 5 modeling control variables, 3+2 input data variables

inputs1 = {
        # Programming assumptions
        "directory_project":                    directory_project,
        "directory_input":                      directory_input,
        "directory_output":                     directory_output,
        "PRINT_FIGURE":                         PRINT_FIGURE,
        "DATA_TYPE":                            DATA_TYPE,
        
        # Power generation technologies
        "power_tech_index":                     power_tech_index,
        "efficiency_power":                     efficiency_power,
        "capital_cost_ngcc_array":              capital_cost_ngcc_array,
        "capital_cost_wind_array":              capital_cost_wind_array,
        "capital_cost_solar_array":             capital_cost_solar_array,
        "capital_cost_nuclear_array":           capital_cost_nuclear_array,
        
        # Fuel cost
        "ng_fuel_cost_array":                   ng_fuel_cost_array,
        "nuclear_fuel_cost":                    nuclear_fuel_cost,
        "storage_fuel_cost":                    storage_fuel_cost,

        # Energy storage technologies
        "capital_cost_storage_array":           capital_cost_storage_array,        
        "storage_charging_efficiency_array":    storage_charging_efficiency_array,
        "storage_charging_duration_array":      storage_charging_duration_array,

        # Unmet demand
        "unmet_demand_cost_array":              unmet_demand_cost_array,
        "curtailment_cost":                     curtailment_cost,
        
        # Other "default" assumptions
        "variable_OM_cost_power":               variable_OM_cost_power,
        "variable_OM_cost_storage":             variable_OM_cost_storage,
        "fixed_OM_cost_power":                  fixed_OM_cost_power,
        "fixed_OM_cost_storage":                fixed_OM_cost_storage,                    
        "capital_charge_rate_power":            capital_charge_rate_power,
        "capital_charge_rate_storage":          capital_charge_rate_storage,
        
        # Input data
        "demand":                               demand,  
        "wind_capacity_factor":                 wind_capacity_factor,
        "solar_capacity_factor":                solar_capacity_factor,
        
        # Dealing with input data
        # "year_simulation_array":                year_simulation_array,
        "simulation_start_array":               simulation_start_array,  
        "simulation_end_array":                 simulation_end_array,

        "core_model_file":                      core_model_file
        } 

# Call Loop_Model function
temp_folder = loop_model(inputs1)
copy2(__file__, temp_folder)

# -----------------------------------------------------------------------------

#inputs2 = inputs1.copy()
#inputs2["core_model_file"] = 'Core_Model_FakeCurtailment'
#
## Call Loop_Model function
#temp_folder = loop_model(inputs2)
#copy2(__file__, temp_folder)

# -----------------------------------------------------------------------------

#inputs3 = inputs1.copy()
#inputs3["core_model_file"] = 'Core_Model_NoCurtailment'
#
## Call Loop_Model function
#temp_folder = loop_model(inputs3)
#copy2(__file__, temp_folder)

# -----------------------------------------------------------------------------

#inputs4 = inputs1.copy()
#inputs4["capital_cost_ngcc_array"] = np.array([1e10])
#
## Call Loop_Model function
#temp_folder = loop_model(inputs4)
#copy2(__file__, temp_folder)

#------------------------------------------------------------------------------

#inputs5 = inputs4.copy()
#inputs5["core_model_file"] = 'Core_Model_FakeCurtailment'
#
## Call Loop_Model function
#temp_folder = loop_model(inputs5)
#copy2(__file__, temp_folder)

#------------------------------------------------------------------------------

#inputs6 = inputs4.copy()
#inputs6["core_model_file"] = 'Core_Model_NoCurtailment'
#
## Call Loop_Model function
#temp_folder = loop_model(inputs6)
#copy2(__file__, temp_folder)