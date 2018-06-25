# -*- coding: utf-8 -*-
"""
Script_SingleScenario_results.py

Motivation
    Generate "representive" figures for an optimizaiton run

History
    Feb 18, 2018 some old codes
    [Likely that I did not do anything between February and June]
    Jun 7, 2018  completely rewrote the code
    Jun 14 & 18, 2018 added comments
    Jun 19, 2018
        rewrote the "one-scenario" script to relect changes in file IOs.
        packaged the "one-scenario" script into a function so that I could run 
        the anlysis and plotting for many scenarios.
        
    Jun 19, 2018
        moved the (actual) functions to Funct_Graphics.py
    Jun 20, 2018
        changed the file name.
    Jun 21-22, 2018
        dynamically determined the time range
    
@author: Fan
"""
#import sys
#import numpy as np
#from Funct_Graphics import func_graphics_dispatch_mix_1scenario
#from Funct_Graphics import func_graphics_dispatch_mix_time_selection

import os
from itertools import product
from Funct_Graphics import func_optimization_results_time_series_1scenario

##%%
## -----------------------------------------------------------------------------
## func_plotting_time_series_results_1scenario()
##
## Function: 
##   Given the locations (directories or file paths), load the data, perform the
##   the analysis, generate the figures, and save the figures to files.     
## 
## Input
##   A DICT variable named input_data, with the following keys:
##    DATA_TYPE
##    optimization_results_file_path
##    directory_output
##    graphics_file_name_prefix
##    graphics_file_name_root
##    SAVE_FIGURES_TO_PDF
##    time_range_1
##    time_range_2
##
## Output    
##   Five groups of time-series figures for an optimization run.
##   If you choose to save the files, five files will be saved.
##
##   Five groups
##       1   dispatch mix and demand mix for all hourly data
##       2-3 dispatch mix and demand mix for a selected range of data
##       4-5 dispatch mix and demand mix for another selected range of data
##    
## History
##   June 3, 2018 wrote the code
##   June 19, 2018 packaged the code into this function
## -----------------------------------------------------------------------------
#
#def func_plotting_time_series_results_1scenario(input_data):
#    
#    # -------------------------------------------------------------------------
#
#    DATA_TYPE = input_data["DATA_TYPE"]
#    optimization_results_file_path = input_data["optimization_results_file_path"]
#    directory_output = input_data["directory_output"]
#    graphics_file_name_prefix = input_data["graphics_file_name_prefix"]
#    graphics_file_name_root = input_data["graphics_file_name_root"]
#    SAVE_FIGURES_TO_PDF = input_data["SAVE_FIGURES_TO_PDF"]
#    time_range_1 = input_data["time_range_1"]
#    time_range_2 = input_data["time_range_2"]
#
#    # -------------------------------------------------------------------------
#
#    # load the data
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
#    # load the data
#    
#    power_tech_index = model_inputs['power_tech_index']
#    demand = model_inputs['demand']
#    dispatched_power = model_results['dispatched_power']
#    dispatched_storage_discharge = model_results['dispatched_storage_discharge']
#    
#    dispatched_storage_charge = model_results['dispatched_storage_charge']
#    unmet_demand = model_results['unmet_demand']
#    dispatched_curtailment = model_results['dispatched_curtailment']
#    
#    dispatched_curtailment = np.array(dispatched_curtailment)
#    
#    # cvx.sum_entries(dispatched_power, axis=0).T + dispatched_storage_discharge + unmet_demand 
#    # == demand + dispatched_storage_charge
#    
#    # -------------------------------------------------------------------------
#    
#    # quick test
#    
#    system_balance = \
#        np.sum(dispatched_power, axis = 0) + dispatched_storage_discharge.flatten() + \
#        unmet_demand.flatten() - demand - dispatched_storage_charge.flatten()
#    
#    if np.abs(np.sum(system_balance)) > 1:
#         sys.exit("Value error! system energy balance broken!")
#    
#    # --------------------------------------------------------------------------
#    
#    # Figures 1 dispatch mix and demand mix
#    #   using func_graphics_dispatch_mix_1scenario()
#    
#    # Right now, 12 figures will be generated.
#    # 2+2 (supply+demand) figures for each time resolution
#    # In total, three time resolutions (hourly, daily, weekly)
#    
#    # dispatched_results_matrix
#    # row: time_steps
#    # column: technology
#    dispatched_results_matrix = np.column_stack(
#            (dispatched_power.T, 
#             dispatched_storage_discharge,
#             unmet_demand,
#             ))
#    
#    demand_results_matrix = np.column_stack(
#            (demand, 
#             dispatched_storage_charge,
#             dispatched_curtailment.T)
#            )
#    
#    legend_list_dispatch = sorted(power_tech_index.keys(), key=lambda x: x[1])
#    legend_list_dispatch.append('storage')
#    legend_list_dispatch.append('unmet demand')
#    
#    legend_list_demand = ['demand', 'storage charge', 'curtailed generation']
#    
#    graphics_file_name_1 = \
#        graphics_file_name_prefix + 'dispatch_and_demand_mix' + \
#        graphics_file_name_root + "{}_{}".format(0, 'end')
#    
#    input_data = {
#            "demand":                       demand,
#            "dispatched_results_matrix":    dispatched_results_matrix,
#            "demand_results_matrix":        demand_results_matrix,
#            "directory_output":             directory_output,
#            "graphics_file_name":           graphics_file_name_1,
#            "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,        
#            "legend_list_dispatch":         legend_list_dispatch,
#            "legend_list_demand":           legend_list_demand,         
#            }
#    
#    func_graphics_dispatch_mix_1scenario(input_data)
#    
#    # -------------------------------------------------------------------------
#    
#    # Figures 2(a) dispatch mix
#    #   using func_graphics_dispatch_mix_time_selection() for one full year
#        
#    # 2 figures will be generated
#    
#    # dispatched_results_matrix
#    # row: time_steps
#    # column: technology
#    dispatched_results_matrix = np.column_stack(
#            (dispatched_power.T, 
#             dispatched_storage_discharge,
#             unmet_demand)
#            )
#    
#    legend_list = sorted(power_tech_index.keys(), key=lambda x: x[1])
#    legend_list.append('storage')
#    legend_list.append('unmet demand')
#    
#    graphics_file_name_2a = \
#        graphics_file_name_prefix + 'dispatch_mix' + \
#        graphics_file_name_root + "{}_{}".format(time_range_1[0], time_range_1[1])
#            
#    input_data = {
#            "time_range":                   time_range_1,
#            "demand":                       demand,
#            "mix_matrix":                   dispatched_results_matrix,
#            "directory_output":             directory_output,
#            "graphics_file_name":           graphics_file_name_2a,
#            "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
#            "title_text":                   "dispatch mix",
#            "legend_list":                  legend_list,        
#            }
#    
#    func_graphics_dispatch_mix_time_selection(input_data)
#    
#    # -------------------------------------------------------------------------
#    
#    # Figures 2(b) demand mix
#    #   using func_graphics_dispatch_mix_time_selection() for one full year
#    
#    # 2 figures will be generated
#    
#    demand_results_matrix = np.column_stack(
#            (demand, 
#             dispatched_storage_charge,
#             dispatched_curtailment.T)
#            )
#    
#    legend_list = ['demand', 'storage charge', 'curtailed generation']
#    
#    graphics_file_name_2b = \
#        graphics_file_name_prefix + 'demand_mix' + \
#        graphics_file_name_root + "{}_{}".format(time_range_1[0], time_range_1[1])
#    
#    input_data = {
#            "time_range":                   time_range_1,        
#            "mix_matrix":                   demand_results_matrix,
#            "directory_output":             directory_output,
#            "graphics_file_name":           graphics_file_name_2b,
#            "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
#            "title_text":                   "demand mix",
#            "legend_list":                  legend_list,        
#            }
#    
#    func_graphics_dispatch_mix_time_selection(input_data)
#    
#    # -------------------------------------------------------------------------
#    
#    # Figures 3(a) dispatch mix
#    #   using func_graphics_dispatch_mix_time_selection() for 19 weeks
#    
#    # 2 figures will be generated
#    
#    # -------------------------------------------------------------------------
#    
#    # time_range_2 = (7*24, 20*7*24)
#    
#    # dispatched_results_matrix
#    # row: time_steps
#    # column: technology
#    dispatched_results_matrix = np.column_stack(
#            (dispatched_power.T, 
#             dispatched_storage_discharge,
#             unmet_demand)
#            )
#    
#    legend_list = sorted(power_tech_index.keys(), key=lambda x: x[1])
#    legend_list.append('storage')
#    legend_list.append('unmet demand')
#    
#    graphics_file_name_3a = \
#        graphics_file_name_prefix + 'dispatch_mix' + \
#        graphics_file_name_root + "{}_{}".format(time_range_2[0], time_range_2[1])
#    
#    input_data = {
#            "time_range":                   time_range_2,
#            "demand":                       demand,
#            "mix_matrix":                   dispatched_results_matrix,
#            "directory_output":             directory_output,
#            "graphics_file_name":           graphics_file_name_3a,
#            "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
#            "title_text":                   "dispatch mix",
#            "legend_list":                  legend_list,        
#            }
#    
#    func_graphics_dispatch_mix_time_selection(input_data)
#    
#    # -------------------------------------------------------------------------
#    
#    # Figures 3(b) demand mix
#    #   using func_graphics_dispatch_mix_time_selection() for 19 weeks
#    
#    # 2 figures will be generated
#    
#    demand_results_matrix = np.column_stack(
#            (demand, 
#             dispatched_storage_charge,
#             dispatched_curtailment.T)
#            )
#    
#    legend_list = ['demand', 'storage charge', 'curtailed generation']
#    
#    graphics_file_name_3b = \
#        graphics_file_name_prefix + 'demand_mix' + \
#        graphics_file_name_root + "{}_{}".format(time_range_2[0], time_range_2[1])
#    
#    input_data = {
#            "time_range":                   time_range_2,        
#            "mix_matrix":                   demand_results_matrix,
#            "directory_output":             directory_output,
#            "graphics_file_name":           graphics_file_name_3b,
#            "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
#            "title_text":                   "demand mix",
#            "legend_list":                  legend_list,        
#            }
#    
#    func_graphics_dispatch_mix_time_selection(input_data)

# -----------------------------------------------------------------------------

#%% Script

# -----------------------------------------------------------------------------
# Loop values for the loop

# ['1e-2', '1e-1', '1e0', '1e1', '1e2', '1e3']
# ['without_NG', 'with_NG']

storage_scenario_list = ['1e-2', '1e-1', '1e0', '1e1', '1e2', '1e3']
ng_scenario_list =  ['without_NG', 'with_NG']

# -----------------------
# Common values for the loop

SAVE_FIGURES_TO_PDF = 1

directory_project = os.path.dirname(os.path.realpath(__file__))
directory_project = directory_project + '/'
directory_output = directory_project + "Plots_Scenario1/"

# -----------------------

# Use a loop to plot figures for different optionmization runs

for storage_scenario, ng_scenario in product(storage_scenario_list, ng_scenario_list):

    graphics_file_name_prefix = "storage_scenario_"
    graphics_file_name_root = "_{}_{}_".format(storage_scenario, ng_scenario)

    optimization_results_file_path = directory_project + \
        "Results_Base/20180514/{}/20180514_{}/optimization_related.pkl".format(ng_scenario, storage_scenario)

    input_data ={
        "optimization_results_file_path":   optimization_results_file_path,
        "directory_output":             directory_output,
        "graphics_file_name_prefix":    graphics_file_name_prefix,
        "graphics_file_name_root":      graphics_file_name_root,
        "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
        }

    # call the function to plot figures
    func_optimization_results_time_series_1scenario(input_data)