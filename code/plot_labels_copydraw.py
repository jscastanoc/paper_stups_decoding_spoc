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

plotter = PlotCopyDraw(experiment, experiment_id, preload=False)
#%%
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
             'VPpcah_19_05_17',
             'VPpcaj_19_05_31',
             'VPpcaj_19_06_01',
             'VPpcaj_19_07_11']

available_sessions =[
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
available_sessions.sort()

for session in available_sessions:
    vp = session.split('_')[0]
    date = '_'.join(session.split('_')[1:])
    with open(constants.SESSION_CFG, 'r') as f:
        session_cfg = json.load(f)[vp]
    #break
    f, ax = plt.subplots(1,figsize=(4,2))
    ax = plotter.plot_labels(session, type_plot='hist', plot_args=dict(ax = ax))
    ax.grid()
    f.savefig('figures/histogram_labels/histogram_labels_%s_%s.pdf' % (vp,session_cfg[date]['day']))
    ax.set_ylim([0,1])
    plt.close(f)