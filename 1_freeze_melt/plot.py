
# -----------------------------------------------------------
import sys
sys.path.insert(0,'../scripts')
import lmplog

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg') # TKAgg, macOSX

w = 2048/1.5
h = w*(5.**0.5-1.)/2.
dpi = 96
sc = 0.52

mpl.rc('figure',facecolor='white') # titlesize=40*sc
mpl.rc('mathtext',default='regular')
mpl.rc('axes',titlesize=50*sc,labelsize=45*sc,\
              lw=3.*sc,grid=False) # labelpad=10.
mpl.rc('legend',fontsize=45*sc,fancybox=False,shadow=False,facecolor='white')
mpl.rc('xtick',labelsize=45*sc,direction='in')
mpl.rc('ytick',labelsize=45*sc,direction='in')
mpl.rc('xtick.major',size=20.*sc,width=3.*sc,pad=7.)
mpl.rc('ytick.major',size=20.*sc,width=3.*sc,pad=7.)
mpl.rc('xtick.minor',size=15.*sc,width=2.*sc)
mpl.rc('ytick.minor',size=15.*sc,width=2.*sc)
mpl.rc('lines',linewidth=5*sc)
mpl.rc('savefig',bbox='tight',dpi=dpi)
mpl.rc('figure.subplot',hspace=0.25)
mpl.rc('font',family='serif')
mpl.rc('mathtext',default='regular',fontset='dejavuserif')
# -----------------------------------------------------------


data_freeze = lmplog.read('example_output/freeze.log')
data_melt = lmplog.read('example_output/melt.log')
show = ['temp','press','poteng','density','c_msd[4]']


fig = plt.figure(figsize=(w/dpi,0.5*len(show)*h/dpi), dpi=dpi)
gs = mpl.gridspec.GridSpec(len(show), 1)
gs.update(left=None,right=None,hspace=0.0)

for i,name in enumerate(show):
    ax = plt.subplot(gs[i])
    # ---------------------------
    start = data_freeze['ix_eq'][0][0]+1
    x = np.array(data_freeze['step'][start:])/1000.
    y = data_freeze[name][start:]
    ax.plot(x,y,color='b',label='freeze',linewidth=2.)
    # ---------------------------
    start = data_melt['ix_eq'][0][0]+1
    x = np.array(data_melt['step'][start:])/1000.
    y = data_melt[name][start:]
    ax.plot(x,y,color='r',label='melt',linewidth=2.)
    # ---------------------------
    ax.set_xlim(xmin=0.0, xmax=None)
    ax.set_ylim(ymin=None, ymax=None)
    ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
    ax.set_ylabel(name)
    ax.yaxis.labelpad=20
    if i == (len(show)-1):
        ax.set_xlabel('step/1000')
        ax.legend()
    else:
        ax.set_xticklabels([])

plt.savefig('thermo_output.png')
