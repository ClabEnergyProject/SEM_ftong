# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 19:54:47 2018

@author: Fan
"""

from __future__ import division
import numpy as np
import os
# from itertools import product
from Supporting_Functions import func_load_optimization_results

#%% Script
# -----------------------------------------------------------------------------
# Here is the actual script to run the analysis
#   calling the function defined above,     
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Common settings

# -----------------------------

# (preparing to) load the data

SAVE_FIGURES_TO_PDF = 0

directory_project = os.path.dirname(os.path.realpath(__file__))
directory_project = directory_project + '/'
directory_output = directory_project + 'Plots_Storage/'

# -----------------------------------------------------------------------------

# Loops over optimization runs

# ['1e-2', '1e-1', '1e0', '1e1', '1e2', '1e3']
# ['without_NG', 'with_NG']

storage_scenario_list = ['1e-2']
ng_scenario_list = ['without_NG']

# ------------------------------

# actually load the data

#for ng_scenario, storage_scenario in product(ng_scenario_list, storage_scenario_list):
#
#    optimization_results_file_path = directory_project + \
#        "Results_Base/20180514/{}/20180514_{}/optimization_related.pkl".format(ng_scenario, storage_scenario)
#    
#    graphics_file_name = "Storage_analysis_alternative_size_" + storage_scenario + "_" + ng_scenario
#    
#    scenario_name = "storage cost: " + storage_scenario + "$/kWh, " + ng_scenario
#    
#    input_data = {
#        "optimization_results_file_path":      optimization_results_file_path,
#        "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
#        "directory_output":             directory_output,
#        "graphics_file_name":           graphics_file_name,
#        "scenario_name":                scenario_name,
#        }
#    
#    func_storage_analysis_alternative_size(input_data)

ng_scenario = ng_scenario_list[0]
storage_scenario = storage_scenario_list[0]
    
optimization_results_file_path = directory_project + \
        "Results_Base/20180514/{}/20180514_{}/optimization_related.pkl".format(ng_scenario, storage_scenario)

temp_dict = func_load_optimization_results(optimization_results_file_path)
model_inputs = temp_dict['model_inputs']
model_results = temp_dict['model_results']

storage_charging_efficiency = model_inputs['storage_charging_efficiency']
storage_optimization_charge = model_results['dispatched_storage_charge']
storage_optimization_discharge = model_results["dispatched_storage_discharge"]
storage_optimization_soc = model_results["storage_energy_soc"]
storage_optimization_capacity = model_results["capacity_storage"]

# Ok. So here, I have loaded the optimization assumptions and results

# -----------------------------------------------------------------------------

## Replicate the SOC propagation
#
#storage_optimization_soc1 = np.zeros(storage_optimization_soc.shape)
#
#storage_optimization_soc1[0] = storage_optimization_soc[0]
#
#for ii in xrange(len(storage_optimization_soc1)-1):
#    
#    storage_optimization_soc1[ii+1] = \
#        storage_optimization_soc1[ii] + \
#        storage_optimization_charge[ii] * storage_charging_efficiency - \
#        storage_optimization_discharge[ii] / storage_charging_efficiency
#        
## You will find that storage_optimization_soc1 and storage_optimization_soc1
##   are identical.
        
# -----------------------------------------------------------------------------        