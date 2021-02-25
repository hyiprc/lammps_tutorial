
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


data = lmplog.read('example_output/tensile.log')

fig = plt.figure(figsize=(w/dpi,h/dpi), dpi=dpi)
gs = mpl.gridspec.GridSpec(1, 1)
#gs.update(left=None,right=None,hspace=0.0)

ax = plt.subplot(gs[0])
# ---------------------------
start = data['ix_eq'][1][0]
ref = data['lz'][start]
x = (np.array(data['lz'][start:]) - ref)/ref # strain
y = -np.array(data['pzz'][start:])*1e-4  # stress in GPa unit from pressure unit bar
ax.scatter(x,y,color='b',label='strain rate: 1e9',edgecolors='none',s=60)
#ax.plot(x,y,color='b',label='rate = 1e9',linewidth=2.)
# ----- line fit ------
a,b = np.polyfit(x,y,1)
x_fit = np.linspace(x[0],x[-1],20)
plt.plot(x_fit,a*x_fit+b,color='k',label=f"y = {a:.3f}x + {b:.3f}",linewidth=3.)
# ---------------------------
ax.set_xlim(xmin=0.0, xmax=None)
ax.set_ylim(ymin=0.0, ymax=None)
ax.xaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.yaxis.set_minor_locator(mpl.ticker.AutoMinorLocator())
ax.set_xlabel('strain')
ax.set_ylabel('stress (GPa)')
ax.yaxis.labelpad=20
ax.legend()

plt.savefig('stress_strain.png')
