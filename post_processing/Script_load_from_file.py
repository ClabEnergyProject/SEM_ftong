# -*- coding: utf-8 -*-
"""
Script_Single_Temp.py

Function
    Serves a piece to example code on how to load the optimization results from files.

History
    Feb 18, 2018 (likely) created this example file
    Jun 19, 2018 reproduced this script
    Jun 20, 2018 reproduced this script (re-packaged into a function)
    
@author: Fan
"""

#import numpy as np
#import os
#import sys
from Supporting_Functions import func_load_optimization_results

##%%
## -----------------------------------------------------------------------------
## func_load_optimization_results()
##
## Function: load the optimization assumptions and results from files to the
##   system memory (variable names)
##
## Input
##   optimization_results_file_path -- full file path for the optimization
##                                       assumptions and results
##
## Output
##   A DICT variable with the following keys
##       model_inputs
##       model_results
##
## History
##   Feb 18, 2018
##   Jun 19-20, 2018
## -----------------------------------------------------------------------------
#
#def func_load_optimization_results(optimization_results_file_path):
#    
#    # optimization_results_data_type = input_data['optimization_results_data_type']
#    # optimization_results_file_path = input_data['optimization_results_file_path']
#    
#    # get the file extension automatically
#    
#    filename, optimization_results_data_type = os.path.splitext(optimization_results_file_path)
#
#    # print optimization_results_data_type
#
#    if optimization_results_data_type == ".npz":
#    
#        # How was the files generated?        
#        # The file ABC.npz was created using the SAVEZ function of the numpy package.
#    
#        # Deal with dictionary variables    
#        # First note that when you saved dict variables into .npz files and then retrieve
#        # them back, they have data_type = object (more accurately, it is a numpy.ndarray
#        # type), rather than dictionary, so you have to use them slightly differently.
#        # However, model_results.item() is a dictionary type variable.
#        # So, you access the files like these, model_results.item()['unmet_demand']    
#    
#        # ---------------------------------------------------------------------
#    
#        # Load the data file
#        npzfile = np.load(optimization_results_file_path)
#    
#        # ---------------------------------------------------------------------
#    
#        # Look for what is in the file
#        # The function will list all variable names
#    
#        model_inputs = npzfile['model_inputs'].item()
#        model_results = npzfile['model_results'].item()
#    
#        # ---------------------------------------------------------------------
#    
#    elif optimization_results_data_type == ".pkl":
#        
#        import pickle
#        
#        f = open(optimization_results_file_path, 'rb')
#        model_inputs, model_results = pickle.load(f)
#
#    else:
#        sys.exit('Error! Unsupported file types for optimization results!')
#
#    # -------------------------------------------------------------------------
#
#    output_data = {
#            "model_inputs":     model_inputs,
#            "model_results":    model_results,
#            }
#
#    return output_data

# -----------------------------------------------------------------------------
# This is the code from an older version (script commands)
# -----------------------------------------------------------------------------

#%% graphical settings
#
# SAVE_FIGURES_TO_PDF = 0
#
##%% load the data
#
#DATA_TYPE = 'pkl'
#
#if DATA_TYPE == "npz":
#
#    # The file ABC.npz was created using the SAVEZ function of the numpy package.
#
#    # -------------------------------------------------------------------------
#
#    # Load the data file
#
#    file_path = "D:/M/\WorkCarnegie/Post_Processing/Results_Base/20180514/Without_NG/20180514_1e1/optimization_related.npz"
#    npzfile = np.load(file_path)
#
#    # -------------------------------------------------------------------------
#
#    # Look for what is in the file
#    # The function will list all variable names
#
#    model_inputs = npzfile['model_inputs'].item()
#    model_results = npzfile['model_results'].item()
#
#    # -------------------------------------------------------------------------
#
#    # Deal with dictionary variables
#
#    # First note that when you saved dict variables into .npz files and then retrieve
#    # them back, they have data_type = object (more accurately, it is a numpy.ndarray
#    # type), rather than dictionary, so you have to use them slightly differently.
#    # However, model_results.item() is a dictionary type variable.
#    # So, you access the files like these, model_results.item()['unmet_demand']
#
#elif DATA_TYPE == "pkl":
#    
#    import pickle
#    
#    file_path = "D:/M/\WorkCarnegie/Post_Processing/Results_Base/20180514/Without_NG/20180514_1e1/optimization_related.pkl"
#
#    f = open(file_path, 'rb')
#    model_inputs, model_results = pickle.load(f)

#%% Script

# optimization_results_data_type = 'pkl'
optimization_results_file_path = "D:/M/WorkCarnegie/Post_Processing/Results_Base/20180514/Without_NG/20180514_1e1/optimization_related.pkl"

#input_data = {
#        'optimization_results_data_type':   optimization_results_data_type,
#        'optimization_results_file_path':   optimization_results_file_path,
#        }

load_optimization = func_load_optimization_results(optimization_results_file_path)
model_inputs = load_optimization['model_inputs']
model_results = load_optimization['model_results']