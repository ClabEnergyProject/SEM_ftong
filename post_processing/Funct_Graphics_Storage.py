# -*- coding: utf-8 -*-
"""
Func_Graphics_Storage.py

Function: generate figures from optimizaiton results

Functions defined:
    func_plotting_storage_static_1scenario()
    func_plotting_storage_static_1scenario_1()
    func_graphic_storage_results_1scenario()  -- directly callable

History
    Jun 10, 2018 initiated and finished
    Jun 18, 2018 checked and commented
    Jun 19, 2018 renamed some functions
    Jun 21, 2018 updated the code for loading the optimization results from files
    Jun 23, 2018 updated comments
        updated func_plotting_storage_static_1scenario()
    June 23-24, 2018 updated texts and labels on figures

@author: Fan
"""

from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from Supporting_Functions import func_lines_plot
from Supporting_Functions import func_PMF_plot
from Supporting_Functions import func_moving_window
from Supporting_Functions import func_change_in_period
from Supporting_Functions import func_load_optimization_results
from matplotlib.backends.backend_pdf import PdfPages

#%%
# -----------------------------------------------------------------------------
# func_plotting_storage_static_1scenario()
#
# Function
#   This function produces figures for energy storage based on optimization results
#   (state of charge, dischage, charge, capacity, demand) from a single run.
#
# Input
#   input_data, a DICT variable, which has the following keys:
#       capacity_storage [1]
#       storage_energy_soc [optimization steps]
#       dispatched_storage_discharge [optimization steps]
#       dispatched_storage_charge [optimization steps]
#       demand [optimization steps]
#       directory_output <string> full directory
#       graphics_file_name <string> file name, without the file extention
#       SAVE_FIGURES_TO_PDF [1] whether or not save to a file
#
# Output
#   7 figures, either shown in the Console or a PDF file
#
# Usage
#   called upon in the function func_plotting_storage_results_1scenario()
#
# History
#   June 10, 2018 drafted the function
#   June 22-23, 2018 added parallel axes and fixed some figure-related issues
#   June 23-24, 2018 updated texts and labels on figures
#
# @ Fan Tong
# -----------------------------------------------------------------------------

def func_plotting_storage_static_1scenario(input_data):
    
    # -------------------------------------------------------------------------
    
    # Load the input data
    
    storage_energy_soc = input_data["storage_energy_soc"]
    capacity_storage = input_data["capacity_storage"]
    dispatched_storage_discharge = input_data["dispatched_storage_discharge"]
    dispatched_storage_charge = input_data["dispatched_storage_charge"]
    demand = input_data["demand"]
    
    directory_output = input_data["directory_output"]
    graphics_file_name = input_data["graphics_file_name"]
    SAVE_FIGURES_TO_PDF = input_data["SAVE_FIGURES_TO_PDF"]    
    
    # -------------------------------------------------------------------------
    
    if SAVE_FIGURES_TO_PDF:
        if not os.path.exists(directory_output):
            os.makedirs(directory_output)
                        
        pdf_pages = PdfPages(
            directory_output + graphics_file_name + '.pdf')
            
    # -------------------------------------------------------------------------
    # Plotting style
    
    plt.style.use('default')
    # plt.style.use('bmh')
    # plt.style.use('fivethirtyeight')
    # plt.style.use('seaborn-white')
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] =  'Helvetica' #'Palatino' # 'Ubuntu'
    plt.rcParams['font.monospace'] = 'Helvetica Mono' #'Palatino Mono' # 'Ubuntu'
    plt.rcParams['font.size'] = 16
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 16
    plt.rcParams['ytick.labelsize'] = 16
    plt.rcParams['legend.fontsize'] = 14
    plt.rcParams['figure.titlesize'] = 16
    plt.rcParams['lines.linewidth'] = 2.0
    plt.rcParams['grid.color'] = 'k'
    plt.rcParams['grid.linestyle'] = ':'
    plt.rcParams['grid.linewidth'] = 0.5
    plt.rcParams['xtick.major.width'] = 2
    plt.rcParams['xtick.major.size'] = 6
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.major.width'] = 2
    plt.rcParams['ytick.major.size'] = 6
    plt.rcParams['ytick.direction'] = 'in'
    
    # -------------------------------------------------------------------------
    
    # Historgram
    
    # Prepare data for later use
    
    storage_energy_soc_normalized = storage_energy_soc / capacity_storage
    
    storage_discharge_normDemand = np.reshape(dispatched_storage_discharge, -1) / demand
    storage_discharge_normDemand_nz = [e for i, e in enumerate(storage_discharge_normDemand) if e != 0]
    
    storage_discharge_normCapacity = np.reshape(dispatched_storage_discharge, -1) / capacity_storage
    storage_discharge_normCapacity_nz = [e for i, e in enumerate(storage_discharge_normCapacity) if e != 0]
    
    # np.savez('temp', dispatched_storage_discharge, capacity_storage, storage_discharge_normCapacity)
    
    # -------------------------------------------------------------------------
    
    num_bins = 500
    figsize_oneplot = (8,6)
    figsize_subplot= (8,8)
    
    # -------------------------------------------------------------------------
    
    # Figure 1 State of charge
    
    figure1 = plt.figure(figsize=figsize_oneplot)
    ax1 = figure1.add_subplot(111)
    
    inputs1 = {
            "x_data":       storage_energy_soc_normalized,
            "ax":           ax1,
            "x_label":      "Storage state of charge",
            "y_label":      "Probability",
            #"title":        "Histogram on storage's state of charge",
            "num_bins":     num_bins,
            "zero_one_range":   1,
            }
    
    func_PMF_plot(inputs1)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure1, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    #
    # Figure 2 Discharge energy (hourly-averge demand) - full
    
    # figure2, ax2 = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True, figsize=(8, 8))
    
    figure2, ax2 = plt.subplots(nrows=2, ncols=2, figsize=figsize_subplot)
    
    inputs2a = {
            "x_data":       storage_discharge_normDemand,
            "ax":           ax2[0,0],
            "num_bins":     num_bins,
            }
    
    ax2[0,0] = func_PMF_plot(inputs2a)
    
    start, end = ax2[0,0].get_xlim()
    ax2[0,0].xaxis.set_ticks(np.arange(start, end, (end-start)/2))
    
#    ax2[0,0].tick_params(
#        axis='x',          # changes apply to the x-axis
#        which='both',      # both major and minor ticks are affected
#        bottom=False,      # ticks along the bottom edge are off
#        top=False,         # ticks along the top edge are off
#        labelbottom=False) # labels along the bottom edge are off
    
    # -------------------------------------------------------------------------
    
    # Discharge energy (hourly-averge demand) - nonzero portion
    
    inputs2b = {
            "x_data":       storage_discharge_normDemand_nz,
            "ax":           ax2[0,1],
            "num_bins":     num_bins,
            }
    
    ax2[0,1] = func_PMF_plot(inputs2b)
    
    start, end = ax2[0,1].get_xlim()
    ax2[0,1].xaxis.set_ticks(np.arange(start, end, (end-start)/2))
    
#    ax2[0,1].tick_params(
#        axis='x',          # changes apply to the x-axis
#        which='both',      # both major and minor ticks are affected
#        bottom=False,      # ticks along the bottom edge are off
#        top=False,         # ticks along the top edge are off
#        labelbottom=False) # labels along the bottom edge are off
    
    # -------------------------------------------------------------------------
    
    # Discharge energy (fraction of storage capacity) - full
    
    inputs2c = {
            "x_data":       storage_discharge_normCapacity,
            "ax":           ax2[1,0],
            "num_bins":     num_bins,
            "zero_one_range":   1,            
            }
    
    ax2[1,0] = func_PMF_plot(inputs2c)
    
    start, end = ax2[1,0].get_xlim()
    ax2[1,0].xaxis.set_ticks(np.arange(start, end, (end-start)/2))
    
    # -------------------------------------------------------------------------
    
    # Discharge energy (fraction of storage capacity) - nonzero portion
    
    inputs2d = {
            "x_data":       storage_discharge_normCapacity_nz,
            "ax":           ax2[1,1],
            "num_bins":     num_bins,
            "zero_one_range":   1,
            }
    
    ax2[1,1] = func_PMF_plot(inputs2d)
    
    start, end = ax2[1,1].get_xlim()
    ax2[1,1].xaxis.set_ticks(np.arange(start, end, (end-start)/2))
    
    #left  = 0.125  # the left side of the subplots of the figure
    #right = 0.9    # the right side of the subplots of the figure
    #bottom = 0.1   # the bottom of the subplots of the figure
    #top = 0.9      # the top of the subplots of the figure
    #wspace = 0.2   # the amount of width reserved for blank space between subplots
    #hspace = 0.2   # the amount of height reserved for white space between subplots
    figure2.subplots_adjust(left=0.15, bottom=0.10, right=None, top=None, wspace=0.2, hspace=0.2)
    
    figure2.text(
            0.5, 0.04, 
            'Storage discharge energy (normalized)', 
            ha='center',
            fontsize=16,
            fontname='Helvetica Mono',
            fontweight='bold')
    
    figure2.text(
            0.04, 0.5, 
            'Probability', 
            va='center',
            rotation='vertical',
            fontsize=16,
            fontname='Helvetica Mono',
            fontweight='bold')
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure2, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    #    
    # Figure 3 Time series plot of discharge energy
    
    optimization_steps = demand.size
    time_series = np.arange(0, optimization_steps)
    
    mix_matrix = np.column_stack(
                (dispatched_storage_charge, 
                dispatched_storage_discharge))
    
    figure3 = plt.figure(figsize=figsize_oneplot)
    ax3 = figure3.add_subplot(111)
    
    # title_text = "Storage discharge and charge"
    legend_list = ['Storage charge', 'Storage discharge']
    
    inputs3 = {
            "x_data":        time_series, 
            "y2_data":       mix_matrix/np.average(demand),
            "y_data":        mix_matrix/1e6,
            "ax":            ax3,
            "x_label":      'Time (hour in the year)',
            "y2_label":     'hourly-average demand',
            "y_label":      '1e6 kWh',
            #"title":        title_text,
            "legend":       legend_list,
            "line_width":    1,
            'grid_option':   0,
            }        
            
    func_lines_plot(inputs3)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure3, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    # Figure 4 
    # Time series of discharging/charging - integral in a moving window
    # Calculate, for a rolling basis, how much is cumulative discharge over a certain time period
    
    figure4, ax4 = plt.subplots(nrows=2, ncols=1, figsize=figsize_subplot)
    time_series = np.arange(0, optimization_steps)
    
    # -----------------------------------
    
    # Figure (a) # Time series of discharging - integral in a moving window
    
    dispatched_storage_discharge_MA24 = (
            func_moving_window(dispatched_storage_discharge, 24, 'sum'))
    dispatched_storage_discharge_MA168 = (
            func_moving_window(dispatched_storage_discharge, 24*7, 'sum'))
    dispatched_storage_discharge_MA672 = (
            func_moving_window(dispatched_storage_discharge, 24*28, 'sum'))
    
    mix_matrix = np.column_stack(
                (dispatched_storage_discharge,
                 dispatched_storage_discharge_MA24, 
                dispatched_storage_discharge_MA168,
                dispatched_storage_discharge_MA672))
    
    legend_list = ['1 hour', '1 day', '1 week', '4 weeks']
    
    title_text = 'Storage cumulative discharge'
    
    inputs4a = {
            "x_data":       time_series, 
            "y2_data":      mix_matrix / np.average(demand),
            "y_data":       mix_matrix / 1e9,
            "ax":           ax4[0],
            #"x_label":      'Time (hour in the year)',
            "y2_label":     'hourly-average demand',
            "y_label":      '1e9 kWh',
            "legend":        legend_list,
            "line_width":    1,
            'grid_option':   0,
            'title':         title_text,
            }        
            
    ax4[0] = func_lines_plot(inputs4a)
    
    # -----------------------------------   
    
    # Figure (b) Time series of charging - integral in a moving window
    
    # time_series = np.arange(0, optimization_steps)
    
    dispatched_storage_charge_MA24 = (
            func_moving_window(dispatched_storage_charge, 24, 'sum'))
    dispatched_storage_charge_MA168 = (
            func_moving_window(dispatched_storage_charge, 24*7, 'sum'))
    dispatched_storage_charge_MA672 = (
            func_moving_window(dispatched_storage_charge, 24*28, 'sum'))
    
    mix_matrix = np.column_stack(
                (dispatched_storage_charge,
                 dispatched_storage_charge_MA24, 
                dispatched_storage_charge_MA168,
                dispatched_storage_charge_MA672))
    
    legend_list = ['1 hour', '1 day', '1 week', '4 weeks']
    
    title_text = 'Storage cumulative charge'
    
    inputs4b = {
            "x_data":       time_series, 
            "y2_data":       mix_matrix / np.average(demand),
            "y_data":       mix_matrix / 1e9,
            "ax":           ax4[1],
            "x_label":      'Time (hour in the year)',
            "y2_label":     'hourly-average demand',
            "y_label":      '1e9 kWh',
            "legend":       legend_list,
            "line_width":    1,
            'grid_option':   0,
            'title':         title_text,
            }           
    
    ax4[1] = func_lines_plot(inputs4b)

    # -----------------------------------
    
    #left  = 0.125  # the left side of the subplots of the figure
    #right = 0.9    # the right side of the subplots of the figure
    #bottom = 0.1   # the bottom of the subplots of the figure
    #top = 0.9      # the top of the subplots of the figure
    #wspace = 0.2   # the amount of width reserved for blank space between subplots
    #hspace = 0.2   # the amount of height reserved for white space between subplots
    figure4.subplots_adjust(left=None, bottom=None, right=None, top=None, hspace=0.2)    
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure4, bbox_inches='tight')
        plt.close()
        
    # -------------------------------------------------------------------------
    
    # Figure 5 Time series of state of charge - time series
    
    time_series = np.arange(0, optimization_steps)
    
    title_text = 'Storage state of charge'
    
    figure5 = plt.figure(figsize=figsize_oneplot)
    ax5 = figure5.add_subplot(111)
    
    inputs5 = {
            "x_data":       time_series, 
            "y_data":       storage_energy_soc_normalized,
            "y2_data":       storage_energy_soc / np.average(demand),
            "ax":           ax5,
            "x_label":      'Time (hour in the year)',
            "y_label":      'fraction of storage capacity',
            "y2_label":     'hourly-average demand',
            "title":        title_text,
            "line_width":    1,
            'grid_option':   0,
            }
    
    func_lines_plot(inputs5)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure5, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 6 Change in state of charge over a moving window
    
    # This is a very messy figure!
    
    # -----------------------------------
    
    time_series = np.arange(0, optimization_steps)
    
    storage_energy_soc_normalized = np.reshape(storage_energy_soc_normalized, -1)
    
    storage_energy_soc_normalized_diff_hour = (
        func_change_in_period(storage_energy_soc_normalized, 1))
    storage_energy_soc_normalized_diff_day = (
        func_change_in_period(storage_energy_soc_normalized, 24))
    storage_energy_soc_normalized_diff_week = (
        func_change_in_period(storage_energy_soc_normalized, 24*7))
    storage_energy_soc_normalized_diff_month = (
        func_change_in_period(storage_energy_soc_normalized, 24*28))
    
    mix_matrix = np.column_stack(
                (storage_energy_soc_normalized_diff_hour,
                 storage_energy_soc_normalized_diff_day, 
                storage_energy_soc_normalized_diff_week,
                storage_energy_soc_normalized_diff_month))
    
    legend_list = ['1 hour', '1 day', '1 week', '4 weeks']
    
    title_text = 'Change in storage\'s state of charge'
    
    # -----------------------------------
    
    figure6 = plt.figure(figsize=figsize_oneplot)
    ax6 = figure6.add_subplot(111)    
    
    inputs6 = {
            "x_data":       time_series, 
            "y_data":       mix_matrix,
            "y2_data":      mix_matrix * capacity_storage / np.average(demand),
            "ax":           ax6,
            "x_label":      'Time (hour in the year)',
            "y_label":      'fraction of storage capacity',
            "y2_label":     'hourly-average demand',
            "title":        title_text,
            "legend":       legend_list,
            "line_width":    1,
            'grid_option':   0,
            }           
    
    func_lines_plot(inputs6)
    
    ax6.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure6, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 7 Sorted time series of discharging
    
    time_series = np.arange(0, demand.size)
    
    title_text = 'Storage discharge (sorted by magnitude)'
    
    figure7 = plt.figure(figsize=figsize_oneplot)
    ax7 = figure7.add_subplot(111)
    
    inputs7 = {
            "x_data":       time_series, 
            "y_data":       -np.sort(-dispatched_storage_discharge, axis=0)/1e6,
            "y2_data":      -np.sort(-dispatched_storage_discharge, axis=0)/np.average(demand),
            "ax":           ax7,
            "x_label":      'Time (hour in the year)',
            "y_label":      '1e6 kWh',
            "y2_label":     'hourly-average demand',
            "title":         title_text,
            "line_width":    1,
            'grid_option':   0,
            }
    
    func_lines_plot(inputs7)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure7, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 7b Sorted time series of discharging
    
    time_series = np.arange(0, demand.size)
    
    title_text = 'Storage charge (sorted by magnitude)'
    
    figure7b = plt.figure(figsize=figsize_oneplot)
    ax7b = figure7b.add_subplot(111)
    
    inputs7b = {
            "x_data":        time_series,
            "y_data":        -np.sort(-dispatched_storage_charge, axis=0)/1e6,
            "y2_data":       -np.sort(-dispatched_storage_charge, axis=0)/np.average(demand),
            "ax":            ax7b,
            "x_label":       'Time (hour in the year)',
            "y_label":       '1e6 kWh',
            "y2_label":      'hourly-average demand',
            "title":         title_text,
            "line_width":    1,
            'grid_option':   0,
            }
    
    func_lines_plot(inputs7b)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure7b, bbox_inches='tight')
        plt.close()
        
    # -------------------------------------------------------------------------
    # File closure
        
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.close()

#%%
# -----------------------------------------------------------------------------
# func_plotting_storage_static_1scenario_1
#
# Goal
#   This function produces figures for energy storage based on optimization results
#   (state of charge, dischage, charge, capacity, demand) from a single run.
#
# Input
#   input_data, a DICT variable, which has the following keys:
#       capacity_storage [1]
#       storage_energy_soc [optimization steps]
#       dispatched_storage_discharge [optimization steps]
#       dispatched_storage_charge [optimization steps]
#       demand [optimization steps]
#       directory_output <string> full directory
#       graphics_file_name <string> file name, without the file extention
#       SAVE_FIGURES_TO_PDF [1] whether or not save to a file
# Output
#   12 figures, either shown in the Console or a PDF file
#
# Additional note
#   The contents shown in the produced figures are the same as those produced by
#       func_graphic_storage_static_1scenario(). The only difference between the
#       two functions are that this function produces each figure in a page while
#       the other function uses subplots to combine similar figures.
#
# Usage
#   called upon in the function func_plotting_storage_results_1scenario()
#        
# History
#   June 10, 2018 drafted the function
#   June 23-24, 2018 updated texts and labels on figures
#       added parallel axes for some figures, reducing the total # of figures
#           from 15 to 12        
#
# @ Fan Tong        
# -----------------------------------------------------------------------------

def func_plotting_storage_static_1scenario_1(input_data):
    
    # -------------------------------------------------------------------------
    
    # load the input data
    
    storage_energy_soc = input_data["storage_energy_soc"]
    capacity_storage = input_data["capacity_storage"]
    dispatched_storage_discharge = input_data["dispatched_storage_discharge"]
    dispatched_storage_charge = input_data["dispatched_storage_charge"]
    demand = input_data["demand"]
    
    directory_output = input_data["directory_output"]
    graphics_file_name = input_data["graphics_file_name"]
    SAVE_FIGURES_TO_PDF = input_data["SAVE_FIGURES_TO_PDF"]
    
    # -------------------------------------------------------------------------
    
    if SAVE_FIGURES_TO_PDF:
        if not os.path.exists(directory_output):
            os.makedirs(directory_output)
                        
        pdf_pages = PdfPages(
            directory_output + graphics_file_name + '.pdf')
    
    # -------------------------------------------------------------------------
    
    # Plotting style
    
    plt.style.use('default')
    # plt.style.use('bmh')
    # plt.style.use('fivethirtyeight')
    # plt.style.use('seaborn-white')
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] =  'Helvetica ' #'Palatino' # 'Ubuntu'
    plt.rcParams['font.monospace'] = 'Helvetica Mono' #'Palatino Mono' # 'Ubuntu'
    plt.rcParams['font.size'] = 16
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 16
    plt.rcParams['ytick.labelsize'] = 16
    plt.rcParams['legend.fontsize'] = 14
    plt.rcParams['figure.titlesize'] = 16
    plt.rcParams['lines.linewidth'] = 2.0
    plt.rcParams['grid.color'] = 'k'
    plt.rcParams['grid.linestyle'] = ':'
    plt.rcParams['grid.linewidth'] = 0.5
    plt.rcParams['xtick.major.width'] = 2
    plt.rcParams['xtick.major.size'] = 6
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.major.width'] = 2
    plt.rcParams['ytick.major.size'] = 6
    plt.rcParams['ytick.direction'] = 'in'
    
    # -------------------------------------------------------------------------
    
    # Historgram
    
    # Prepare data for later use
    
    storage_energy_soc_normalized = storage_energy_soc / capacity_storage
    
    storage_discharge_normDemand = np.reshape(dispatched_storage_discharge, -1) / demand
    storage_discharge_normDemand_nz = [e for i, e in enumerate(storage_discharge_normDemand) if e != 0]
    
    # storage_discharge_normDemandAve = np.reshape(dispatched_storage_discharge, -1) / np.average(demand)
    
    storage_discharge_normCapacity = np.reshape(dispatched_storage_discharge, -1) / capacity_storage
    storage_discharge_normCapacity_nz = [e for i, e in enumerate(storage_discharge_normCapacity) if e != 0]
    
    # -------------------------------------------------------------------------
    
    # Figure 1 State of charge
    
    num_bins = 500
    fig_size = (8, 6)
    
    figure1 = plt.figure(figsize = fig_size)
    ax1 = figure1.add_subplot(111)
    
    inputs1 = {
            "x_data":       storage_discharge_normCapacity,
            "ax":           ax1,
            "x_label":      "Storage state of charge",
            "y_label":      "Probability",
            # "title":        "Histogram on storage's state of charge",
            "num_bins":     num_bins,
            "zero_one_range":   1,
            }
    
    func_PMF_plot(inputs1)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure1, bbox_inches='tight')
        plt.close()
        
    # -------------------------------------------------------------------------
    
    # Figure 2 Discharge energy (hourly-averge demand) - full
    
    figure2 = plt.figure(figsize = fig_size)
    ax2 = figure2.add_subplot(111)
    
    inputs2 = {
            "x_data":       storage_discharge_normDemand,
            "ax":           ax2,
            "x_label":      "Storage discharge energy (hourly-averge demand)",
            "y_label":      "Probability",
            # "title":        "Histogram on storage's discharge energy",
            "num_bins":     num_bins,
            }
    
    func_PMF_plot(inputs2)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure2, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 3 Discharge energy (hourly-averge demand) - nonzero portion
    
    figure3 = plt.figure(figsize = fig_size)
    ax3 = figure3.add_subplot(111)
    
    inputs3 = {
            "x_data":       storage_discharge_normDemand_nz,
            "ax":           ax3,
            "x_label":      "Storage discharge energy (hourly-averge demand)",
            "y_label":      "Probability",
            # "title":        "Histogram on storage's nonzero discharge energy",
            "num_bins":     num_bins,
            }
    
    func_PMF_plot(inputs3)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure3, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 4 Discharge energy (fraction of storage capacity) - full
    
    figure4 = plt.figure(figsize = fig_size)
    ax4 = figure4.add_subplot(111)
    
    inputs4 = {
            "x_data":       storage_discharge_normCapacity,
            "ax":           ax4,
            "x_label":      "Storage discharge energy(fraction of storage capacity)",
            "y_label":      "Probability",
            # "title":        "Histogram on storage's discharge energy",
            "num_bins":     num_bins,
            "zero_one_range":   1,
            }
    
    func_PMF_plot(inputs4)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure4, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 5 Discharge energy (fraction of storage capacity) - nonzero portion
    
    figure5 = plt.figure(figsize = fig_size)
    ax5 = figure5.add_subplot(111)
    
    inputs5 = {
            "x_data":       storage_discharge_normCapacity_nz,
            "ax":           ax5,
            "x_label":      "Storage discharge energy (fraction of storage capacity)",
            "y_label":      "Probability",
            # "title":        "Histogram on storage's nonzero discharge energy",
            "num_bins":     num_bins,
            "zero_one_range":  1,
            }
    
    func_PMF_plot(inputs5)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure5, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 6 Time series plot of discharge energy
    
    optimization_steps = demand.size
    time_series = np.arange(0, optimization_steps)
    
    mix_matrix = np.column_stack(
                (dispatched_storage_charge, 
                dispatched_storage_discharge))
    
    # title_text = "Storage discharge and charge"
    legend_list = ['Storage charge', 'Storage discharge']
    
    figure6 = plt.figure(figsize = fig_size)
    ax6 = figure6.add_subplot(111)
    
    inputs6 = {
            "x_data":        time_series, 
            "y_data":        mix_matrix/1e6,
            "y2_data":       mix_matrix/np.average(demand),
            "ax":            ax6,
            "x_label":       'Time (hour in the year)',
            "y_label":       '1e9 kWh',
            "y2_label":      'hourly-average demand',
            # "title":         title_text,
            "legend":        legend_list,
            "line_width":    1,
            'grid_option':   0,
            }        
            
    func_lines_plot(inputs6)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure6, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 7 Time series of discharge - integral in a moving window
    
    # Calculate, for a rolling basis, how much is cumulative discharge over a certain time period
    
    time_series = np.arange(0, optimization_steps)
    
    dispatched_storage_discharge_MA24 = (
            func_moving_window(dispatched_storage_discharge, 24, 'sum'))
    dispatched_storage_discharge_MA168 = (
            func_moving_window(dispatched_storage_discharge, 24*7, 'sum'))
    dispatched_storage_discharge_MA672 = (
            func_moving_window(dispatched_storage_discharge, 24*28, 'sum'))
    
    mix_matrix = np.column_stack(
                (dispatched_storage_discharge,
                 dispatched_storage_discharge_MA24, 
                dispatched_storage_discharge_MA168,
                dispatched_storage_discharge_MA672))
    
    legend_list = ['1 hour', '1 day', '1 week', '4 weeks']
    
    title_text = 'Storage cumulative discharge'
    
    # -------------------------
    
    figure7 = plt.figure(figsize = fig_size)
    ax7 = figure7.add_subplot(111)
    
    inputs7 = {
            "x_data":        time_series, 
            "y_data":        mix_matrix/1e9,
            "y2_data":       mix_matrix/np.average(demand),
            "ax":            ax7,
            "x_label":       'Time (hour in the year)',
            "y_label":       '1e9 kWh',
            "y2_label":      'hourly-average demand',
            "title":         title_text,
            "legend":        legend_list,
            "line_width":    1,
            'grid_option':   0,
            }        
            
    func_lines_plot(inputs7)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure7, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
#    # Figure 8 Time series of discharging - integral in a moving window (2)
#    
#    time_series = np.arange(0, optimization_steps)
#    
#    #mix_matrix = np.column_stack(
#    #            (dispatched_storage_discharge,
#    #             dispatched_storage_discharge_MA24, 
#    #            dispatched_storage_discharge_MA168))
#    #
#    #legend_list = ['1 hour', '1 day', '1 week']
#    
#    title_text = 'Storage discharged energy (integral in a moving window)'
#    
#    figure8 = plt.figure(figsize = fig_size)
#    ax8 = figure8.add_subplot(111)
#    
#    inputs8 = {
#            "x_data":       time_series, 
#            "y_data":       mix_matrix/np.average(demand),
#            "ax":           ax8,
#            "x_label":      'Time (hour in the year)',
#            "y_label":      'Discharged energy\n(hourly average demand)',
#            "title":        title_text,
#            "legend":       legend_list,
#            "line_width":    1,
#            'grid_option':   0,
#            }        
#            
#    func_lines_plot(inputs8)
#        
#    if SAVE_FIGURES_TO_PDF:
#        pdf_pages.savefig(figure8, bbox_inches='tight')
#        plt.close()
    
    # -------------------------------------------------------------------------    
    
    # Figure 9 Time series of charging - integral in a moving window
    
    time_series = np.arange(0, optimization_steps)
    
    dispatched_storage_charge_MA24 = (
            func_moving_window(dispatched_storage_charge, 24, 'sum'))
    dispatched_storage_charge_MA168 = (
            func_moving_window(dispatched_storage_charge, 24*7, 'sum'))
    dispatched_storage_charge_MA672 = (
            func_moving_window(dispatched_storage_charge, 24*28, 'sum'))
    
    mix_matrix = np.column_stack(
                (dispatched_storage_charge,
                 dispatched_storage_charge_MA24, 
                dispatched_storage_charge_MA168,
                dispatched_storage_charge_MA672))
    
    legend_list = ['1 hour', '1 day', '1 week', '4 weeks']
    
    title_text = 'Storage cumulative charge'
    
    # -------------------------
    
    figure9 = plt.figure(figsize = fig_size)
    ax9 = figure9.add_subplot(111)
    
    inputs9 = {
            "x_data":        time_series, 
            "y_data":        mix_matrix/1e9,
            "y2_data":       mix_matrix/np.average(demand),
            "ax":            ax9,
            "x_label":       'Time (hour in the year)',
            "y_label":       '1e9 kWh',
            "y2_label":      'hourly-average demand',
            "title":         title_text,
            "legend":        legend_list,
            "line_width":    1,
            'grid_option':   0,
            }           
    
    func_lines_plot(inputs9)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure9, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
#    # Figure 10 Time series of charging - integral in a moving window (2)
#    
#    time_series = np.arange(0, optimization_steps)    
#    
#    title_text = 'Storage charged energy (integral in a moving window)'
#    
#    figure10 = plt.figure(figsize = fig_size)
#    ax10 = figure10.add_subplot(111)
#    
#    inputs10 = {
#            "x_data":       time_series, 
#            "y_data":       mix_matrix/np.average(demand),
#            "ax":           ax10,
#            "x_label":      'Time (hour in the year)',
#            "y_label":      'Charged energy\n(hourly average demand)',
#            "title":        title_text,
#            "legend":       legend_list,
#            "line_width":    1,
#            'grid_option':   0,
#            }           
#    
#    func_lines_plot(inputs10)
#    
#    if SAVE_FIGURES_TO_PDF:
#        pdf_pages.savefig(figure10, bbox_inches='tight')
#        plt.close()
    
    # -------------------------------------------------------------------------    
    
    # Figure 11 Time series of state of charge - time series
    
    time_series = np.arange(0, optimization_steps)
    
    title_text = 'Storage state of charge'
    
    figure11 = plt.figure(figsize = fig_size)
    ax11 = figure11.add_subplot(111)
    
    inputs11 = {
            "x_data":       time_series, 
            "y_data":       storage_energy_soc_normalized,
            "y2_data":       storage_energy_soc/np.average(demand),
            "ax":           ax11,
            "x_label":      'Time (hour in the year)',
            "y_label":      'fraction of storage capacity',
            "y2_label":     'hourly-average demand',
            "title":        title_text,
            "line_width":    1,
            'grid_option':   0,
            }           
    
    func_lines_plot(inputs11)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure11, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 12 Change in state of charge over a moving window
    
    # This is a very messy figure!
    
    time_series = np.arange(0, optimization_steps)
    
    storage_energy_soc_normalized = np.reshape(storage_energy_soc_normalized, -1)
    
    storage_energy_soc_normalized_diff_hour = (
        func_change_in_period(storage_energy_soc_normalized, 1))
    storage_energy_soc_normalized_diff_day = (
        func_change_in_period(storage_energy_soc_normalized, 24))
    storage_energy_soc_normalized_diff_week = (
        func_change_in_period(storage_energy_soc_normalized, 24*7))
    storage_energy_soc_normalized_diff_month = (
        func_change_in_period(storage_energy_soc_normalized, 24*28))
    
    mix_matrix = np.column_stack(
                (storage_energy_soc_normalized_diff_hour,
                 storage_energy_soc_normalized_diff_day, 
                storage_energy_soc_normalized_diff_week,
                storage_energy_soc_normalized_diff_month))
    
    legend_list = ['1 hour', '1 day', '1 week', '4 weeks']
    
    title_text = 'Change in storage\'s state of charge'
    
    # -------------------------
    
    figure12 = plt.figure(figsize = fig_size)
    ax12 = figure12.add_subplot(111)
    
    inputs12 = {
            "x_data":       time_series, 
            "y_data":       mix_matrix,
            "y2_data":      mix_matrix * capacity_storage / np.average(demand),
            "ax":           ax12,
            "x_label":      'Time (hour in the year)',
            "y_label":      'fraction of storage capacity',
            "y2_label":     'hourly-average demand',
            "title":        title_text,
            "legend":       legend_list,
            "line_width":    1,
            'grid_option':   0,
            }           
    
    func_lines_plot(inputs12)
    
    ax12.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure12, bbox_inches='tight')
        plt.close()
    
#    # -------------------------------------------------------------------------
#    
#    # Figure 12b Change in state of charge over a moving window
#    
#    # This is a very messy figure!
#    
#    # -------------------------
#    
#    time_series = np.arange(0, optimization_steps)
#    
#    storage_energy_soc_normalized = np.reshape(storage_energy_soc_normalized, -1)
#    
#    storage_energy_soc_normalized_diff_hour = (
#        func_change_in_period(storage_discharge_normDemandAve, 1))
#    storage_energy_soc_normalized_diff_day = (
#        func_change_in_period(storage_discharge_normDemandAve, 24))
#    storage_energy_soc_normalized_diff_week = (
#        func_change_in_period(storage_discharge_normDemandAve, 24*7))
#    storage_energy_soc_normalized_diff_month = (
#        func_change_in_period(storage_discharge_normDemandAve, 24*28))
#    
#    mix_matrix = np.column_stack(
#                (storage_energy_soc_normalized_diff_hour,
#                 storage_energy_soc_normalized_diff_day, 
#                storage_energy_soc_normalized_diff_week,
#                storage_energy_soc_normalized_diff_month))
#    
#    legend_list = ['1 hour', '1 day', '1 week', '4 weeks']
#    
#    title_text = 'Change in storage\'s stored energy\n(normalized to hourly average demand)'
#    
#    # -------------------------
#    
#    figure12b = plt.figure(figsize = fig_size)
#    ax12b = figure12b.add_subplot(111)
#    
#    inputs12b = {
#            "x_data":       time_series, 
#            "y_data":       mix_matrix,
#            "ax":           ax12b,
#            "x_label":      'Time (hour in the year)',
#            #"y_label":      'Change in storage\'s state of charge',
#            "title":        title_text,
#            "legend":       legend_list,
#            "line_width":    1,
#            'grid_option':   0,
#            }           
#    
#    func_lines_plot(inputs12b)
#    
#    if SAVE_FIGURES_TO_PDF:
#        pdf_pages.savefig(figure12b, bbox_inches='tight')
#        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 13 Sorted time series of discharging
    
    time_series = np.arange(0, demand.size)
    
    title_text = 'Storage discharge (sorted by magnitude)'
    
    figure13 = plt.figure(figsize = fig_size)
    ax13 = figure13.add_subplot(111)
    
    inputs13 = {
            "x_data":       time_series, 
            "y_data":       -np.sort(-dispatched_storage_discharge, axis=0)/1e6,
            "y2_data":      -np.sort(-dispatched_storage_discharge, axis=0)/np.average(demand),
            "ax":           ax13,
            "x_label":      'Time (hour in the year)',
            "y_label":      '1e6 kWh',
            "y2_label":     'hourly-average demand',
            "title":        title_text,
            "line_width":    1,
            'grid_option':   0,
            }           
    
    func_lines_plot(inputs13)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure13, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
    
    # Figure 13b Sorted time series of discharging
    
    time_series = np.arange(0, demand.size)
    
    title_text = 'Storage charge (sorted by magnitude)'
    
    figure13b = plt.figure(figsize = fig_size)
    ax13b = figure13b.add_subplot(111)
    
    inputs13b = {
            "x_data":       time_series,
            "y_data":       -np.sort(-dispatched_storage_charge, axis=0)/1e6,
            "y2_data":      -np.sort(-dispatched_storage_charge, axis=0)/np.average(demand),
            "ax":           ax13b,
            "x_label":      'Time (hour in the year)',
            "y_label":      '1e6 kWh',
            "y2_label":     'hourly average demand',
            "title":        title_text,
            "line_width":    1,
            'grid_option':   0,
            }
    
    func_lines_plot(inputs13b)
    
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.savefig(figure13b, bbox_inches='tight')
        plt.close()
    
    # -------------------------------------------------------------------------
        
    if SAVE_FIGURES_TO_PDF:
        pdf_pages.close()
        
#%%
# -----------------------------------------------------------------------------
# func_graphics_storage_results_1scenario
#
# Input
#   input_data, a DICT variable, containing inforamtion related to where to locate
#       the optimization results and where to put the output files
#   intput_side (optimization results)'
#       DATA_TYPE
#       directory_optimization_results
#   output_side (graphical outputs)
#       directory_output
#       graphics_file_name
#       SAVE_FIGURES_TO_PDF
#
# Output
#   8 or 15 figures depending on which function is called
#   a set of relevant figures about energy storage usage from an optimization
#
# Functions called
#   func_plotting_storage_static_1scenario()
#   func_plotting_storage_static_1scenario_1(), depending on the cases.
#
# Usage
#   Quite stand alone, can be directly called by a script file
#        
# History
#   Jun 10, 2018 drafted the function
#   Jun 21, 2018 updated the code for loading the optimization results from files
#        
# @ Fan Tong
# -----------------------------------------------------------------------------

def func_graphics_storage_results_1scenario(input_data):
    
    # -------------------------------------------------------------------------
    
    optimization_results_file_path = input_data["optimization_results_file_path"]
    directory_output = input_data["directory_output"]
    graphics_file_name = input_data["graphics_file_name"]
    SAVE_FIGURES_TO_PDF = input_data["SAVE_FIGURES_TO_PDF"]

    # -------------------------------------------------------------------------

    # load the optimization assumptions and results
    
    temp_dict = func_load_optimization_results(optimization_results_file_path)
    model_inputs = temp_dict['model_inputs']
    model_results = temp_dict['model_results']    
    
    # -------------------------------------------------------------------------
    
    # Get the needed data and call the ploting function
    
    demand = model_inputs['demand']

    dispatched_storage_charge = model_results["dispatched_storage_charge"]
    dispatched_storage_discharge = model_results["dispatched_storage_discharge"]
    storage_energy_soc = model_results["storage_energy_soc"]
    capacity_storage = model_results["capacity_storage"]
    
    inputs = {
            "storage_energy_soc":           storage_energy_soc,
            "capacity_storage":             capacity_storage,
            "dispatched_storage_discharge": dispatched_storage_discharge,
            "dispatched_storage_charge":    dispatched_storage_charge,
            "demand":                       demand,
            "directory_output":             directory_output,
            "graphics_file_name":           graphics_file_name,
            "SAVE_FIGURES_TO_PDF":          SAVE_FIGURES_TO_PDF,
            }

    # Call function

    #func_plotting_storage_static_1scenario(inputs)

    # Here is an outpudated information, which would generate figures to show
    #   the same information as in func_plotting_storage_static_1scenario().
    #   But instead of using subplots to combine figures, this _1() function
    #   generated each figure seperately.

    inputs["graphics_file_name"] = graphics_file_name + "_1"
    func_plotting_storage_static_1scenario_1(inputs)        