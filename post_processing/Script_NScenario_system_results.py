# -*- coding: utf-8 -*-
"""
Script_NScenario_system_results.py

Purpose:
    compare the same variable from multiple scenarios
    generate two types of figures (whose x-axis is the time series for the optimization)
        (1) the specific variable vs. natural time series
        (2) sorted variable time series vs. corresponding time series
    these figures are saved to Plots_Scenarios folder.    

History
    Jun 17, 2018 initiated and finished the coding
    Jun 20, 2018         
        packaged the "one-scenario" script into a function so that I could run 
            the anlysis and plotting for many scenarios.
        changed the file name.
        added x_label input
    June 23-24, 2018 updated texts and labels on figures        

@author: Fan Tong
"""

from __future__ import division
import os
#import numpy as np
#import pickle
#from Funct_Graphics import func_graphics_system_results_Nscenarios
from Funct_Graphics import func_optimization_results_system_results_Nscenarios

##%%
## -----------------------------------------------------------------------------
## func_optimization_results_snapshot_Nscenarios()
##
## Function: generate "representative" results (figures) for a set of optimization 
##   runs whose only difference was due to a change in an assumption.
##
## Input
##   A DICT variable named input_data, that has the following keys
##       optimization_results_file_path_list
##       scenario_list_number
##       SAVE_FIGURES_TO_PDF
##       graphics_file_name
##       directory_output
##       x_label
##   In a nutsheel, these input information tells where to locate the optimization
##       results, what is the distinction across different runs, where to save
##       the generated figures, and how to decorate the figures.
##
## Output
##   A PDF book containing 8 figures.
##   Read the description of func_graphics_system_results_Nscenarios() for details
##
## Functions called
##   func_graphics_system_results_Nscenarios()
##
## History
##   Jun 17, 2018 wrote the code
##   Jun 20, 2018 re-packaged into a function
## -----------------------------------------------------------------------------
#
#def func_optimization_results_snapshot_Nscenarios(input_data):
#
#    # load the input data
#    
#    optimization_results_file_path_list = input_data['optimization_results_file_path_list']
#    scenario_list_number = input_data['scenario_list_number']
#    SAVE_FIGURES_TO_PDF = input_data['SAVE_FIGURES_TO_PDF']
#    graphics_file_name = input_data['graphics_file_name']
#    directory_output = input_data['directory_output']
#    x_label = input_data['x_label']
#
#    # -------------------------------------------------------------------------
#
#    # load the data from scenario to get "power_tech_index"
#
#    f = open(optimization_results_file_path_list[0], 'rb')
#    model_inputs, model_results = pickle.load(f)
#    
#    power_tech_index = model_inputs['power_tech_index']
#    
#    # -------------------------------------------------------------------------
#    
#    # prepare for the loop
#    
#    # 9 variables (matrix form) to be assembled
#    
#    storage_capacity_matrix = np.zeros([len(scenario_list_number)])
#    storage_discharge_matrix = np.zeros([len(scenario_list_number)])
#    storage_cycle_matrix = np.zeros([len(scenario_list_number)])
#    storage_investment_matrix = np.zeros([len(scenario_list_number)])
#    
#    power_capacity_matrix = np.zeros([len(power_tech_index), len(scenario_list_number)])
#    power_dispatch_matrix = np.zeros([len(power_tech_index), len(scenario_list_number)])
#    cost_power_matrix = np.zeros([len(power_tech_index), len(scenario_list_number)])
#    cost_everything_matrix = np.zeros([len(power_tech_index)+3, len(scenario_list_number)])
#    
#    optimum_cost_matrix = np.zeros([len(scenario_list_number)])
#    
#    # ----------------------
#    
#    # loop to extract and "combine" optimization results
#    
#    for scenario_idx in xrange(len(scenario_list_number)):
#    
#        # actually load the data
#    
#        f = open(optimization_results_file_path_list[scenario_idx], 'rb')
#        model_inputs, model_results = pickle.load(f)
#            
#        # ---------------------------------------------------------------------
#        
#        # Energy storage
#    
#        storage_discharge_matrix[scenario_idx] = (
#            sum(model_results["dispatched_storage_discharge"])
#            )
#        
#        storage_capacity_matrix[scenario_idx] = (
#            model_results["capacity_storage"]
#            )
#    
#        storage_cycle_matrix[scenario_idx] = (
#            sum(model_results["dispatched_storage_discharge"]) /
#            model_results["capacity_storage"]
#            )
#        
#        storage_investment_matrix[scenario_idx] = (
#            model_results["capacity_storage"] * model_inputs['capital_cost_storage']
#            )
#    
#        # ---------------------------------------------------------------------
#    
#        # Power generation
#    
#        power_capacity_matrix[:,scenario_idx] = \
#            np.reshape(model_results['capacity_power'], -1)
#    
#        power_dispatch_matrix[:,scenario_idx] = \
#            np.reshape(np.sum(model_results['dispatched_power'], axis=1), -1)
#    
#        power_dispatch_total = \
#            np.sum(model_results['dispatched_power'], axis = 1)
#    
#        cost_power_matrix[:,scenario_idx] = (
#            ((power_dispatch_total * model_inputs['variable_cost_power'] +
#             model_results['capacity_power'] * model_inputs['fixed_cost_power'])
#            / np.sum(model_inputs['demand'])))
#    
#        # ---------------------------------------------------------------------
#    
#        # Cost breakdown by "everything" (every type)
#        # power generation technologies, storage, unmet demand, curtailment
#    
#        storage_discharge_total = np.sum(model_results['dispatched_storage_discharge'])
#        storage_charge_total = np.sum(model_results['dispatched_storage_charge']) 
#        
#        cost_everything_matrix[0:len(power_tech_index),scenario_idx] = (
#            cost_power_matrix[:,scenario_idx])
#    
#        cost_everything_matrix[len(power_tech_index)+0,scenario_idx] = (
#            (storage_discharge_total * model_inputs['variable_cost_storage'] +
#             storage_charge_total * model_inputs['variable_cost_storage'] +
#             model_results["capacity_storage"] * model_inputs['fixed_cost_storage'])
#             / np.sum(model_inputs['demand']))
#    
#        cost_everything_matrix[len(power_tech_index)+1,scenario_idx] = (
#            np.sum(model_results['unmet_demand']) * model_inputs['unmet_demand_cost']
#            / np.sum(model_inputs['demand']))
#            
#        cost_everything_matrix[len(power_tech_index)+2,scenario_idx] = (
#            np.sum(model_results['dispatched_curtailment']) * model_inputs['curtailment_cost']
#            / np.sum(model_inputs['demand']))
#        
#        # ---------------------------------------------------------------------
#        
#        # Optimal system cost
#        
#        optimum_cost_matrix[scenario_idx] = (
#            model_results['optimum'] / np.sum(model_inputs['demand']))
#    
#    # -------------------------------------------------------------------------
#    # Graphics
#    
#    # Graphics settings
#    
#    input_data = {
#            "power_tech_index":             power_tech_index,
#            "demand":                       model_inputs['demand'],
#            "assumptions_matrix":           np.array(scenario_list_number),
#            "storage_discharge_matrix":     storage_discharge_matrix,
#            "storage_capacity_matrix":      storage_capacity_matrix,
#            "storage_cycle_matrix":         storage_cycle_matrix,
#            "storage_investment_matrix":    storage_investment_matrix,
#            "power_capacity_matrix":        power_capacity_matrix,
#            "power_dispatch_matrix":        power_dispatch_matrix,
#            "cost_power_matrix":            cost_power_matrix,
#            "cost_everything_matrix":       cost_everything_matrix,
#            "directory_output":             directory_output,
#            "graphics_file_name":           graphics_file_name,
#            "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
#            "x_label":                      x_label,
#            }    
#
#    # call the function to generate figures
#    
#    func_graphics_system_results_Nscenarios(input_data)

# -----------------------------------------------------------------------------
#%% Script

# -----------------------------------------------------------------------------

# Common settings across multiple scenarios

SAVE_FIGURES_TO_PDF = 1

x_label = 'Energy storage capital cost ($/kWh)'

directory_project = os.path.dirname(os.path.realpath(__file__))
directory_project = directory_project + '/'
directory_output = directory_project + '/Plots_ScenarioN/'

# [1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3]
# ['1e-2', '1e-1', '1e0', '1e1', '1e2', '1e3']
scenario_list_number = [1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3]
scenario_list_string = ['1e-2', '1e-1', '1e0', '1e1', '1e2', '1e3']

# -----------------------------------------------------------------------------

# 'without_NG', 'with_NG'
ng_scenario_list = ['without_NG', 'with_NG']

for ng_scenario in ng_scenario_list:

    graphics_file_name = 'storage_scenarios_' + ng_scenario + "_" + "system_results"

    # You have to make sure that the optimization results are stored here
    # "Results_Base/20180514/{}/20180514_{}/optimization_related.pkl".format(
    #                ng_scenario, storage_scenario_list[storage_scenario_idx])
          
    optimization_results_file_path_list = [
            directory_project + \
            "Results_Base/20180514/{}/20180514_{}/optimization_related.pkl".format(
            ng_scenario, scenario) for scenario in scenario_list_string]
    
    # -----------------------------------------------------------------------------
    
    input_data = {
        'optimization_results_file_path_list':      optimization_results_file_path_list,
        'scenario_list_number':         scenario_list_number,
        'SAVE_FIGURES_TO_PDF':          SAVE_FIGURES_TO_PDF,
        'graphics_file_name':           graphics_file_name,
        'directory_output':             directory_output,
        'x_label':                      x_label,
        }
    
    func_optimization_results_system_results_Nscenarios(input_data)