import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as image

import statsbomb as sb

twitter_color = '#141d26'
plt.rcParams["font.size"] = 12

# Change the text color to white
COLOR = 'white'
plt.rcParams['text.color'] = COLOR
plt.rcParams['axes.labelcolor'] = COLOR
plt.rcParams['xtick.color'] = COLOR
plt.rcParams['ytick.color'] = COLOR

color_list = ['#004D98', '#A50044', '#EDBB00', '#DB0030', '#FFED02', '#000000']

COLOR = 'white'

XMAX, XMIN = 120, 0
YMAX, YMIN = 80, 0


def draw_pitch(title=None, outfilepath=None):
    fig, ax = plt.subplots(figsize=(10, 7), facecolor=twitter_color)

    fig.patch.set_facecolor('#141d26')
    ax.patch.set_facecolor('#141d26')

    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    ax.plot([0, 120], [0, 0], color=COLOR)
    ax.plot([120, 120], [0, 80], color=COLOR)
    ax.plot([120, 0], [80, 80], color=COLOR)
    ax.plot([0, 0], [80, 0], color=COLOR)
    ax.plot([60, 60], [0, 80], color=COLOR)
    ax.plot([0, 0], [36, 44], color=COLOR, linewidth=10)
    ax.plot([120, 120], [36, 44], color=COLOR, linewidth=10)

    centreCircle = plt.Circle((60, 40), 12, color=COLOR, fill=False)
    ax.add_patch(centreCircle)

    ax.plot([0, 18],  [18, 18], color=COLOR)
    ax.plot([18, 18],  [18, 62], color=COLOR)
    ax.plot([18, 0],  [62, 62], color=COLOR)
    ax.plot([0, 6],  [30, 30], color=COLOR)
    ax.plot([6, 6],  [30, 50], color=COLOR)
    ax.plot([6, 0],  [50, 50], color=COLOR)


    ax.plot([120, 102],  [18, 18], color=COLOR)
    ax.plot([102, 102],  [18, 62], color=COLOR)
    ax.plot([102, 120],  [62, 62], color=COLOR)
    ax.plot([120, 114],  [30, 30], color=COLOR)
    ax.plot([114, 114],  [30, 50], color=COLOR)
    ax.plot([114, 120],  [50, 50], color=COLOR)
    ax.set_ylim(ax.get_ylim()[::-1])

    ax.tick_params(bottom=False, left=False,
                  labelbottom=False, labelleft=False)

    if title:
        ax.set_title(title)
    if outfilepath:
        plt.savefig(outfilepath, bbox_inches='tight', facecolor=twitter_color)

    plt.show()
    
    return fig, ax


draw_pitch()
