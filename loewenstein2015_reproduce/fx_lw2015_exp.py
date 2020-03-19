import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pl

matplotlib.rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage{tgheros}',    
    r'\usepackage[eulergreek]{sansmath}',   
    r'\sansmath',
    r'\usepackage{siunitx}',    
    r'\sisetup{detect-all}'
]  


import numpy as np
from scipy import optimize

from load_data_equal import *
from data_extracted_from_figure import xvals_data, yvals_data, yerrs


def powerlaw_func_s(t, gamma, s):
    return (t/s+1)**(-1*gamma)

def powerlaw_func(t, gamma):
    return (t+1)**(-1*gamma)

def powerlaw_classic(t, alpha, c, k):
    return k*t**(-1*alpha) + c


xfig = 2.85
# fig, (ax1,ax2) = pl.subplots(2,1)
# fig.set_size_inches(xfig*1.4*1.22,3.2*1.22)


fig, (ax1,ax2,ax3) = pl.subplots(1,3,
                                 gridspec_kw={'width_ratios': [1.3, 1.3,1]})
fig.set_size_inches(xfig*1.4*1.22*1.2*1.05,2.2*1.22)


df = load_lw2015_data()
df = add_unique_id(df)

session, srvprb = lw2015_sampling(df)
day = [4*sno for sno in session] + [20,24,28,32,36,40,44]

from_data, from_figure = True, True
pl_fit, pls_fit = False, False

# base_line, = ax.plot(day, srvprb, 'x', label='from data')

for ax in [ax1,ax2]:


    if from_figure:

        unit = 1
        xvals_data_sec = [x*unit for x in xvals_data]

        master = np.sum(np.array(yvals_data[:-1])*(-1*np.diff(yvals_data)))/np.sum(np.array(yvals_data[:-1]))

        print()
        print(np.diff(yvals_data))
        print(yvals_data)

        ax.errorbar(xvals_data_sec, yvals_data,
                    yerr=yerrs, fmt='.', color='k',
                    label='data from Loewen-\nstein et al.~(2015)', zorder=100)

    

    if from_data:

        xs = np.linspace(0, day[-1], 1000)
        ys = (xs/4+1)**(-1.384)


        klabel =   'power law model \n ' + \
                  r'\[f(t) = (\frac{t}{\text{\SI{4}{d}}}+1)^{-\gamma},\]' +\
                   '\nwith ' + r'$\gamma=1.384$'

        ax.plot(xs,ys, 'red', label=klabel, zorder=50)


    # if True:

    #     xs = np.linspace(0, day[-1], 1000)
    #     ys = (xs/4+1)**(-1.10082)

    #     klabel = r'$f(t) = (t+1)^{-\gamma}$,'+'\n $\gamma=1.101$'

    #     ax.plot(xs,ys, 'grey', label=klabel)




    if pl_fit:


        prm, prm_cov = optimize.curve_fit(powerlaw_func,
                                          day, srvprb, 
                                          p0=[1.5])

        slabel = '$\gamma = %.4f$' %(prm[0])

        xs = np.linspace(0, day[-1], 1000)

        # cnt_vx = cnt_v
        ax.plot(xs, powerlaw_func(xs,*prm),
                color=base_line.get_color(), linestyle='-',
                label=slabel, alpha=0.9)    


    if pls_fit:


        prm, prm_cov = optimize.curve_fit(powerlaw_func_s,
                                          xvals_data_sec, yvals_data,
                                          # day, srvprb, 
                                          p0=[1.5, 1])

        slabel = '$\gamma = %.4f$' %(prm[0]) +\
                 ',\n' +  r'$s\approx' +'%.2f$' %(prm[1])

        xs = np.linspace(0, day[-1], 1000)

        # cnt_vx = cnt_v
        ax.plot(xs, powerlaw_func_s(xs,*prm),
                color=base_line.get_color(), linestyle='--',
                label=slabel, alpha=0.9)    


    if True:
        # xs = np.linspace(0, day[-1], 1000)

        # p = master
        p = (1421-999)/1421.

        # xs = np.array([0, 1, 2, 3, 4, 5, 6, 7])
        xs = np.linspace(0, 11, num=1000)
        ys = (1-p)**xs
        label='exponential model'
        ax.plot(xs*4, ys, label=label)



    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')


    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])


    
ax1.set_xlabel('time since synapse\n growth [d]')    
ax2.set_xlabel('time since synapse\n growth [d]')

ax1.set_ylabel('probability of survival')
# ax2.set_ylabel('probability of survival')


# # ax.set_ylim(top=1.05)
ax2.set_xlim(left=2*10**-1)
ax2.set_yscale('log')
ax2.set_xscale('log')

ax3.axis('off')

handles, labels = ax2.get_legend_handles_labels()
order = [2,0,1]
handles= [handles[idx] for idx in order]
labels = [labels[idx] for idx in order]

ax2.legend(handles, labels, frameon=False, prop={'size': 10},
           loc='center left', labelspacing=1.15, borderpad=1.25,
           bbox_to_anchor=(1, 0.5))


    
fig.tight_layout(rect=[0., 0., 1, 0.95])

import os
fname = os.path.splitext(os.path.basename(__file__))[0]
fig.savefig("{}.pdf".format(fname), dpi=300,
           bbox_inches='tight')


# copy the generated graphic to thesis LaTeX folder
from shutil import copyfile
dest = "/home/fh/sci/rsc/dctrl/pub/scrpt/img/"
copyfile("{}.pdf".format(fname), dest+"{}.pdf".format(fname))
print("Copied file to \n\t" + dest + "{}.pdf".format(fname))
