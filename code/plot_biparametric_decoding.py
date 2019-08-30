import os, sys
import json
from importlib import reload
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.environ['STUPS_TOOLBOX'])
sys.path.append(os.environ['FSPOC_TOOLBOX_PY'])

import stups 
from stups.experiments.plotting.plotting import PlotCopyDraw
from stups import constants
reload(stups)

stups.constants.RESULTS_DIR = '/mnt/fs_nemo/results/'
print(stups.constants.RESULTS_DIR)

experiment = 'spoc_gridsearch'
experiment_id = 'spoc_001'

plotter = PlotCopyDraw(experiment, experiment_id, preload=True)

available_sessions =['VPpcac_18_01_17',
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
                     'VPpcaj_19_05_31',
                     'VPpcaj_19_06_01']
available_sessions.sort()

#%%
for session in available_sessions:
    vp = session.split('_')[0]
    date = '_'.join(session.split('_')[1:])
    with open(constants.SESSION_CFG, 'r') as f:
        session_cfg = json.load(f)[vp]
    #break
    f, ax = plt.subplots(1,figsize=(3.2,2.2))
    
    plotter.df_filter = plotter._filter_results({'metrics-pval_pearson':[0,0.01],
                             'meta-session': session})
    
    
    plotter.biparametric_plot(['parameters-fc','parameters-fw'],
                              'metrics-test_pearson',
                              plot_args=dict(ax=ax,
                                         colormap='YlOrBr',
                                         edgecolor=None,
                                         vmin=.0, vmax=.5,
                                         colorbar=False))
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlim([0,35])
    ax.set_ylim([1,8])
    ax.grid()
    f.savefig('figures/decoding_pearson/decoding_pearson_%s_%s.pdf' % (vp,session_cfg[date]['day']))
    #ax.set_ylim([0,1])
    #break