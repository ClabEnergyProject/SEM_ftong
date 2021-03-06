# -*- coding: utf-8 -*-
"""
Script_StorageAnalysis_AlternativeSize.py

History
    June 3, 2018 initiated and finished.
    June 18, 2018 
        added additional comments.
        changed variable names
            met_energy_ratio --> discharge_met_energy_percentage
            met_energy_ratio_derivative --> discharge_met_energy_percentage_derivative
        split the plotting codes into functions
    June 19, 2018
        packaged the "one-scenario" script into a function so that I could run 
        the anlysis and plotting for many scenarios. 
        
    June 19, 2018
        moved all "major" functions to Funct_Analysis_Storage.py
        moved the function func_plotting_2yaxes() to Supporting_Information.py

@author: Fan Tong
"""

from __future__ import division
import numpy as np
import os
#import matplotlib.pyplot as plt
#import pickle
from itertools import product
#from matplotlib.backends.backend_pdf import PdfPages
#from Supporting_Functions import func_plotting_2yaxes
from Supporting_Functions import func_load_optimization_results
from Funct_Analysis_Storage import func_storage_analysis_alternative_size

#%%
# -----------------------------------------------------------------------------
# func_alternative_storage_analysis()
#
# Motivation: perform the analysis - taken the optimization results as given, 
#   would a smaller-sized storage perform the same role as the larger storage
#   determined in the optimizaiton.
# 
# Input
#   A DICT variable named, input_data, with the following keys:
#    alternative_size   
#    storage_optimization_discharge
#    storage_optimization_capacity    
#    storage_optimization_soc
#    storage_optimization_capacity
#  Basically, the optimization results and alterantive storage sizes
#
# Output    
#  A DICT variable named, outputs, with the following keys:
#    discharge_unmet_energy
#    discharge_unmet_energy_percentage
#    discharge_unmet_hour
#    discharge_unmet_hour_percentage
#  Basically, the analytical results from the analysis - when does the smaller-
#   sized storage fail, and fail by how much.
#
# History
#   June 3, 2018 wrote the code
#   June 18, 2018 added comments
# -----------------------------------------------------------------------------

#def func_alternative_storage_analysis(input_data):
#
#    # -------------------------------------------------------------------------
#    
#    # Get the results from an optimizaiton
#    
#    storage_charging_efficiency = input_data['storage_charging_efficiency']
#    storage_optimization_charge = input_data['storage_optimization_charge']
#    storage_optimization_discharge = input_data["storage_optimization_discharge"]
#    storage_optimization_soc = input_data["storage_optimization_soc"]
#    storage_optimization_capacity = input_data["storage_optimization_capacity"]
#    
#    storage_test_capacity = storage_optimization_capacity * input_data["alternative_size"]
#    
#    # Total time steps
#    N = storage_optimization_soc.size    
#    
#    # -------------------------------------------------------------------------
#    
#    # Preparation for the loop
#    
#    time_series = np.arange(0, N)
#    
#    # There are five variables with the new storage
#    # [1] state of charge
#    # [2-3] discharge and charging energies - implicit in calculations
#    # [4-5] gaps of discharging and charging energies from the new storage compared to the old one.
#    
#    storage_test_soc = np.zeros(N+1)
#    storage_test_soc[0] = min(storage_optimization_soc[0], storage_test_capacity)
#    
#    storage_test_discharge = np.zeros(N)
#    storage_test_charge = np.zeros(N)
#    storage_test_discharge_gap = np.zeros(N)
#    storage_test_charge_gap = np.zeros(N)
#        
#    # -------------------------------------------------------------------------
#
#    # Fan Tong's version, seems working better than Ken Caldeira's
#    
#    # This analysis is simple, the idea is to move forward in time to check if
#    #   a smaller-sized storage can fulfuil the roles of a larger-sized storage
#    #   which was determined in the optimizaiton. The "roles" of a storage here
#    #   are discharging energy time series and charging energy time series.
#    # In this calculation,
#    #   we move forward with time,
#    #   we take the discharging and charging energies from the grid as given,
#    #   if at a particular time setup, the smaller-sized storage faced trouble
#    #       to discharge or charge fully as expected, we move on.
#    
#    # The key insight is to understand where the smaller-sized energy storage
#    #   technology would fail?
#    # It would fail in two scenarios
#    #   in a discharging event, it hits a zero-energy state before a full discharge,
#    #   in a charging event, it hits the full-capacity state before a full charge.
#    
#    # An area that can easily confuse people (including myself) is the definitions
#    #   of charging and discharging energies at the storage side and at the grid side.
#    # In the optimizaiton, both charging and discharging energies are defined at
#    #   the grid side. The variable names are storage_optimization_charge[i],
#    #   and, storage_optimization_charge[i]
#    # Accordingly, at the storage side, the charging and discharging energies
#    #   are storage_optimization_charge[i] * storage_charging_efficiency, and
#    #   storage_optimization_charge[i] / storage_charging_efficiency.
#    
#    for i in time_series:
#        
#        # current time step is i
#        
#        # deal with charging power flow
#        
#        if storage_optimization_charge[i] > 0:
#            storage_test_charge[i] = min(
#                    (storage_test_capacity - storage_test_soc[i]) / storage_charging_efficiency, 
#                    storage_optimization_charge[i])
#            
#            storage_test_soc[i+1] = storage_test_soc[i] + storage_test_charge[i] * storage_charging_efficiency
#            storage_test_charge_gap = storage_optimization_charge[i] - storage_test_charge[i]    
#        
#        # deal with discharging power flow
#        
#        else:
#            storage_test_discharge[i] = min(
#                    storage_test_soc[i] * storage_charging_efficiency, storage_optimization_discharge[i])
#            
#            storage_test_soc[i+1] = storage_test_soc[i] - storage_test_discharge[i] / storage_charging_efficiency
#            storage_test_discharge_gap[i] = storage_optimization_discharge[i] - storage_test_discharge[i]
#
#    # -------------------------------------------------------------------------
#    # Ken Caldeira's implementation, March, 2018
#    
#    # Modified to take into Ken's version
#    # The key differences are that (1) one equation updates storage_soc, (2) remove the if-elese structure
#    
#    # It seems working fine most of the time, but there seems to be errors with "with NG" scenarios.
#    
##    for i in time_series:
##        
##        storage_test_charge[i] = min(
##                (storage_test_capacity - storage_test_soc[i]) / storage_charging_efficiency, 
##                storage_optimization_charge[i])           
##
##        storage_test_discharge[i] = min(storage_test_soc[i] * storage_charging_efficiency, storage_optimization_discharge[i])
##        storage_test_soc[i+1] = storage_test_soc[i] + storage_test_charge[i] * storage_charging_efficiency - storage_test_discharge[i] / storage_charging_efficiency
##    
##        storage_test_discharge_gap[i] = storage_optimization_discharge[i] - storage_test_discharge[i]
##        storage_test_charge_gap = storage_optimization_charge[i] - storage_test_charge[i]
#
## -----------------------------------------------------------------------------
#
#    # Calculate the energy-counts (kWh) and time-hours (hrs) for the discharge
#    #   energy. Here I normalize them.
#    discharge_unmet_energy = np.sum(storage_test_discharge_gap)
#    discharge_unmet_hours = np.count_nonzero(storage_test_discharge_gap)
#    
#    discharge_unmet_energy_percentage = discharge_unmet_energy / np.sum(storage_optimization_charge)
#    discharge_unmet_hours_percentage = discharge_unmet_hours / np.size(N)
#    
##    print 'Unmet discharging power flows totaled {0:.0f}e9 kWh'.format(unmet_energy/1e9) + \
##        'for {0:.0f} hours.'.format(unmet_hours) + \
##        'This is equivlanet to {0:.0f}% of originally discharged energy'.format(unmet_energy_percentage*100) + \
##        'and {0:.0f}% of operation hours'.format(unmet_hours_percentage*100)
#    
#    # -------------------------------------------------------------------------
#
#    outputs = {
#            "discharge_unmet_energy":               discharge_unmet_energy,
#            "discharge_unmet_hours":                discharge_unmet_hours,
#            "discharge_unmet_energy_percentage":    discharge_unmet_energy_percentage,
#            "discharge_unmet_hours_percentage":     discharge_unmet_hours_percentage,
#            }
#    
#    return outputs

##%%
## -----------------------------------------------------------------------------
## func_plotting_2yaxes()
##
## Motivation: plot two lines with two y-axes
## 
## Input
##   A DICT variable named input_data, with the following keys:
##    x_data <numpy array>
##    y1_data <numpy array>
##    y2_data <numpy array>
##   and, a number of graphics controlling keys
##
## Output    
##   figure: <figure> object.
##    
## History
##   June 3, 2018 wrote the code
##   June 18, 2018 packaged the code into this function
## -----------------------------------------------------------------------------
#
#def func_plotting_2yaxes(input_data):
#    
#    # -------------------------------------------------------------------------
#    # get the input data
#    
#    figsize_oneplot = input_data['figsize_oneplot']
#    x_data = input_data['x_data']
#    y1_data = input_data['y1_data']
#    y2_data = input_data['y2_data']
#    
#    # -------------------------------------------------------------------------
#    # actual plotting
#    
#    figure = plt.figure(figsize = figsize_oneplot)
#    ax1 = figure.add_subplot(111)
#    ax1.plot(x_data, y1_data, 'b')
#    ax2 = ax1.twinx() 
#    ax2.plot(x_data, y2_data, 'r')
#   
#    # -------------------------------------------------------------------------
#    # decoration
#    
#    ax1.tick_params(axis='y', labelcolor='b')
#    ax2.tick_params(axis='y', labelcolor='r')    
#    
#    if "x_label" in input_data.keys():
#        ax1.set_xlabel(input_data["x_label"])
#
#    if "y1_label" in input_data.keys():
#        ax1.set_ylabel(input_data["y1_label"], color='b')
#        
#    if "y2_label" in input_data.keys():
#        ax2.set_ylabel(input_data["y2_label"], color='r')        
#    
#    if "title" in input_data.keys():
#        ax1.set_title(input_data["title"])
#
#    if "legend" in input_data.keys():
#        ax1.legend(input_data["legend"])
#    
#    return figure

##%%
## -----------------------------------------------------------------------------
## func_alternative_storage_graphics()
##
## Motivation: plot the analytical results from the alterantive storage analysis
## 
## Input
##   A DICT variable named input_data, with the following keys:
##    storage_optimization_discharge
##    storage_optimization_capacity    
##    alternative_size_list
##    discharge_unmet_energy_percentage
##    discharge_unmet_hours
##    discharge_met_energy_percentage  
##    SAVE_FIGURES_TO_PDF
##    directory_output
##    graphics_file_name
##
## Output    
##   Three figures about unmet discharge energy and/or its derivatives.
##    
## History
##   June 3, 2018 wrote the code
##   June 18, 2018 packaged the code into this function
## -----------------------------------------------------------------------------
#
#def func_alternative_storage_graphics(input_data):
#    
#    # -------------------------------------------------------------------------
#    # Get the input data
#    
#    # Supporting information
#    
#    storage_optimization_discharge = input_data['storage_optimization_discharge']
#    storage_optimization_capacity = input_data['storage_optimization_capacity']
#    
#    # Actual analytical results
#    
#    alternative_size_list = input_data['alternative_size_list']
#    discharge_unmet_energy_percentage = input_data['discharge_unmet_energy_percentage']
#    discharge_unmet_hours = input_data['discharge_unmet_hours']
#    discharge_met_energy_percentage = input_data['discharge_met_energy_percentage']
#    discharge_met_energy_percentage_derivative = input_data['discharge_met_energy_percentage_derivative'] 
#    
#    # Plotting related
#    
#    SAVE_FIGURES_TO_PDF = input_data['SAVE_FIGURES_TO_PDF']
#    directory_output = input_data['directory_output']
#    graphics_file_name = input_data['graphics_file_name']
#    
#    # -------------------------------------------------------------------------    
#    # Create the ouput folder    
#    
#    if SAVE_FIGURES_TO_PDF:
#        if not os.path.exists(directory_output):
#            os.makedirs(directory_output)
#                        
#        pdf_pages = PdfPages(
#            directory_output + graphics_file_name + '.pdf')
#    
#    # -------------------------------------------------------------------------
#    # Define the plotting style
#    
#    plt.style.use('default')
#    # plt.style.use('bmh')
#    # plt.style.use('fivethirtyeight')
#    # plt.style.use('seaborn-white')
#    plt.rcParams['font.family'] = 'serif'
#    plt.rcParams['font.serif'] =  'Helvetica ' #'Palatino' # 'Ubuntu'
#    plt.rcParams['font.monospace'] = 'Helvetica Mono' #'Palatino Mono' # 'Ubuntu'
#    plt.rcParams['font.size'] = 16
#    plt.rcParams['axes.labelsize'] = 16
#    plt.rcParams['axes.labelweight'] = 'bold'
#    plt.rcParams['axes.titlesize'] = 16
#    plt.rcParams['xtick.labelsize'] = 16
#    plt.rcParams['ytick.labelsize'] = 16
#    plt.rcParams['legend.fontsize'] = 14
#    plt.rcParams['figure.titlesize'] = 16
#    plt.rcParams['lines.linewidth'] = 2.0
#    plt.rcParams['grid.color'] = 'k'
#    plt.rcParams['grid.linestyle'] = ':'
#    plt.rcParams['grid.linewidth'] = 0.5
#    plt.rcParams['xtick.major.width'] = 2
#    plt.rcParams['xtick.major.size'] = 6
#    plt.rcParams['xtick.direction'] = 'in'
#    plt.rcParams['ytick.major.width'] = 2
#    plt.rcParams['ytick.major.size'] = 6
#    plt.rcParams['ytick.direction'] = 'in'
#    
#    # -------------------------------------------------------------------------
#    
#    # Figure 1 fraction of unmet demand and hour of unmet demand
#    
#    title_text = ("storage cost: " + storage_scenario + "$/kWh, " + ng_scenario + "\n" + 
#                   "capacity: {:0.0f}e6 kWh, ".format(storage_optimization_capacity/1e6) + 
#                   "discharged in {:0.1f} eq. cycles, ".format(np.sum(storage_optimization_discharge) / storage_optimization_capacity) +
#                   "over {} hours".format(np.count_nonzero(storage_optimization_discharge))
#                   )
#    
#    input_data_1 = {
#        'figsize_oneplot':      (8,6),
#        'x_data':               alternative_size_list,
#        'y1_data':              discharge_unmet_energy_percentage,
#        'y2_data':              discharge_unmet_hours,
#        'x_label':              'Alternative storage capacity (normalized by original storage capacity)',
#        'y1_label':             'Fraction of unmet discharge energy \n(normalized by total discharged energy)',
#        'y2_label':             'Number of hours\nwith unmet discharge energy',
#        'title':                title_text,
#        }
#    
#    figure1 = func_plotting_2yaxes(input_data_1)
#    
#    if SAVE_FIGURES_TO_PDF:
#        # plt.savefig(directory_project + 'plots/Unmet_energy&hours_'+ storage_scenario + '_' + ng_scenario + '.png', bbox_inches='tight')
#        pdf_pages.savefig(figure1, bbox_inches='tight')
#        plt.close()
#    
#    # ------------------------------------------------------------------------
#    
#    # Figure 2 fraction of met demand and hour of unmet demand
#
#    title_text = ("storage cost: " + storage_scenario + "$/kWh, " + ng_scenario + "\n" + 
#                   "capacity: {:0.0f}e6 kWh, ".format(storage_optimization_capacity/1e6) + 
#                   "discharged in {:0.1f} eq. cycles, ".format(np.sum(storage_optimization_discharge) / storage_optimization_capacity) +
#                   "over {} hours".format(np.count_nonzero(storage_optimization_discharge))
#                   )
#    
#    input_data_2 = {
#        'figsize_oneplot':      (8,6),
#        'x_data':               alternative_size_list,
#        'y1_data':              discharge_met_energy_percentage,
#        'y2_data':              discharge_unmet_hours,
#        'x_label':              'Alternative storage capacity (normalized by original storage capacity)',
#        'y1_label':             'Fraction of met discharge energy\n(normalized by total discharged energy)',
#        'y2_label':             'Number of hours\nwith unmet discharge energy',
#        'title':                title_text,
#        }
#    
#    figure2 = func_plotting_2yaxes(input_data_2)
#    
#    if SAVE_FIGURES_TO_PDF:
#        # plt.savefig(directory_project + 'plots/Met_energy&hours_'+ storage_scenario + '_' + ng_scenario + '.png', bbox_inches='tight')
#        pdf_pages.savefig(figure2, bbox_inches='tight')
#        plt.close()
#    
#    # ------------------------------------------------------------------------
#    
#    # Figure 3 derivatives of met-energy-percentage
#    
#    title_text = ("storage cost: " + storage_scenario + "$/kWh, " + ng_scenario + "\n" + 
#                   "capacity: {:0.0f}e6 kWh, ".format(storage_optimization_capacity/1e6) + 
#                   "discharged in {:0.1f} eq. cycles, ".format(np.sum(storage_optimization_discharge) / storage_optimization_capacity) +
#                   "over {} hours".format(np.count_nonzero(storage_optimization_discharge))
#                   )
#    
#    input_data_3 = {
#        'figsize_oneplot':      (8,6),
#        'x_data':               alternative_size_list[0:alternative_size_list.size-1],
#        'y1_data':              discharge_met_energy_percentage[0:alternative_size_list.size-1],
#        'y2_data':              discharge_met_energy_percentage_derivative,
#        'x_label':              'Alternative storage capacity (normalized by original storage capacity)',
#        'y1_label':             'Fraction of unmet discharge energy \n(normalized by total discharged energy)',
#        'y2_label':             'Derivatives',
#        'title':                title_text,
#        }
#    
#    figure3 = func_plotting_2yaxes(input_data_3)    
#    
#    if SAVE_FIGURES_TO_PDF:
#        # plt.savefig(directory_project + 'plots/Met_energy_derivatives_'+ storage_scenario + '_' + ng_scenario + '.png', bbox_inches='tight')
#        pdf_pages.savefig(figure3, bbox_inches='tight')
#        plt.close()
#        
#    # -----------------------------------------------------------------------------
#    # Write the PDF document to the disk
#    
#    if SAVE_FIGURES_TO_PDF:
#        pdf_pages.close()
#
##%%
## -----------------------------------------------------------------------------
## func_storage_analysis_alternative_size()
##
## Function: 
##   Given the locations (directories or file paths), load the data, perform the
##   the analysis, generate the figures, and save the figures to files.     
## 
## Input
##   A DICT variable named input_data, with the following keys:
##    alternative_size_list
##    SAVE_FIGURES_TO_PDF
##    file_path
##    graphics_file_name
##
## Output    
##   Three figures about unmet discharge energy and/or its derivatives.
##   You can choose to save these files into one PDF book.        
##    
## History
##   June 3, 2018 wrote the code
##   June 19, 2018 packaged the code into this function
## -----------------------------------------------------------------------------
#
#def func_storage_analysis_alternative_size(input_data):
#    
#    alternative_size_list = input_data['alternative_size_list']
#    optimization_results_file_path = input_data['optimization_results_file_path']
#    SAVE_FIGURES_TO_PDF = input_data['SAVE_FIGURES_TO_PDF']
#    directory_output = input_data['directory_output']
#    graphics_file_name = input_data['graphics_file_name']
#    
#    # -------------------------------------------------------------------------
#    
#    # DATA_TYPE = 'pkl'
#    
#    f = open(optimization_results_file_path, 'rb')
#    model_inputs, model_results = pickle.load(f)
#    
#    # -------------------------------------------------------------------------
#    
#    # Previously imported, but never used
#    
#    # demand = model_inputs['demand']
#
#    # -------------------------------------------------------------------------
#    
#    # Note that storage_optimization_charge and storage_optimization_discharge, are
#    # both defined on the grid side.
#    # so, from the storage perspective, 
#    # discharge* = storage_optimization_discharge / one-way efficiency
#    # charge* = storage_optimization_charge * one-way efficiency
#    
#    storage_optimization_charge = model_results["dispatched_storage_charge"]
#    storage_optimization_discharge = model_results["dispatched_storage_discharge"]    
#    storage_optimization_capacity = model_results["capacity_storage"]
#    storage_optimization_soc = model_results["storage_energy_soc"]
#    storage_charging_efficiency = model_inputs["storage_charging_efficiency"]
#    
#    # -------------------------------------------------------------------------
#    
#    # Test: 
#    #   for any time step, discharging energy and charging energy cannot be both nonzero.
#    #   In other word, the piece-by-piece product of the two variables should always be zero.
#    
#    test_variables = storage_optimization_charge * storage_optimization_discharge
#    print 'Test: for any time step, can both discharging power flow and charging power folw be nonzero?'
#    print 'Results (sum {discharging * charging)): ', np.sum(test_variables)
#    
#    if np.sum(test_variables) > 0:
#        raise ValueError("Test failed")
#    
#    # -------------------------------------------------------------------------    
#    
#    input_data = {
#            # Core assumptions
#            "storage_optimization_charge":       storage_optimization_charge,
#            "storage_optimization_discharge":    storage_optimization_discharge,
#            "storage_optimization_soc":          storage_optimization_soc,
#            "storage_optimization_capacity":     storage_optimization_capacity,
#            "storage_charging_efficiency":       storage_charging_efficiency,
#            "alternative_size":                  1,
#            }
#    
#    discharge_unmet_energy = np.zeros(alternative_size_list.shape)
#    discharge_unmet_hours = np.zeros(alternative_size_list.shape)
#    discharge_unmet_energy_percentage = np.zeros(alternative_size_list.shape)
#    discharge_unmet_hours_percentage = np.zeros(alternative_size_list.shape)
#    
#    for i in xrange(alternative_size_list.size):
#        
#        input_data['alternative_size'] = alternative_size_list[i]
#        
#        # Call the function to do the analysis
#        outputs = func_alternative_storage_analysis(input_data)
#        
#        discharge_unmet_energy[i] = outputs["discharge_unmet_energy"]
#        discharge_unmet_energy_percentage[i] = outputs["discharge_unmet_energy_percentage"]
#        discharge_unmet_hours[i] = outputs["discharge_unmet_hours"]
#        discharge_unmet_hours_percentage[i] = outputs["discharge_unmet_hours_percentage"]
#    
#    # -----------------------
#                
#    # some additional calculations    
#        
#    discharge_met_energy_percentage = (
#            1 - discharge_unmet_energy / np.sum(storage_optimization_discharge))
#    
#    # Calculate the derivative
#    
#    discharge_met_energy_percentage_derivative = np.zeros(discharge_met_energy_percentage.size - 1)    
#        
#    for i in xrange(discharge_met_energy_percentage_derivative.size):
#        
#        discharge_met_energy_percentage_derivative[i] = (
#                (discharge_met_energy_percentage[i+1] - discharge_met_energy_percentage[i]) / 
#                (alternative_size_list[i+1] - alternative_size_list[i])
#                )
#    
#    # -------------------------------------------------------------------------
#    
#    # Plotting    
#    
#    input_data = {
#        'storage_optimization_discharge':           storage_optimization_discharge,
#        'storage_optimization_capacity':            storage_optimization_capacity,
#        
#        'alternative_size_list':                    alternative_size_list,
#        'discharge_unmet_energy_percentage':        discharge_unmet_energy_percentage,
#        'discharge_unmet_hours':                    discharge_unmet_hours,
#        'discharge_met_energy_percentage':          discharge_met_energy_percentage,
#        'discharge_met_energy_percentage_derivative':   discharge_met_energy_percentage_derivative,
#        
#        'SAVE_FIGURES_TO_PDF':                      SAVE_FIGURES_TO_PDF,
#        'directory_output':                         directory_output,
#        'graphics_file_name':                       graphics_file_name,
#        }
#    
#    # call the function to plot figures
#    func_alternative_storage_graphics(input_data)

# -----------------------------------------------------------------------------

#%% Script
# -----------------------------------------------------------------------------
# Here is the actual script to run the analysis
#   calling the function defined above,     
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Common settings

# Test 20 cases, 0:5%:100% of the capacity
alternative_size_list = np.arange(0, 1.01, 0.05)

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

for ng_scenario, storage_scenario in product(ng_scenario_list, storage_scenario_list):

    optimization_results_file_path = directory_project + \
        "Results_Base/20180514/{}/20180514_{}/optimization_related.pkl".format(ng_scenario, storage_scenario)
    
    graphics_file_name = "Storage_analysis_alternative_size_" + storage_scenario + "_" + ng_scenario
    
    scenario_name = "storage cost: " + storage_scenario + "$/kWh, " + ng_scenario
    
    input_data = {
        "alternative_size_list":        alternative_size_list,
        "optimization_results_file_path":      optimization_results_file_path,
        "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
        "directory_output":             directory_output,
        "graphics_file_name":           graphics_file_name,
        "scenario_name":                scenario_name,
        }
    
    func_storage_analysis_alternative_size(input_data)
    
    temp_dict = func_load_optimization_results(optimization_results_file_path)
    model_inputs = temp_dict['model_inputs']
    model_results = temp_dict['model_results']