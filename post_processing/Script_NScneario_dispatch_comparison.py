# -*- coding: utf-8 -*-
"""
Script_NScenario_dispatch_comparison.py

Purpose:
    compare the same variable from multiple scenarios
    generate two types of figures (whose x-axis is the time series for the optimizaiton)
        (1) the specific variable vs. natural time series
        (2) sorted variable time series vs. corresponding time series
    these figures are saved to Plots_Scenarios folder.    

History list
    Jun 4 & 9, 2018 Version 1
        got everything to work
    Jun 14, 2018 Version 2
        adapted to the changes function definitions in the Supoorting_Functions.py
        added a new set of figures (1b, 2b, 3b) for a new y axis (in terms of hourly-average demand)
    Jun 17, 2018
        changed the file name of the graphics output
    Jun 19, 2018 attempted to update but did not succeed
    Jun 20, 2018
        changed the file name.
        re-packaged the one-scenario script into a function.

@author: Fan Tong
"""

from __future__ import division
import os
from itertools import product
#import numpy as np
#import pickle
#from Funct_Graphics import func_graphics_dispatch_var_Nscenarios
from Funct_Graphics import func_optimization_results_dispatch_var_Nscenarios

##%%
## -----------------------------------------------------------------------------
## func_optimization_results_dispatch_var_Nscenarios()
##
## Function: generate figures comparing dispatch variables for a technology
##   across a set of optimization runs whose only difference was due to a change
##   in an assumption.
##
## Input
##   A DICT variable named input_data, that has the following keys
##       optimization_results_file_path_list
##       scenario_list_number
##       which_technology_to_compare
##       SAVE_FIGURES_TO_PDF
##       directory_output
##       title_text
##       legend_list
##   In a nutsheel, these input information tells where to locate the optimization
##       results, what is the distinction across different runs, where to save
##       the generated figures, and how to decorate the figures.
##
## Output
##   A PDF book containing 8 figures.
##   Read the description of func_graphics_dispatch_var_Nscenarios() for details
##
## Functions called
##   func_graphics_dispatch_var_Nscenarios()
##
## History
##   Jun 4, 9, 14, 2018 wrote the code
##   Jun 20, 2018 re-packaged into a function
## -----------------------------------------------------------------------------
#
#def func_optimization_results_dispatch_var_Nscenarios(input_data):
#
#    # load the input data
#    
#    optimization_results_file_path_list = input_data['optimization_results_file_path_list']
#    scenario_list_number = input_data['scenario_list_number']
#    which_technology_to_compare = input_data['which_technology_to_compare']
#    SAVE_FIGURES_TO_PDF = input_data['SAVE_FIGURES_TO_PDF']
#    graphics_file_name = input_data['graphics_file_name']
#    directory_output = input_data['directory_output']
#    title_text = input_data['title_text']
#    legend_list = input_data['legend_list']
#
#    # -----------------------------------------------------------------------------
#
#    f = open(optimization_results_file_path_list[0], 'rb')
#    model_inputs, model_results = pickle.load(f)
#    
#    power_tech_index = model_inputs['power_tech_index']
#    optimization_time_steps = len(model_inputs['demand'])
#    
#    # -----------------------------------------------------------------------------
#    
#    dispatched_results_matrix = \
#        np.zeros([optimization_time_steps, len(scenario_list_number)])
#    
#    for scenario_idx in xrange(len(scenario_list_number)):
#
#        # actually load the data
#    
#        f = open(optimization_results_file_path_list[scenario_idx], 'rb')
#        model_inputs, model_results = pickle.load(f)    
#            
#        if which_technology_to_compare == "storage":
#            dispatched_results = model_results["dispatched_storage_discharge"]
#            dispatched_results_matrix[:, scenario_idx] = \
#                np.reshape(dispatched_results, -1)
#        else:
#            dispatched_results = model_results["dispatched_power"]
#            dispatched_results_matrix[:, scenario_idx] = \
#                np.reshape(dispatched_results[power_tech_index[which_technology_to_compare], :], -1)
#    
#    # -----------------------------------------------------------------------------
#    # Graphics
#    
#    input_data = {
#            "demand":                       model_inputs['demand'],
#            "dispatched_results_matrix":    dispatched_results_matrix,
#            "directory_output":             directory_output,
#            "graphics_file_name":           graphics_file_name,
#            "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
#            "title_text":                   title_text,
#            "legend_list":                  legend_list,
#            }
#    
#    # call the function
#    
#    func_graphics_dispatch_var_Nscenarios(input_data)


# -----------------------------------------------------------------------------
#%% Script

# -----------------------------------------------------------------------------

# Common settings across multiple scenarios

SAVE_FIGURES_TO_PDF = 1

directory_project = os.path.dirname(os.path.realpath(__file__))
directory_project = directory_project + '/'
directory_output = directory_project + '/Plots_ScenarioN/'

# '1e-2', '1e-1', '1e0', '1e1', '1e2', '1e3'
scenario_list_number = [1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3]
scenario_list_string = ['1e-2', '1e-1', '1e0', '1e1', '1e2', '1e3']

legend_list = [i+ "$/kWh" for i in scenario_list_string]

# -----------------------------------------------------------------------------

# ['without_NG', 'with_NG']
ng_scenario_list = ['with_NG']

# "wind", "solar", "natural_gas", "storage"
which_technology_to_compare_list = ["wind", "solar", "natural_gas", "storage"]

for ng_scenario, which_technology_to_compare in \
    product(ng_scenario_list, which_technology_to_compare_list):
    
    graphics_file_name = (
            'storage_scenarios_' + ng_scenario + "_" + "dispatch_timeseries_" + 
            which_technology_to_compare)

    # You have to make sure that the optimization results are stored here
    # "Results_Base/20180514/{}/20180514_{}/optimization_related.pkl".format(
    #                ng_scenario, storage_scenario_list[storage_scenario_idx])
          
    optimization_results_file_path_list = [
            directory_project + \
            "Results_Base/20180514/{}/20180514_{}/optimization_related.pkl".format(
            ng_scenario, scenario) for scenario in scenario_list_string]

    if which_technology_to_compare == "storage":
        title_text = (
                which_technology_to_compare + 
                " discharged energy from storage scenarios, " + 
                ng_scenario)
    else:
        title_text = (
                which_technology_to_compare + 
                " generation from storage scenarios, " + 
                ng_scenario)

    # -----------------------------------------------------------------------------
    
    input_data = {
        'optimization_results_file_path_list':      optimization_results_file_path_list,
        'scenario_list_number':         scenario_list_number,
        'which_technology_to_compare':  which_technology_to_compare,
        'SAVE_FIGURES_TO_PDF':          SAVE_FIGURES_TO_PDF,
        'graphics_file_name':           graphics_file_name,
        'directory_output':             directory_output,
        'title_text':                   title_text,
        'legend_list':                  legend_list,
        }
    
    func_optimization_results_dispatch_var_Nscenarios(input_data)