# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 00:48:03 2018

@author: Fan
"""

import os
import sys
import datetime
import numpy as np
from operator import itemgetter
from Funct_Graphics import funct_graphics

def post_processing (model_inputs, inputs, model_results):    
    
    #%%
    # -------------------------------------------------------------------------
    
    # Get the general assumptions
    # break down the dictionary "inputs", which is defined in Script.py
    
    # Programming assumptions
    directory_input = inputs['directory_input']
    directory_output = inputs['directory_output']
    # directory_project = inputs['directory_project']
    PRINT_FIGURE = inputs['PRINT_FIGURE']
    DATA_TYPE = inputs['DATA_TYPE']

    # Power generation technologies
    power_tech_index = inputs['power_tech_index']
    efficiency_power = inputs['efficiency_power']
    # capital_cost_ngcc_array = inputs['capital_cost_ngcc_array']
    # capital_cost_wind_array = inputs['capital_cost_wind_array']
    # capital_cost_solar_array = inputs['capital_cost_solar_array']
    # capital_cost_nuclear_array = inputs['capital_cost_nuclear_array']
    
    # Fuel cost
    # ng_fuel_cost_array = inputs['ng_fuel_cost_array']
    nuclear_fuel_cost = inputs['nuclear_fuel_cost']
    # storage_fuel_cost = inputs['storage_fuel_cost']
    
    # Energy storage technologies
    # capital_cost_storage_array = inputs['capital_cost_storage_array']
    # storage_charging_efficiency_array = inputs['storage_charging_efficiency_array']
    # storage_charging_duration_array = inputs['storage_charging_duration_array']
    
    # Unmet demand
    # unmet_demand_cost_array = inputs['unmet_demand_cost_array']
    curtailment_cost = inputs['curtailment_cost']
    
    # Other "default" assumptions
    variable_OM_cost_power = inputs['variable_OM_cost_power']
    variable_OM_cost_storage = inputs['variable_OM_cost_storage']
    fixed_OM_cost_power = inputs['fixed_OM_cost_power']
    fixed_OM_cost_storage = inputs['fixed_OM_cost_storage']
    capital_charge_rate_power = inputs['capital_charge_rate_power']
    capital_charge_rate_storage = inputs['capital_charge_rate_storage']    

    # Input data
    #demand = inputs['demand']
#    wind_capacity_factor = inputs['wind_capacity_factor']
#    solar_capacity_factor = inputs['solar_capacity_factor']

    # Dealing with input data
    # year_simulation = inputs['year_simulation']
#    "simulation_start_array":               simulation_start_array,
#    "simulation_end_array":                 simulation_end_array,

    # -------------------------------------------------------------------------
    
    # Get the optimization inputs
    
    # break down the dictionary "model_inputs", which is defined in Loop_Model.py
    
    # Core assumptions
#    power_tech_index = model_inputs['power_tech_index']
    fixed_cost_power = model_inputs['fixed_cost_power']
    fixed_cost_storage = model_inputs['fixed_cost_storage']    
    variable_cost_power = model_inputs['variable_cost_power']
    variable_cost_storage = model_inputs['variable_cost_storage']    
    unmet_demand_cost = model_inputs['unmet_demand_cost']
    curtailment_cost = model_inputs['curtailment_cost']
    storage_charging_efficiency = model_inputs['storage_charging_efficiency']
    storage_charging_duration = model_inputs['storage_charging_duration']

    # Input data
    demand = model_inputs['demand']
#    wind_capacity_factor = model_inputs['wind_capacity_factor']    
#    solar_capacity_factor = model_inputs['solar_capacity_factor']

    # Supportive variables (used in post-processing)
    capital_cost_power = model_inputs['capital_cost_power']
    capital_cost_storage = model_inputs['capital_cost_storage']
    annualized_capital_cost_power = model_inputs['annualized_capital_cost_power']
    annualized_capital_cost_storage = model_inputs['annualized_capital_cost_storage']
    variable_fuel_cost_power = model_inputs['variable_fuel_cost_power']
    variable_fuel_cost_storage = model_inputs['variable_fuel_cost_storage']
    ng_fuel_cost = model_inputs['ng_fuel_cost']
    simulation_start = model_inputs['simulation_start']
    simulation_end = model_inputs['simulation_end']
    
    # -------------------------------------------------------------------------
    
    # Get the optimization results
    
    # break down the dictionary "model_results", which is defined in Core_Model.py
    
    # Core optimization results (decision variables)
    dispatched_power = model_results['dispatched_power']
    capacity_power = model_results['capacity_power']
    dispatched_storage_discharge = model_results['dispatched_storage_discharge']
    dispatched_storage_charge = model_results['dispatched_storage_charge']
    unmet_demand = model_results['unmet_demand']
    capacity_storage = model_results['capacity_storage']
    # storage_energy_soc = model_results['storage_energy_soc']

    # Curtailment
    dispatched_curtailment = model_results['dispatched_curtailment']
#    curtailment_solar = model_results['curtailment_solar']
#    curtailment_wind = model_results['curtailment_wind']
#    curtailment_nuclear = model_results['curtailment_nuclear']    
    
    # Optimization status
    solution_status = model_results['solution_status']
    optimum = model_results['optimum']    
    
    # Supporting information (used in post-processing)
    run_time = model_results['run_time']
    constraints_count = model_results['constraints_count']

    
    #%%
    # -------------------------------------------------------------------------  
    
    # Quick processing
    
    # dimension(dispatched_power) = (4, 8760)
    # sum over axis=0 implies the sum of power generation technology (at any time in axis=1)
    # sum over axis=1 implies the sum of all time (at any technology in axis=0)
    
    dispatched_storage_discharge_solution_total = np.sum(dispatched_storage_discharge)
    dispatched_storage_charge_solution_total = np.sum(dispatched_storage_charge) 
    dispatched_power_discharge_solution_total = np.sum(dispatched_power, axis = 1)  
    unmet_demand_solution_total = np.sum(unmet_demand)
    curtailment_solution_total = np.sum(dispatched_curtailment)
    
    print "curtailment_solution_total=", curtailment_solution_total
    
    # -------------------------------------------------------------------------    
    
    # Create the ouput folder
    
    today = datetime.datetime.now()
    output_folder = directory_output + \
        str(today.year) + str(today.month).zfill(2) + str(today.day).zfill(2) + "_" + \
        str(today.hour).zfill(2) + str(today.minute).zfill(2) + str(today.second).zfill(2)
    os.makedirs(output_folder)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)    
    
    #%% Text output
    
    # -------------------------------------------------------------------------
    
    # This is the best way to do the job.
    power_tech_string = ""
    for key in sorted(power_tech_index.keys(), key = itemgetter(1)):
        power_tech_string = power_tech_string + key + ", "

    # Ancillary information

    orig_stdout = sys.stdout
    f = open(output_folder + "\\output.txt", 'w')
    sys.stdout = f
    
    print "\n------------------------------------------------------------------------"
    print "solutions"
    print "------------------------------------------------------------------------\n"
    
    print 'time elapsed: %.1f'  %run_time, 'seconds'
    print >>orig_stdout, 'time elapsed: %.1f'  %run_time, 'seconds'
    
    print 'status:', solution_status
    print >>orig_stdout, 'status:', solution_status
    
    print 'number of constraints:', constraints_count
    print >>orig_stdout, 'number of constraints:', constraints_count
    
    print 'studied time periods (which hour?):', simulation_start, simulation_end
    print >>orig_stdout, 'studied time periods (which hour?):', simulation_start, simulation_end
    
    print 'Total system cost($): %.0f' %optimum
    print >>orig_stdout, 'Total system cost($): %.0f' %optimum
    
    print 'Average system cost ($/kWh): %.3f' %(optimum / np.sum(demand))
    print >>orig_stdout, 'Average system cost ($/kWh): %.3f' %(optimum / np.sum(demand))

    # -------------------------------------------------------------------------
    
    # Actual power generation
    
    print 'Generation (relative to demand) :', power_tech_string, dispatched_power_discharge_solution_total.T / np.sum(demand)
    
    print 'Other generation-equivalent (relative to demand), storage in, storage out, curtailment, unmet demand :', \
            (dispatched_storage_discharge_solution_total,
             dispatched_storage_charge_solution_total,
             curtailment_solution_total, 
             unmet_demand_solution_total) / np.sum(demand)
    
    # Generation capacity
    
    print 'Capacity of power generation (GW):', power_tech_string, (capacity_power.T / 1e6)
    print 'Capacity of energy storage (GWh):', (capacity_storage / 1e6)

    # -------------------------------------------------------------------------

    # Cost share by technology
    
#    print >>orig_stdout, dispatched_power_discharge_solution_total.shape
#    print >>orig_stdout, variable_cost_power.shape
#    print >>orig_stdout, capacity_power.shape
#    print >>orig_stdout, fixed_cost_power.shape
    
    cost_contributions_power = \
        ((dispatched_power_discharge_solution_total * variable_cost_power +
         capacity_power * fixed_cost_power) 
        / np.sum(demand))
        
    cost_contributions_storage = \
        ((dispatched_storage_discharge_solution_total * variable_cost_storage +
          dispatched_storage_charge_solution_total * variable_cost_storage +
          capacity_storage * fixed_cost_storage)
            / np.sum(demand))

    cost_contributions_unmet_demand = \
        ((unmet_demand_solution_total * unmet_demand_cost)
        / np.sum(demand))
        
    cost_contributions_curtailment = \
        ((curtailment_solution_total * curtailment_cost)
        / np.sum(demand))  
    
    print 'Contribution to system cost ($/kWh): ', power_tech_string, ' energy storage, unmet demand,', \
        np.append (cost_contributions_power, (cost_contributions_storage, cost_contributions_unmet_demand))
                        
    # Fixed cost - as a function of deployed capacity

    cost_contributions_fixed_cost_power = capacity_power * fixed_cost_power / np.sum(demand)
    cost_contributions_fixed_cost_storage = capacity_storage * fixed_cost_storage / np.sum(demand)
    
    print 'Fixed cost contribution ($/kWh):', power_tech_string, 'energy storage,', \
        np.append (cost_contributions_fixed_cost_power, cost_contributions_fixed_cost_storage)

    # Variable cost - as a function of utlization

    cost_contributions_variable_cost_power = \
        (dispatched_power_discharge_solution_total * variable_cost_power) / np.sum(demand)
    cost_contributions_variable_cost_storage = \
        (dispatched_storage_discharge_solution_total * variable_cost_storage +
         dispatched_storage_charge_solution_total * variable_cost_storage) / np.sum(demand)
    
    print 'Variable cost contribution ($/kWh):', power_tech_string, 'energy storage,', \
        np.append (cost_contributions_variable_cost_power, cost_contributions_variable_cost_storage)                
      
    # Capital cost

    cost_contributions_capital_power = capacity_power * annualized_capital_cost_power / np.sum(demand)
    cost_contributions_capital_storage = capacity_storage * annualized_capital_cost_storage / np.sum(demand)

    print 'Capital cost contribution ($/kWh):', power_tech_string, 'energy storage,', \
        np.append (cost_contributions_capital_power, cost_contributions_capital_storage)

    # Fuel cost

    cost_contributions_fuel_power = dispatched_power_discharge_solution_total * variable_fuel_cost_power / np.sum(demand)
    cost_contributions_fuel_storage = dispatched_storage_discharge_solution_total * variable_fuel_cost_storage / np.sum(demand)

    print 'Fuel cost contribution ($/kWh):', power_tech_string, 'energy storage,', \
        np.append (cost_contributions_fuel_power, cost_contributions_fuel_storage)    
        
    # Fixed O&M cost
    
    cost_contributions_fixedOM_power = capacity_power * fixed_OM_cost_power / np.sum(demand)
    cost_contributions_fixedOM_storage = capacity_storage * fixed_OM_cost_storage / np.sum(demand)

    print 'Fixed O&M cost contribution ($/kWh):', power_tech_string, 'energy storage,', \
        np.append (cost_contributions_fixedOM_power, cost_contributions_fixedOM_storage)    
    
    # Variable O&M cost

    cost_contributions_variableOM_power = \
        dispatched_power_discharge_solution_total * variable_OM_cost_power / np.sum(demand)
    cost_contributions_variableOM_storage = \
        (dispatched_storage_discharge_solution_total * variable_OM_cost_storage +
         dispatched_storage_charge_solution_total * variable_OM_cost_storage) / np.sum(demand)

    print 'Variable O&M cost contribution ($/kWh):', power_tech_string, 'energy storage,', \
        np.append (cost_contributions_variableOM_power, cost_contributions_variableOM_storage)

    # -------------------------------------------------------------------------

    # Investment cost

    investment_power = capacity_power * capital_cost_power / 1e9
    investment_storage = capacity_storage * capital_cost_storage / 1e9

    print 'Investment cost (billion $):', power_tech_string, 'energy storage,', \
        np.append (investment_power, investment_storage)      
    
    # -------------------------------------------------------------------------
    
    # Capacity factor
        
    if capacity_power[power_tech_index['natural_gas']] !=0:
        ngcc_cf = (np.sum(dispatched_power[power_tech_index['natural_gas'], :]) / (demand.size * capacity_power[power_tech_index['natural_gas']]))
    else:
        ngcc_cf = 0
        
    if capacity_power[power_tech_index['wind']] !=0:
        wind_cf = np.sum(dispatched_power[power_tech_index['wind'], :]) / (demand.size * capacity_power[power_tech_index['wind']])
    else:
        wind_cf = 0
        
    if capacity_power[power_tech_index['solar']] !=0:
        solar_cf = np.sum(dispatched_power[power_tech_index['solar'], :]) / (demand.size * capacity_power[power_tech_index['solar']])            
    else:
        solar_cf = 0        
        
    if capacity_power[power_tech_index['nuclear']] !=0:
        nuclear_cf = (np.sum(dispatched_power[power_tech_index['nuclear'], :]) / (demand.size * capacity_power[power_tech_index['nuclear']]))        
    else:
        nuclear_cf = 0        
    
    if capacity_storage !=0:
        capacity_factor_storage = dispatched_storage_discharge_solution_total / capacity_storage
    else:
        capacity_factor_storage = 0

    capacity_factor_power = np.array([ngcc_cf, wind_cf, solar_cf, nuclear_cf])
    print 'Capacity factor:', power_tech_string, 'energy storage,', np.append (capacity_factor_power, capacity_factor_storage)
    
    # -----------------------------------------------------------------------------
    
    print "\n------------------------------------------------------------------------"
    print "used_assumptions"
    print "------------------------------------------------------------------------\n"        
    
    print "Input folder:", directory_input
    print "Output folder:", output_folder
    print "Power generation, capital cost ($/kW):",  capital_cost_power
    print "Energy storage, capital cost ($/kWh):",  capital_cost_storage
    print "Capital charge rate (power generation, storage)", capital_charge_rate_power, capital_charge_rate_storage
    print "Power generation, fixed operation cost ($/kW):", fixed_OM_cost_power
    print "Energy storage, fixed operation cost ($/kWh):",  fixed_OM_cost_storage
    print "Power generation, fuel cost ($/kWh):", variable_fuel_cost_power
    print "Power generation, efficiency:", efficiency_power
    print "Power generation, variable O&M cost ($/kWh):", variable_OM_cost_power
    print "Energy storage, variable O&M cost ($/kWh):", variable_OM_cost_storage
    print "Power generation, fixed O&M cost ($/kWh):", fixed_OM_cost_power
    print "Energy storage, fixed O&M cost ($/kWh):", fixed_OM_cost_storage    
    print "Unmet demand cost ($/kWh):", unmet_demand_cost
    print "Energy storage round-trip efficiency:", storage_charging_efficiency ** 2
    print "Energy storage charging duration:", storage_charging_duration
#    print "Curtailment cost ($/kWh):", curtailment_cost
    
    sys.stdout = orig_stdout
    f.close()
    
    # -----------------------------------------------------------------------------
        
    if PRINT_FIGURE == 1:
        funct_graphics(model_inputs, model_results, directory_output)
    
    #%% Data file output       
    if DATA_TYPE == "npz":
        np.savez(output_folder + '/optimization_related',
             model_inputs = model_inputs,
             model_results = model_results)
        
    elif DATA_TYPE == "pkl":
        import pickle
        f = open(output_folder + "/optimization_related.pkl","wb")
        pickle.dump([model_inputs, model_results], f)
        f.close()
    
    #%% Post-processing - Function return variables

    # 99 columns
    # Assumptions (aka, optimization inputs): 37 columns
    #   1    simulation start time (hour)
    #   1    simulation end time (hour)
    #   1    total demand
    #   4    power generation, capital cost
    #   1    storage, capital cost
    #   1    natural gas fuel cost
    #   1    nuclear fuel cost
    #   1    unmet demand variable cost
    #   1    curtailment cost
    #   4    power generation, fixed cost
    #   1    storage, fixed cost
    #   4    power generation, variable cost
    #   1    storage, variable cost
    #   4    power generation, fixed O&M cost
    #   1    storage, fixed O&M cost
    #   4    power generation, variable O&M cost
    #   1    storage, variable O&M cost
    #   1    power generation, capital charge rate
    #   1    storage, capital charge rate
    #   1    NGCC efficiency
    #   1    nuclear efficiency
    #   1    storage efficiency
    
    # Results (aka, optimization results): 61 columns
    #   1    optimal systems cost
    #   4    power generation, cost contributions
    #   1    energy storage, cost contributions
    #   1    unmet demand, cost contributions
    #   1    curtailment, cost contributions
    #   4    power generation, fixed cost contributions
    #   1    energy storage, fixed cost contributions
    #   4    power generation, variable cost contributions
    #   1    energy storage, variable cost contributions    
    #   4    power generation, capital cost contributions
    #   1    energy storage, capital cost contributions
    #   4    power generation, fuel cost contributions
    #   1    energy storage, fuel cost contributions 
    #   4    power generation, fixed O&M cost contributions
    #   1    energy storage, fixed O&M cost contributions
    #   4    power generation, variable O&M cost contributions
    #   1    energy storage, variable O&M cost contributions
    #   4    power generation, investment
    #   1    energy storage, investment
    #   4    power generation, dispatched generation
    #   1    energy storage, discharging flow
    #   1    energy storage, charging flow
    #   1    power generation, curtailment
    #   1    unmet demand
    #   4    power generation, deployed capacity
    #   1    energy storage, deployed capacity    
    #   4    power generation, capacity factor
    #   1    energy storage, capacity factor （equivalent full-discharge cycle)

    output_table_row1 = np.concatenate((
            # assumptions            
            np.array([simulation_start], float),
            np.array([simulation_end], float),
            np.array([np.sum(demand)], float),
            capital_cost_power,
            np.array([capital_cost_storage], float),
            np.array([ng_fuel_cost], float),
            np.array([nuclear_fuel_cost], float),
            np.array([unmet_demand_cost], float),
            np.array([curtailment_cost], float),
            ), axis = 0)
    
    output_table_row2 = np.concatenate((                
            fixed_cost_power,
            np.array([fixed_cost_storage], float),
            variable_cost_power,
            np.array([variable_cost_storage], float),
            fixed_OM_cost_power,
            np.array([fixed_OM_cost_storage], float), 
            variable_OM_cost_power,
            np.array([variable_OM_cost_storage], float),
            np.array([capital_charge_rate_power], float),
            np.array([capital_charge_rate_storage], float),
            np.array([efficiency_power[power_tech_index['natural_gas']]], float),
            np.array([efficiency_power[power_tech_index['nuclear']]], float),
            np.array([storage_charging_efficiency], float),
            np.array([storage_charging_duration], float),
            ), axis = 0)

    # print >>sys.stdout, output_table_row1
    # print >>sys.stdout, output_table_row1.shape
    
    # print >>sys.stdout, output_table_row2
    # print >>sys.stdout, output_table_row2.shape

#    print >>sys.stdout, "line 472"
#    print >>sys.stdout, optimum / np.sum(demand)
#    print >>sys.stdout, cost_contributions_power
#    print >>sys.stdout, cost_contributions_storage
#    print >>sys.stdout, cost_contributions_unmet_demand
#    print >>sys.stdout, cost_contributions_curtailment
    
    output_table_row3 = np.concatenate((
            # results           
            np.array([optimum / np.sum(demand)], float),
            cost_contributions_power,
            np.array([cost_contributions_storage], float),
            np.array([cost_contributions_unmet_demand], float),
            np.array([cost_contributions_curtailment], float),            
            ), axis = 0)
    
#    print >>sys.stdout, output_table_row3
#    print >>sys.stdout, output_table_row3.shape        
        
    output_table_row4 = np.concatenate((        
            cost_contributions_fixed_cost_power,
            np.array([cost_contributions_fixed_cost_storage], float),
            cost_contributions_variable_cost_power,
            np.array([cost_contributions_variable_cost_storage], float),
            ), axis = 0)
    
    # print >>sys.stdout, output_table_row4.shape
            
    output_table_row5 = np.concatenate((
            cost_contributions_capital_power,
            np.array([cost_contributions_capital_storage], float),
            cost_contributions_fuel_power,
            np.array([cost_contributions_fuel_storage], float),               
            cost_contributions_fixedOM_power,
            np.array([cost_contributions_fixedOM_storage], float),
            cost_contributions_variableOM_power,
            np.array([cost_contributions_variableOM_storage], float),
            ), axis = 0)

    output_table_row6 = np.concatenate((            
            investment_power,
            np.array([investment_storage], float),
            dispatched_power_discharge_solution_total / np.sum(demand),
            np.array([dispatched_storage_discharge_solution_total / np.sum(demand)], float),
            np.array([-dispatched_storage_charge_solution_total / np.sum(demand)], float),
            np.array([-curtailment_solution_total / np.sum(demand)], float),
            np.array([unmet_demand_solution_total / np.sum(demand)], float),
            capacity_power,
            np.array([capacity_storage], float),
            capacity_factor_power,
            np.array([capacity_factor_storage], float),
            ), axis = 0)
    
    output_table_row = np.concatenate((
            output_table_row1, 
            output_table_row2, 
            output_table_row3, 
            output_table_row4,
            output_table_row5,
            output_table_row6,
            ), axis=0)
    
    return output_table_row