# -*- coding: utf-8 -*-
"""
Created on Sun May 13 22:41:36 2018

@author: Fan
"""

#%% Previously used scenario settings

#capital_cost_wind_array = np.array([1500, 750, 375]) # $/kWh 
#capital_cost_solar_array = np.array([1500, 750, 375]) # $/kWh 
#capital_cost_nuclear_array = np.array([6000, 3000, 1500]) # $/kWh
#capital_cost_storage_array = np.array([300, 30, 3]) # $/kWh
#
#ng_fuel_cost_array = np.array([5, 10, 20]) # $/MJ
#
## np.array([0.4,0.3,0.2,0.1])
## np.linspace(0,0.3,31)
#unmet_demand_cost_array = np.array([10000000]) # $/kWh

# capital_cost_storage_array = np.array([300, 300/(10**0.2), 300/(10**0.4), 300/(10**0.6), 300/(10**0.8), 30, 30/(10**0.2), 30/(10**0.4), 30/(10**0.6), 30/(10**0.8), 3]) # $/kWh
# capital_cost_storage_array = np.array([0.1, 0.3, 1, 3, 10, 30, 100, 300, 1000])
# capital_cost_storage_array = np.array([0.01, 0.1, 1, 10, 100, 1000])          # $/kWh
capital_cost_storage_array = np.array([0.01])          # $/kWh

# capital_cost_nuclear_array = np.array([6000, 5500, 5000, 4500, 4000, 3500, 3000, 2500, 2000, 1500, 1000, 500]) # $/kWh

# np.array([0.4,0.3,0.2,0.1])
# unmet_demand_cost_array = np.linspace(0,0.3,31)
unmet_demand_cost_array = np.array([10])                # $/kWh
# unmet_demand_cost_array = np.array([6,15]) 

# define end time point so don't evaluate entire data series
simulation_block_index = np.array([1]) # Starting from 1 to 36
simulation_block_size = HOUR_IN_1_YEAR * 1
simulation_start_array = simulation_block_size * (simulation_block_index-1) + 0
simulation_end_array = simulation_block_size * (simulation_block_index-1) + simulation_block_size