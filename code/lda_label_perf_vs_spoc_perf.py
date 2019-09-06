#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 17:17:19 2019

@author: jscastanoc
"""

import os, sys
from os.path import join
import json
from importlib import reload
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
#rc('font',**{'family':'serif'})
#rc('text', usetex=True)
plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=15)
sys.path.append(os.environ['STUPS_TOOLBOX'])
sys.path.append(os.environ['FSPOC_TOOLBOX_PY'])

import stups 
from stups.experiments.plotting.plotting import PlotCopyDraw
from stups import constants
from stups.processing import projection_performance_metrics

experiment = 'spoc_gridsearch'
experiment_id = 'spoc_001'

sessions = constants.SESSIONS_COPYDRAW

plt.close('all')

str_xaxis = 'AUC - LDA for label generation'
figure_size = (4,3)

fig_ncomp = plt.figure(figsize = figure_size)
ax_ncomp  = plt.axes()
ax_ncomp.set_xlabel(str_xaxis)
ax_ncomp.set_ylabel('$\%$ signif. comp.')
ax_ncomp.grid(True)

fig_maxdec = plt.figure(figsize = figure_size)
ax_max_dec = plt.axes()
ax_max_dec.set_xlabel(str_xaxis)
ax_max_dec.set_ylabel('RegTask - best decoding')
ax_max_dec.grid(True)

#ax_ncomp.axis('equal')
#ax_max_dec.axis('equal')
for session in sessions:
    plotter = PlotCopyDraw(experiment, experiment_id, preload=False,
                           constraints = {'meta-session': session})
    plotter.load_results()
    df_scores, y, ix_clean = plotter.load_labels(session)
    
    _, _, decoding_auc =projection_performance_metrics(df_scores[constants.STANDARD_PERFORMANCE_METRICS], 
                                   df_scores['stim'],
                                    detrend=True, 
                                    t_stamps=df_scores['startTStamp'].values,
                                    reject_outliers=True,
                                    return_performance=True)
    average_lda_auc = np.mean(decoding_auc)
    
    n_signf_components = (plotter.df_filter['metrics-pval_pearson'] < 0.02).sum()/len(plotter.df_filter['metrics-pval_pearson'])
    max_decoding_perf = plotter.df_filter['metrics-test_pearson'].max()
    
    ax_ncomp.scatter(average_lda_auc, n_signf_components, c='royalblue')
    ax_max_dec.scatter(average_lda_auc, max_decoding_perf, c='royalblue')
    #break
    
savedirfig = '/home/jscastanoc/Desktop/tmp/output_stups_overview/'
figname = join(savedirfig,'auclda_vs_ncomp.pdf')
fig_ncomp.savefig(figname, bbox_inches = 'tight')

figname = join(savedirfig,'auclda_vs_bestdec.pdf')
fig_maxdec.savefig(figname, bbox_inches = 'tight')
# load lda performance

# load 