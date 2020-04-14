# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 20:46:55 2020

@author: FSalinas
email: fabio.salinas1982@gmail.com
"""

from matplotlib import pyplot as plt
from matplotlib.cbook import boxplot_stats
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats

def getstats(X, varname):
    '''
    The function need two varibles: X and varname
    
    Parameters
    ----------
    X : LIST with numeric values
    varname : STRING with the name of the variable
    
    Returns two objects: outliers, ndf
    -------
    outliers: List with the outlier values.
    ndf: Pandas Dataframe object with trhe statistic values calculated.
    '''
    plt.style.use('seaborn-whitegrid')

    f, (ax_box, ax_hist) = plt.subplots(
        2,
        sharex = True,
        figsize = (17, 7),
        gridspec_kw = {"height_ratios": (0.2, 1)}
    )
    
    outliers = [y for stat in boxplot_stats(X) for y in stat['fliers']]
    
    description = pd.DataFrame(
        X,
        columns=[varname]
    ).describe()
    ndf = {}
    for med in description.index:
        ndf[med] = round(description.loc[med][0], 2)
    ndf['median'] = round(np.median(X), 2)
    ndf['mode'] = round(list(stats.mode(X))[0][0], 2)
    ndf['kurtosis'] = round(stats.kurtosis(X), 2)
    ndf['skewness'] = round(stats.skew(X), 2)
    ndf['# outliers'] = len(outliers)
    
    sdf = pd.DataFrame(data=None, columns = ['variable', 'value'])
    sdf['variable'] = list(ndf.keys())
    sdf['value'] = list(ndf.values())

    sns.boxplot(X, ax = ax_box)
    ax_box.axvline(ndf['mean'], color = 'r', linestyle = '--')
    ax_box.axvline(ndf['median'], color = 'g', linestyle = '-')

    sns.distplot(X, ax = ax_hist)
    ax_hist.axvline(ndf['mean'], color = 'r', linestyle = '--')
    ax_hist.axvline(ndf['median'], color = 'g', linestyle = '-')

    plt.legend({'Media':ndf['mean'],'Mediana':ndf['median']})
    ax_hist.set(xlabel=varname)
    
    sl = []
    for fil in sdf.index:
        sl += ['{var}: {val:,.2f}'.format(var = sdf.loc[fil,'variable'], val = sdf.loc[fil,'value'])]

    textstr = '\n'.join(sl)

    props = dict(boxstyle='round', facecolor='#eafff5', alpha=0.5)

    ax_hist.text(
        0.05,
        0.95,
        textstr,
        transform = ax_hist.transAxes,
        fontsize = 14,
        verticalalignment = 'top',
        bbox = props
    )

    plt.show()

    return(outliers, ndf)