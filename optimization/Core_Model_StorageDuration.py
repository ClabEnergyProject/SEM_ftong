#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""

File name: Core_Model.py

Idealized energy system models

Spatial scope: U.S.
Data: Matt Shaner's paper with reanalysis data and U.S. demand.

Technology:
    Generation: natural gas, wind, solar, nuclear
    Energy storage: one generic (a pre-determined round-trip efficiency)
    Curtailment: No
    Unmet demand: Yes
    
Speical consideration
    Inequality constraints for RE generation.
    No curtailment variable.    
    
Optimization:
    Linear programming (LP)
    Energy balance constraints for the grid and the energy storage facility.

@author: Fan
Time
    Dec 1, 4-8, 11, 19, 22
    Jan 2-4, 24-27
    
"""

# -----------------------------------------------------------------------------

import cvxpy as cvx
import numpy as np
import time

# Core function
#   Linear programming
#   Output postprocessing

def core_model (model_inputs):
    
    simulation_start = time.time()

    print "\nJust to be clear, you are calling a core model formulation that calculates curtailment after optimization\n"

    # -------------------------------------------------------------------------    
    
    #%% Get the input data
    
    # Core assumptions
    power_tech_index = model_inputs['power_tech_index']
    fixed_cost_power = model_inputs['fixed_cost_power']
    fixed_cost_storage = model_inputs['fixed_cost_storage']    
    variable_cost_power = model_inputs['variable_cost_power']
    variable_cost_storage = model_inputs['variable_cost_storage']    
    unmet_demand_cost = model_inputs['unmet_demand_cost']
    # curtailment_cost = model_inputs['curtailment_cost']
    storage_charging_efficiency = model_inputs['storage_charging_efficiency']
    storage_charging_duration = model_inputs['storage_charging_duration']

    # Input data
    demand = model_inputs['demand']        
    wind_capacity_factor = model_inputs['wind_capacity_factor']    
    solar_capacity_factor = model_inputs['solar_capacity_factor']

    # Supportive variables (used in post-processing)
#    capital_cost_power = model_inputs['capital_cost_power']
#    capital_cost_storage = model_inputs['capital_cost_storage']
#    annualized_capital_cost_power = model_inputs['annualized_capital_cost_power']
#    annualized_capital_cost_storage = model_inputs['annualized_capital_cost_storage']
#    variable_fuel_cost_power = model_inputs['variable_fuel_cost_power']
#    variable_fuel_cost_storage = model_inputs['variable_fuel_cost_storage']
#    ng_fuel_cost = model_inputs['ng_fuel_cost']       
    
    # -------------------------------------------------------------------------

    simulation_periods = demand.size
    
    # -------------------------------------------------------------------------
    
    #%% Construct the Problem
    
    # -------------------------------------------------------------------------
    ## Define Variables
    
    # Number of generation technologies = power_tech_index.size
    # Number of time steps/units in a given time duration = demand.size
    #       demand.size returns an integer value
    
    # capacity_power = Installed power capacities for all generation technologies = [kW]
    # dispatched_power = Power generation at each time step for each generator = [kWh]
    
    # dispatched_curtailment = Curtailed renewable energy generation at each time step = [kWh]
    #   This is more like a dummy variable
    
    # capacity_storage = Deployed size of energy storage = [kWh]
    # storage_energy_soc = State of charge for the energy storage = [kWh]
    # dispatched_storage_charge = Charging energy flow for energy storage (grid -> storage) = [kWh]
    # dispatched_storage_discharge = Discharging energy flow for energy storage (grid <- storage) = [kWh]
    
    # unmet_demand = unmet demand/load = [kWh]
    
    capacity_power = cvx.Variable(fixed_cost_power.size)
    dispatched_power = cvx.Variable(fixed_cost_power.size, simulation_periods)
    #dispatched_curtailment = cvx.Variable(simulation_periods)
    
    capacity_storage = cvx.Variable(1)
    storage_energy_soc = cvx.Variable(simulation_periods + 1)
    dispatched_storage_charge = cvx.Variable(simulation_periods)
    dispatched_storage_discharge = cvx.Variable(simulation_periods)
    
    unmet_demand = cvx.Variable(simulation_periods)
    
    # -----------------------------------------------------------------------------
    ## Define Contraints
    
    # (1) For all time steps, supply must equal demand.
    # (2-3) Renewable energy generation (wind and solar) is prescribed by "real-time" capacity factors.
    # (4) Natural gas power generation is less than or equal to installed capacity.
    # (5) Nuclear generation constraint (must-run & fixed)
    # (6-7) Constrain the variable space for power generations.
    # (8-11) Energy storage constraints.
    # (12) Unmet demand.
    
    constraints = [
            cvx.sum_entries(dispatched_power, axis=0).T + dispatched_storage_discharge + unmet_demand == demand + dispatched_storage_charge,
            dispatched_power[power_tech_index['solar'],:].T <= solar_capacity_factor * capacity_power[power_tech_index['solar']], 
            dispatched_power[power_tech_index['wind'],:].T <= wind_capacity_factor * capacity_power[power_tech_index['wind']],
            dispatched_power[power_tech_index['natural_gas'],:] <= capacity_power[power_tech_index['natural_gas']], 
            dispatched_power[power_tech_index['nuclear'],:].T <= capacity_power[power_tech_index['nuclear']],
            dispatched_power >= 0,
            capacity_power >= 0,
            storage_energy_soc <= capacity_storage,
            storage_energy_soc >= 0,
            dispatched_storage_discharge <= capacity_storage / storage_charging_duration,
            dispatched_storage_charge <= capacity_storage / storage_charging_duration,
            dispatched_storage_charge >= 0,
            dispatched_storage_discharge >= 0,
            unmet_demand >= 0,            
            ]
    
    # Energy storage constraints for all time steps
    
    for i in xrange(simulation_periods):
        constraints += [
                storage_energy_soc[i+1] == storage_energy_soc[i] + storage_charging_efficiency * \
                dispatched_storage_charge[i] - 1/storage_charging_efficiency * dispatched_storage_discharge[i]
                ]
    
    # The last one constraint - stability conditions
    
    constraints += [
                storage_energy_soc[0] == storage_energy_soc[simulation_periods]
                ]
    
    # -----------------------------------------------------------------------------
    ## Define Objective Function
    
    # Objective function = Total system cost (NPV, annualized for one year) 
    #   = fixed cost + variable cost
    #   = capital cost + fuel cost + fixed O&M cost + variable O&M cost
    
    fcn2min = \
        cvx.sum_entries(capacity_power.T * fixed_cost_power
        + cvx.sum_entries(dispatched_power.T * variable_cost_power)
        + cvx.sum_entries(dispatched_storage_discharge.T * variable_cost_storage)
        + cvx.sum_entries(dispatched_storage_charge.T * variable_cost_storage)
        + cvx.sum_entries(capacity_storage.T * fixed_cost_storage)
        + cvx.sum_entries(unmet_demand.T * unmet_demand_cost)
        + cvx.sum_entries(
                (capacity_power[power_tech_index['nuclear']] - dispatched_power[power_tech_index['nuclear'],:].T) 
                * variable_cost_power[power_tech_index['nuclear']])
        + cvx.sum_entries(
                (wind_capacity_factor * capacity_power[power_tech_index['wind']] - dispatched_power[power_tech_index['wind'],:].T) 
                * variable_cost_power[power_tech_index['wind']])
        +cvx.sum_entries(
                (solar_capacity_factor * capacity_power[power_tech_index['solar']] - dispatched_power[power_tech_index['solar'],:].T) 
                * variable_cost_power[power_tech_index['solar']]))
    obj = cvx.Minimize(fcn2min)
    
    # -------------------------------------------------------------------------
    
    #%% Problem solving
    
    # print cvx.installed_solvers()
    # print >>orig_stdout, cvx.installed_solvers()
    
    # Form and Solve the Problem
    prob = cvx.Problem(obj, constraints)
    prob.solve(solver = 'GUROBI', BarConvTol = 1e-11)
    
    simulation_end_timestamp = time.time()        
    
    # -------------------------------------------------------------------------
    
    #%% Results processing
    
    # Conversion from MATRIX to ARRAY
    
    dispatched_power_solution = np.asarray(dispatched_power.value)    
    unmet_demand_solution = np.asarray(unmet_demand.value)

    # These two methods are equivalent    
    # capacity_power_solution = np.squeeze(np.asarray(capacity_power.value))
    capacity_power_solution = capacity_power.value.A1
      
    dispatched_storage_discharge_solution = np.asarray(dispatched_storage_discharge.value)
    dispatched_storage_charge_solution = np.asarray(dispatched_storage_charge.value) 
    
    capacity_storage_solution = capacity_storage.value
     
    storage_energy_soc = storage_energy_soc[0:-1]
    storage_energy_soc_solution = np.asarray(storage_energy_soc.value)    
        
    # -------------------------------------------------------------------------
    
    # Calculate curtailment
    
    curtailment_solar_solution = (
            solar_capacity_factor * capacity_power_solution[power_tech_index['solar']] - 
            dispatched_power_solution[power_tech_index['solar'],:])
    
    curtailment_wind_solution = (
            wind_capacity_factor * capacity_power_solution[power_tech_index['wind']] - 
            dispatched_power_solution[power_tech_index['wind'],:])
    
    curtailment_nuclear_solution =  (
            capacity_power.value[power_tech_index['nuclear']] - 
            dispatched_power.value[power_tech_index['nuclear'],:])
    
    dispatched_curtailment_solution = (
            curtailment_solar_solution + curtailment_wind_solution + curtailment_nuclear_solution)
    
    # -----------------------------------------------------------------------------
    
    # All the generated outputs from the optimization
    # 7 core variables, and 4+2+2 supporting informative variables.
    
    results = {
            # Core optimization results (decision variables)            
            'dispatched_power':                 dispatched_power_solution,
            'capacity_power':                   capacity_power_solution,
            'dispatched_storage_discharge':     dispatched_storage_discharge_solution,
            'dispatched_storage_charge':        dispatched_storage_charge_solution,
            'unmet_demand':                     unmet_demand_solution,
            'capacity_storage':                 capacity_storage_solution,
            'storage_energy_soc':               storage_energy_soc_solution,
            
            # Curtailment results
            'dispatched_curtailment':           dispatched_curtailment_solution,            
            'curtailment_solar':                curtailment_solar_solution,
            'curtailment_wind':                 curtailment_wind_solution,
            'curtailment_nuclear':              curtailment_nuclear_solution,
            
            # Optimization status
            'solution_status':                  prob.status,
            'optimum':                          prob.value,
            
            # Supporting information (used in post-processing)
            'run_time':                         (simulation_end_timestamp - simulation_start),
            'constraints_count':                len(constraints),
            }
    
    return results