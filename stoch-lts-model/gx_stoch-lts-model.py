
import numpy as np
from scipy.integrate import quad

from pload import L


get_label = lambda df: r"$\mu_b = "+str(df["bn_mu"])+"$"
L = L()


# L.pload("kmcartsdd_Xo1.0E-01_XT1.0E-02_a0.9987_bn-mu0.0000_bn-dt0.022000_N2.0E+01_Tmax5.0E+03")
L.pload("kmcartsdd_Xo1.0E-01_XT1.0E-02_a0.9987_bn-mu0.0000_bn-dt0.022000_N2.0E+01_Tmax1.0E+03")





def plot_fpt(df, ax):

    df_ts = df["Ts"]
    
    counts, edges = np.histogram(np.array(df_ts),
                                 bins=np.arange(1,df["Tmax"],10.),
                                 # bins=10**np.linspace(0,5,150),
                                 density=True)
    centers = (edges[:-1] + edges[1:])/2.
    ax.plot(centers, counts, '.', label=get_label(df))

    # counts, edges = np.histogram(np.array(df_ts),
    #                              bins=np.arange(1,df["Tmax"],500.),
    #                              density=True)
    # centers = 10**((np.log10(edges[:-1]) + np.log10(edges[1:]))/2.)
    # ax.plot(centers, counts, '.', label=get_label(df))

def plot_wtail(df, ax):

    ax.hist(df["wrecs"], bins=10**np.linspace(-3,1.,100),
            log=False, normed=True, histtype=u'step', label=get_label(df))



import matplotlib as mpl
mpl.use('Agg')

from matplotlib import style
style.use('classic')

import pylab as pl
from matplotlib import rc

rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Sans serif']})
rc('text', usetex=True)
pl.rcParams['text.latex.preamble'] = [
    r'\usepackage[eulergreek]{sansmath}',  
    r'\sansmath',               
    r'\usepackage{siunitx}',   
    r'\sisetup{detect-all}'
]  


fig = pl.figure()
fig.set_size_inches(6.,1.2)

ax = fig.add_subplot(111)
xlow = 150+25

df = L.dfs[0]

i, k = 2,0
while k<df["Tmax"]:
    if df["wrecs"][i,k]>0:
        break
    else:
        k+=1
z=k
low=k
while low<df["Tmax"]:
    if df["wrecs"][i,low]>0:
        low+=1
    else:
        break

xva = range(k-(df["Tmax"]-900)+22,k)
yva = df["wrecs"][11][900:df["Tmax"]][6:-16]



ax.plot(xva, yva, 'grey')

print(yva)

ax.plot(range(k,low),df["wrecs"][i][k:low], 'black')


ax.plot([xlow,k-(df["Tmax"]-900)+22],[df["X_0"]]*2, 'black', linestyle=':')

while k<df["Tmax"]:
    if df["wrecs"][i,k]>0:
        k+=1
    else:
        break

i, l = 16,0
while l<df["Tmax"]:
    if df["wrecs"][i,l]>0:
        break
    else:
        l+=1

ax.plot(range(k,df["Tmax"]),df["wrecs"][i][l:l+df["Tmax"]-k], 'grey')

ax.plot([k, df["Tmax"]*1.05],[df["XT"]]*2, 'black', linestyle=':')

print(len(list(range(k,df["Tmax"]))))
print(len(df["wrecs"][i][l:l+df["Tmax"]-k]))


ax.set_xlim(xlow, df["Tmax"]*1.05)
ax.set_ylim(bottom=-0.0875)


pl.xticks([z-(df["Tmax"]-900)+22,z,k, df["Tmax"]], ['$t=0$', '','', '$t=t_{\mathrm{max}}$'])
pl.yticks([df["X_0"]], ["$X_{\mathrm{insert}}$"])

ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
# ax
pl.yticks([df["XT"], df["wrecs"][i][l+df["Tmax"]-k]], ["$X_\mathrm{prune}$", "$X_{T_{\mathrm{max}}}$"])

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

ax.tick_params(axis='x', which='major', pad=7)

l = k-z
mid = z+(k-z)/2
sep = 30
hl=(k-z)*0.025
hw=0.03

ax.arrow(mid-sep,-0.35, -(l/2-sep), 0., clip_on=False, shape='full',
         head_width=hw, head_length=hl,
         head_starts_at_zero=False, color='k',
         length_includes_head=True)

ax.arrow(mid+sep,-0.35, (l/2-sep), 0., clip_on=False, shape='full',
         head_width=hw, head_length=hl,
         head_starts_at_zero=False, color='k',
         length_includes_head=True)

ax.text(mid, -0.38, '$T$', fontdict={'ha': 'center'}, clip_on=False)


# ax.arrow(z,-0.35, k-z, 0., clip_on=False, shape='full',
#          head_width=0.05, head_length=(k-z)*0.05,
#          head_starts_at_zero=False, color='k')


import os
fname = os.path.splitext(os.path.basename(__file__))[0]

fig.savefig("{}.pdf".format(fname), dpi=300, bbox_inches='tight')



# copy the generated graphic to thesis LaTeX folder
from shutil import copyfile
dest = "/home/fh/sci/rsc/dctrl/pub/scrpt/img/"
copyfile("{}.pdf".format(fname), dest+"{}.pdf".format(fname))
print("Copied file to \n\t" + dest + "{}.pdf".format(fname))
