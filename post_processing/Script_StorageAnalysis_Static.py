# -*- coding: utf-8 -*-
"""
Script_StorageAnalysis_Static.py

Moviation: this script is used to plot a set of relevant figures about 
energy storage usage from an optimization

History
    Jun 10, 2018  initiated and finished
    Jun 18-19, 2018 updated, commented and fixed
    
    Jun 19, 2018 moved the function to Funct_Graphics_Storage.py
    Jun 20, 2018 updated the code for loading the optimizaiton results
    June 23-24, 2018 updated texts and labels on figures
    
@author: Fan
"""

from __future__ import division
import os
from itertools import product
#import numpy as np
from Funct_Graphics_Storage import func_graphics_storage_results_1scenario

##%%
## -----------------------------------------------------------------------------
## func_plotting_storage_results_1scenario
##
## Input
##   input_data, a DICT variable, containing inforamtion related to where to locate
##       the optimization results and where to put the output files
##   intput_side (optimization results)'
##       DATA_TYPE
##       directory_optimization_results
##   output_side (graphical outputs)
##       directory_output
##       graphics_file_name
##       SAVE_FIGURES_TO_PDF
##
## Output
##   8 or 15 figures depending on which function is called
##   a set of relevant figures about energy storage usage from an optimization
##
## Functions called
##   func_graphic_storage_static_1scenario()
##   func_graphic_storage_static_1scenario1(), depending on the cases.
##
## History
##   June 10, 2018 
## -----------------------------------------------------------------------------
#
#def func_plotting_storage_results_1scenario(input_data):
#    
#    DATA_TYPE = input_data["DATA_TYPE"]
#    optimization_results_file_path = input_data["optimization_results_file_path"]
#    directory_output = input_data["directory_output"]
#    graphics_file_name = input_data["graphics_file_name"]
#    SAVE_FIGURES_TO_PDF = input_data["SAVE_FIGURES_TO_PDF"]
#
#    # -------------------------------------------------------------------------
#    
#    # Load the data
#
#    if DATA_TYPE == "npz":
#    
#        # The file ABC.npz was created using the SAVEZ function of the numpy package.
#    
#        # ---------------------------------------------------------------------
#    
#        # Load the data file
#        npzfile = np.load(optimization_results_file_path)
#        
#        # Deal with dictionary variables
#    
#        # First note that when you saved dict variables into .npz files and then retrieve
#        # them back, they have data_type = object (more accurately, it is a numpy.ndarray
#        # type), rather than dictionary, so you have to use them slightly differently.
#        # However, model_results.item() is a dictionary type variable.
#        # So, you access the files like these, model_results.item()['unmet_demand']
#    
#        # ---------------------------------------------------------------------
#    
#        # Look for what is in the file
#        # The function will list all variable names
#    
#        model_inputs = npzfile['model_inputs'].item()
#        model_results = npzfile['model_results'].item()
#    
#    elif DATA_TYPE == "pkl":
#        
#        import pickle
#    
#        f = open(optimization_results_file_path, 'rb')
#        model_inputs, model_results = pickle.load(f)
#    
#    # -------------------------------------------------------------------------
#    
#    # Get the needed data and call the ploting function
#    
#    demand = model_inputs['demand']
#
#    dispatched_storage_charge = model_results["dispatched_storage_charge"]
#    dispatched_storage_discharge = model_results["dispatched_storage_discharge"]
#    storage_energy_soc = model_results["storage_energy_soc"]
#    capacity_storage = model_results["capacity_storage"]
#    
#    inputs = {
#            "storage_energy_soc":           storage_energy_soc,
#            "capacity_storage":             capacity_storage,
#            "dispatched_storage_discharge": dispatched_storage_discharge,
#            "dispatched_storage_charge":    dispatched_storage_charge,
#            "demand":                       demand,
#            "directory_output":             directory_output,
#            "graphics_file_name":           graphics_file_name,
#            "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
#            }
#
#    func_graphic_storage_static_1scenario(inputs)
#
#    # Same information.
#    # But instead of using subplots to combine figures, show each figure seperately.
#
#    # inputs["graphics_file_name"] = graphics_file_name + "_1"
#    # func_graphic_storage_static_1scenario_1(inputs)

#%% Script
# -----------------------------------------------------------------------------
# Here is the actual script to run the analysis
#   calling the function defined above,     
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

# Common settings

#DATA_TYPE = 'pkl'
SAVE_FIGURES_TO_PDF = 1

directory_project = os.path.dirname(os.path.realpath(__file__))
directory_project = directory_project + '/'
directory_output = directory_project + "Plots_Storage/"

# -----------------------------------------------------------------------------

# Loop values for the loop

# ['1e-2', '1e-1', '1e0', '1e1', '1e2', '1e3']
# ['without_NG', 'with_NG']

storage_scenario_list = ['1e-2']
ng_scenario_list = ['without_NG']

# -----------------------

# Use a loop to plot figures for different optionmization runs

for storage_scenario, ng_scenario in product(storage_scenario_list, ng_scenario_list):

    optimization_results_file_path = directory_project + \
        "Results_Base/20180514/{}/20180514_{}/optimization_related.pkl".format(ng_scenario, storage_scenario)

    graphics_file_name = "Storage_results_" + storage_scenario + "_" + ng_scenario

    input_data ={
        "optimization_results_file_path":   optimization_results_file_path,
        "directory_output":             directory_output,
        "graphics_file_name":           graphics_file_name,
        "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
        }

    func_graphics_storage_results_1scenario(input_data)
