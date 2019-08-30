#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 15:23:35 2019

@author: jscastanoc
"""
import os, sys
import json
import numpy as np
import collections
from importlib import reload
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sys.path.append(os.environ['STUPS_TOOLBOX'])
import stups 
from stups.experiments.plotting.explorer import ExplorerCopyDraw
reload(stups)

stups.constants.RESULTS_DIR = '/mnt/fs_nemo_work/results/stups'



Metrics = collections.namedtuple('Metrics', 'metric perf_constraint')
ExpProperties = collections.namedtuple('ExpProperties', 'name metrics color')

experiment = {'spoc_gridsearch': ExpProperties(name='spoc_001', 
                                              metrics=Metrics(metric='metrics-test_pearson',
                                                              perf_constraint='metrics-pval_pearson'),
                                              color='#669900'),
              'ssd_gridsearch': ExpProperties(name='ssd_001', 
                                              metrics=Metrics(metric='metrics-test_pearson',
                                                              perf_constraint='metrics-pval_pearson'),
                                              color='#cccc00'),
             'csp_gridsearch': ExpProperties(name='csp_001', 
                                              metrics=Metrics(metric='metrics-test_class_accuracy',
                                                              perf_constraint='metrics-pval_class_accuracy'),
                                              color='#cc6699')}
                                              
sessions = {'VPpcac_18_04_11': [],
           'VPpcad_18_07_19': [[4.479321570302304, 6.954853569374958, 'csp_gridsearch']],
           'VPpcae_18_09_03': [],
           'VPpcaf_18_11_22': [],
           'VPpcag_19_02_28': [],
           'VPpcah_19_05_17': [[3.4009528967263374, 5.573454919897326, 'spoc_gridsearch']],
           'VPpcaj_19_07_11': []}



DEBUG=False
plt.close('all')
for session, props in sessions.items():
    if not props:
        continue
    vp = session.split('_')[0]
    date = '_'.join(session.split('_')[1:])
    with open(stups.constants.SESSION_CFG, 'r') as f:
        session_cfg = json.load(f)[vp]
    
    if not DEBUG:
        df_all_experiments = []
    #fig, ax1 = plt.subplots(figsize=(4,3))    
    #ax = [ax1]
    #ax.append(ax[-1].twinx())
    
    x_offset = 0
    #for ix, (c_exp, c_exp_prop)  in enumerate(experiment.items()):
    c_exp = props[0][-1]
    c_exp_prop = experiment[c_exp]
    tol = 0.1
    c_fc = np.mean(props[0][0:-1])
    c_fw = np.diff(props[0][0:-1])[0]
    
    exp_id = c_exp_prop.name
    perf_constraint = c_exp_prop.metrics.perf_constraint
    metric = c_exp_prop.metrics.metric
    
    plotter = stups.experiments.plotting.explorer.PlotCopyDraw(c_exp, exp_id,
                                                                   constraints = {'meta-session':session,
                                                                  perf_constraint:[-np.inf,0.05],
                                                                  'parameters-fc': [c_fc-tol, c_fc+tol ],
                                                                  'parameters-fw': [c_fw-tol, c_fw+tol ]})
    #plotter.
    epochs_plot = plotter.plot_timeseries(plotter.df_filter.index[0],
                                          split='stim', reject=None,
                                          baseline=(None,0), plot_args=dict())
    
    for ix in range(len(epochs_plot[0])):
        epochs_plot[0][ix].filter(1,10)
        epochs_plot[0][ix].plot(scalings=dict(eeg=1))
    #break
    