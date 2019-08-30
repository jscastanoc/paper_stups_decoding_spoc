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

stups.constants.RESULTS_DIR = '/mnt/fs_nemo_work/results/'




Metrics = collections.namedtuple('Metrics', 'metric constraint')
ExpProperties = collections.namedtuple('ExpProperties', 'name metrics color')

experiment = {'spoc_gridsearch': ExpProperties(name='spoc_001', 
                                              metrics=Metrics(metric='metrics-test_pearson',
                                                              constraint='metrics-pval_pearson'),
                                              color='#669900'),
              'ssd_gridsearch': ExpProperties(name='ssd_001', 
                                              metrics=Metrics(metric='metrics-test_pearson',
                                                              constraint='metrics-pval_pearson'),
                                              color='#cccc00'),
             'csp_gridsearch': ExpProperties(name='csp_001', 
                                              metrics=Metrics(metric='metrics-test_class_accuracy',
                                                              constraint='metrics-pval_class_accuracy'),
                                              color='#cc6699')}

sessions =['VPpcac_18_01_17',
             'VPpcac_18_04_11',
             'VPpcad_18_06_20',
             'VPpcad_18_07_19',
             'VPpcae_18_09_03',
             'VPpcaf_18_10_26',
             'VPpcaf_18_10_27',
             'VPpcaf_18_11_22',
             'VPpcag_19_01_11',
             'VPpcag_19_01_12',
             'VPpcag_19_02_28',
             'VPpcah_19_04_17',
             'VPpcah_19_05_17',
             'VPpcaj_19_05_31',
             'VPpcaj_19_06_01',
             'VPpcaj_19_07_11']
#session = 'VPpcac_18_01_17'

freq_bins = np.arange(0,37,2)

#colors = ['#669900',''#669900''#cc33ff']
ylims = [[0.,1], [0,1]]

DEBUG=True
with_legend=True
for session in sessions:
    vp = session.split('_')[0]
    date = '_'.join(session.split('_')[1:])
    with open(stups.constants.SESSION_CFG, 'r') as f:
        session_cfg = json.load(f)[vp]
    
    if not DEBUG:
        df_all_experiments = []
    fig, ax1 = plt.subplots(figsize=(4,3))    
    ax = [ax1]
    ax.append(ax[-1].twinx())
    
    x_offset = 0
    for ix, (c_exp, c_exp_prop)  in enumerate(experiment.items()):
        
        if c_exp == 'spoc_gridsearch' or c_exp == 'ssd_gridsearch':
            c_ax = ax[0]
            c_lim = ylims[0]
            axis_color = experiment['spoc_gridsearch'].color
        else:
            c_ax= ax[1]
            c_lim = ylims[1]
            axis_color = experiment['csp_gridsearch'].color
        exp_id = c_exp_prop.name
        constraint = c_exp_prop.metrics.constraint
        metric = c_exp_prop.metrics.metric
        if not DEBUG:
            plotter = stups.experiments.plotting.explorer.PlotCopyDraw(c_exp, exp_id,
                                                                       constraints = {'meta-session':session,
                                                                      constraint:[-np.inf,0.05]})
            df_all_experiments.append(plotter.df_filter)
        df = df_all_experiments[ix]#
        df['freq_binned'] = pd.cut(df['parameters-fc'], freq_bins)
        df['fc_bin_mean'] = np.array([ival.mid for ival in df['freq_binned']],dtype=int)#+x_offset
        x_positions=np.array(sorted([ival.mid for ival in df['freq_binned'].unique()]),dtype=int)
        
        df_mean_per_fc = df.groupby('fc_bin_mean').mean()
        df_size_per_fc = df.groupby('fc_bin_mean').size()
        
        
        toggle_legend = 'brief' if (ix==0 and with_legend) else False
        sns.scatterplot(x=x_positions, y=df_mean_per_fc[metric],
                        size=df_size_per_fc.as_matrix(),size_norm=(1,40),
                        sizes=(1,150),
                        color=c_exp_prop.color, legend=toggle_legend)
        c_ax.set_ylim(c_lim)
        c_ax.set_xticks(freq_bins[::2])
        c_ax.set_xticklabels(freq_bins[::2])
        c_ax.set_xlim([2,37])
        c_ax.set_xlabel('binned frequency [Hz]')
        c_ax.set_ylabel(metric)
        c_ax.tick_params(axis='y', labelcolor=axis_color)
        c_ax.set_title('')
        c_ax.grid(False)
        
    
    fig.suptitle(session)
    legend_str = 'wlegend' if with_legend else 'nolegend'
    fname = 'bubble_csp_spoc_incommon_%s_%s_%s' % (vp,session_cfg[date]['day'], legend_str)
    fig.savefig('/home/jscastanoc/Desktop/tmp/output_stups_overview/%s.pdf' % fname, bbox_inches='tight')
    
    #plt.close(fig)
    if DEBUG:
        break
    