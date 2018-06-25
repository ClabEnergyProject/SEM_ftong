# -*- coding: utf-8 -*-
"""
Created on Tue May 15 21:45:09 2018

@author: Fan
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 21:40:43 2018

@author: Fan
"""

import os
import csv
import numpy as np
from shutil import copy2
import datetime
from itertools import product

#if CORE_MODEL_RUN == 'Formulation_A':
#    from 'Core_Model_' + CORE_MODEL_RUN import core_model
#elseif CORE_MODEL_RUN == 'Formulation_B'::
#    from Core_Model_NoCurtailment import core_model

from Post_Processing import post_processing
# from Post_Processing_Pickle import post_processing

def loop_model(inputs):
    
    directory_project = inputs['directory_project']
    #directory_input = inputs['directory_input']
    directory_output = inputs['directory_output']
    #PRINT_FIGURE = inputs['PRINT_FIGURE']
    
    unmet_demand_cost_array = inputs['unmet_demand_cost_array']
    curtailment_cost = inputs['curtailment_cost']
    capital_cost_storage_array = inputs['capital_cost_storage_array']
    ng_fuel_cost_array = inputs['ng_fuel_cost_array']
    capital_cost_ngcc_array = inputs['capital_cost_ngcc_array']
    capital_cost_wind_array = inputs['capital_cost_wind_array']
    capital_cost_solar_array = inputs['capital_cost_solar_array']
    capital_cost_nuclear_array = inputs['capital_cost_nuclear_array']
    
    power_tech_index = inputs['power_tech_index']
    efficiency_power = inputs['efficiency_power']
    variable_OM_cost_power = inputs['variable_OM_cost_power']
    variable_OM_cost_storage = inputs['variable_OM_cost_storage']
    fixed_OM_cost_power = inputs['fixed_OM_cost_power']
    fixed_OM_cost_storage = inputs['fixed_OM_cost_storage']
    
    storage_charging_efficiency_array = inputs['storage_charging_efficiency_array']
    storage_charging_duration_array = inputs['storage_charging_duration_array']
    capital_charge_rate_power = inputs['capital_charge_rate_power']
    capital_charge_rate_storage = inputs['capital_charge_rate_storage']
    nuclear_fuel_cost = inputs['nuclear_fuel_cost']
    storage_fuel_cost = inputs['storage_fuel_cost']
    
    simulation_start_array = inputs['simulation_start_array']
    simulation_end_array = inputs['simulation_end_array']
    demand = inputs['demand']
    wind_capacity_factor = inputs['wind_capacity_factor']
    solar_capacity_factor = inputs['solar_capacity_factor']

    core_model_file = inputs['core_model_file']      

    import_module = __import__(core_model_file)

    output_table = np.zeros([
        simulation_start_array.size *
        unmet_demand_cost_array.size * 
        capital_cost_storage_array.size * 
        ng_fuel_cost_array.size * 
        capital_cost_ngcc_array.size *
        capital_cost_wind_array.size * 
        capital_cost_solar_array.size * 
        capital_cost_nuclear_array.size * 
        storage_charging_efficiency_array.size *
        storage_charging_duration_array.size, 
        38 + 61])

    #%% The loop
    
    row_index = 0;
    
    for ii_time in xrange(simulation_start_array.size):
        # Get demand and capacity factor data
        simulation_start = simulation_start_array[ii_time]
        simulation_end = simulation_end_array[ii_time]
        
        demand = demand[simulation_start : simulation_end]
        wind_capacity_factor = wind_capacity_factor[simulation_start : simulation_end]
        solar_capacity_factor = solar_capacity_factor[simulation_start : simulation_end] 
        
        for iteration_value in product(
                unmet_demand_cost_array, 
                ng_fuel_cost_array, 
                capital_cost_ngcc_array,                 
                capital_cost_wind_array, 
                capital_cost_solar_array,
                capital_cost_nuclear_array,
                capital_cost_storage_array,
                storage_charging_efficiency_array,
                storage_charging_duration_array):

            # -----------------------------------------------------
            
            # Pre-processing

            unmet_demand_cost = iteration_value[0]
            
            # Fixed cost
            
            capital_cost_storage = iteration_value[6]
            capital_cost_ngcc = iteration_value[2]
            capital_cost_wind = iteration_value[3]
            capital_cost_solar = iteration_value[4]
            capital_cost_nuclear = iteration_value[5]
                        
            capital_cost_power = np.array([
                    capital_cost_ngcc,
                    capital_cost_wind,
                    capital_cost_solar,                                      
                    capital_cost_nuclear])

            annualized_capital_cost_power = capital_cost_power * capital_charge_rate_power # $/kW/yr
            annualized_capital_cost_storage = capital_cost_storage * capital_charge_rate_storage # $/kWh/yr                        
            
            fixed_cost_power = annualized_capital_cost_power + fixed_OM_cost_power
            fixed_cost_storage = annualized_capital_cost_storage + fixed_OM_cost_storage
            
            # Variable cost
            
            ng_fuel_cost = iteration_value[1]
            
            # variable_cost_power = np.array([ng_fuel_cost / 293.07 / ngcc_efficiency, 0, 0, 2.3/1000]) # $/kWh output
            variable_fuel_cost_power = np.array(
                    [ng_fuel_cost / 293.07, 0, 0, nuclear_fuel_cost]) / efficiency_power # $/kWh output                                
            variable_fuel_cost_storage = storage_fuel_cost
                    
            variable_cost_power = variable_OM_cost_power + variable_fuel_cost_power
            variable_cost_storage = variable_OM_cost_storage + variable_fuel_cost_storage
            
            # Storage specification
            
            storage_charging_efficiency = iteration_value[7]
            storage_charging_duration = iteration_value[8]
            
            print 'storage_charging_duration = ', storage_charging_duration
            
            # -----------------------------------------------------
            
            # 8 assumption variables, 3 input data variables, 9 supporting variables
            
            model_inputs = {
                    # Core assumptions
                    "power_tech_index":                     power_tech_index,
                    "fixed_cost_power":                     fixed_cost_power,
                    "fixed_cost_storage":                   fixed_cost_storage,
                    "variable_cost_power":                  variable_cost_power,
                    "variable_cost_storage":                variable_cost_storage,
                    "storage_charging_efficiency":          storage_charging_efficiency,
                    "storage_charging_duration":            storage_charging_duration,
                    "unmet_demand_cost":                    unmet_demand_cost,
                    "curtailment_cost":                     curtailment_cost,                                            
                    
                    # Input data
                    "demand":                               demand,
                    "wind_capacity_factor":                 wind_capacity_factor,
                    "solar_capacity_factor":                solar_capacity_factor,
                    
                    # Supportive variables (used in post-processing)
                    "ng_fuel_cost":                         ng_fuel_cost,
                    "capital_cost_power":                   capital_cost_power,
                    "capital_cost_storage":                 capital_cost_storage,
                    "annualized_capital_cost_power":        annualized_capital_cost_power,
                    "annualized_capital_cost_storage":      annualized_capital_cost_storage,
                    "variable_fuel_cost_power":             variable_fuel_cost_power,
                    "variable_fuel_cost_storage":           variable_fuel_cost_storage,
                    "simulation_start":                     simulation_start,
                    "simulation_end":                       simulation_end,
                    }
                                                         
            # -----------------------------------------------------
            
            # Command output
            
            print '\n----------------------------------------------'
            print 'Scenario: NG fuel cost %.0f/mmBtu, NG capital cost %.0f/kW, \
                wind capital cost %.0f/kW, solar capital cost %.0f/kW, \
                nuclear capital cost %.0f/kW,  storage capital cost %.0f/kWh, unmet demand cost %.0f/kWh' \
                %(ng_fuel_cost, 
                  capital_cost_ngcc,                                      
                  capital_cost_wind,
                  capital_cost_solar,
                  capital_cost_nuclear,                                       
                  capital_cost_storage, 
                  unmet_demand_cost)                                                   
            
            # -----------------------------------------------------
            
            # Function call: run the core model                        
            raw_results = import_module.core_model (model_inputs)
            
            # Function call: postprocessing                        
            output_table_row = post_processing (model_inputs, inputs, raw_results)
            
            # -----------------------------------------------------
            
            # Save the variables during the loop                                                        
            output_table[row_index, ...] = output_table_row
            row_index = row_index + 1
                    
    # -----------------------------------------------------------------------------
    
    # Save the SUMMARY-type results
    
    # Create the folder
    
    today = datetime.datetime.now()
    output_folder = directory_output + \
        str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2) + "_" + \
        str(today.hour).zfill(2) + str(today.minute).zfill(2) + str(today.second).zfill(2) +\
        "_Summary/"
    os.makedirs(output_folder)
    
    # save (copy-and-paste) the python source files

    copy2(directory_project + core_model_file + '.py', output_folder)
    copy2(directory_project + "Loop_Model.py", output_folder)    
    copy2(directory_project + "Post_Processing.py", output_folder)
    
    # save the structured results    
    
    copy2(directory_project + 'Results_header.csv', output_folder + 'Scenario_results.csv')
    
    # It writes the outputs as needed (in terms of significant numbers)
    myFile = open(output_folder + 'Scenario_results.csv', 'ab')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows('\n')
        writer.writerows(output_table)
    
    # print ending information to the command
    
    print today
    
    return output_folder