import requests, json
import numpy as np
import importlib
import pandas as pd
import os

import seaborn as sns
import matplotlib.pyplot as plt


def plot_barh(s_to_plot, title = '', xlabel = '', ylabel = '',
color_palette = 'YlGnBu', pre_unit = '', suff_unit = '', round_place = '',):
    '''
    Plot horizontal bar graph
    '''
    y_labels = s_to_plot.index

    # Plot the figure.
    plt.figure(figsize=(12, 20))
    ax = s_to_plot.plot(kind='barh')
    plt.barh(s_to_plot.index, s_to_plot,
            color = sns.color_palette(color_palette, len(s_to_plot.index)))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yticklabels(y_labels)
    x_llim, x_ulim = ax.get_xlim()
    #x_ulim = xulim_set
    #ax.set_xlim(x_llim, xulim_set) # expand xlim to make labels easier to read
    plt.tight_layout()
    rects = ax.patches