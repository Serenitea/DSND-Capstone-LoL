import requests, json
import numpy as np
import importlib
import pandas as pd
import os

import seaborn as sns
import matplotlib.pyplot as plt

%matplotlib inline
import pdb
import warnings
warnings.filterwarnings('ignore')


def plot_barh(s_to_plot, title = '', xlabel = '', ylabel = '',
color_palette = 'YlGnBu', pre_unit = '', suff_unit = '', round_place = '',
              xllim_set = 0, xulim_set = 1):

    y_labels = s_to_plot.index

    # Plot the figure.
    plt.figure(figsize=(12, 8))
    ax = s_to_plot.plot(kind='barh')
    plt.barh(s_to_plot.index, s_to_plot,
            color = sns.color_palette(color_palette, len(s_to_plot.index)))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_yticklabels(y_labels)
    #x_llim, x_ulim = ax.get_xlim()
    #x_ulim = xulim_set
    ax.set_xlim(xllim_set, xulim_set) # expand xlim to make labels easier to read
    plt.tight_layout()
    rects = ax.patches

    # For each bar: Place a label
    for rect in rects:
        # Get X and Y placement of label from rect.
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # Number of points between bar and label. Change to your liking.
        space = 5
        # Vertical alignment for positive values
        ha = 'left'

        # If value of bar is negative: Place label left of bar
        if x_value < 0:
            # Invert space to place label to the left
            space *= -1
            # Horizontally align label at right
            ha = 'right'

        label_string = "{:."+str(round_place)+"f}"
        # Use X value as label and format number with one decimal place
        #label = "{:.1f}".format(x_value)
        label = label_string.format(x_value)

        # Create annotation
        plt.annotate(
            pre_unit+label+suff_unit,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(space, 0),          # Horizontally shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            va='center',                # Vertically center label
            ha=ha)                      # Horizontally align label differently for
                                        # positive and negative values.