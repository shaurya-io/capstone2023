import matplotlib.pyplot as plt
from random import randint
import sys
import statistics
from scipy import stats
import numpy as np
from IPython.display import Image
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from glob import glob
import gzip
import json
import time
import os
import subprocess
from tqdm import tqdm
import sys
import pickle
import string
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import NullLocator
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import LogLocator


plt.rc('xtick', labelsize=12)
plt.rc('ytick', labelsize=12)
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

def simplify_cdf(data):
        '''Return the cdf and data to plot
                Remove unnecessary points in the CDF in case of repeated data
                '''
        data_len = len(data)
        assert data_len != 0
        cdf = np.arange(data_len) / data_len
        simple_cdf = [0]
        simple_data = [data[0]]

        if data_len > 1:
                simple_cdf.append(1.0 / data_len)
                simple_data.append(data[1])
                for cdf_value, data_value in zip(cdf, data):
                        if data_value == simple_data[-1]:
                                simple_cdf[-1] = cdf_value
                        else:
                                simple_cdf.append(cdf_value)
                                simple_data.append(data_value)
        assert len(simple_cdf) == len(simple_data)
        # to have cdf up to 1
        simple_cdf.append(1)
        simple_data.append(data[-1])

        return simple_cdf, simple_data

def cdfplot(data_in):
        """Plot the cdf of a data array
                Wrapper to call the plot method of axes
                """
        # cannot shortcut lambda, otherwise it will drop values at 0
        data = sorted(filter(lambda x: (x is not None and ~np.isnan(x)
                                                                        and ~np.isinf(x)),
                                                 data_in))[::-1]

        data_len = len(data)
        if data_len == 0:
                return

        simple_cdf, simple_data = simplify_cdf(data)
        return simple_data, simple_cdf


fig2, ax = plt.subplots(1, 1, figsize = (5,3.54), dpi=300)

ax.boxplot(data,patch_artist=True,showfliers=False,boxprops=dict(facecolor="tab:blue"),showmeans=False)

ax.set_xlabel("Country")
ax.set_ylabel("Ping to Google DNS (ms)")
# ax.set_xticklabels(["Pakistan", "India", "Mexico", "Tunisia", "Colombia", "Korea", "Slovakia", "Kenya", "Portugal"])
# ax.set_xlim([100,0])
# ax.set_ylim([0,1])
# ax.set_xscale('log')
ax.grid()
plt.legend(loc="best",ncol=3)

fig2.tight_layout(pad=0.1)
fig2.savefig('results.pdf')