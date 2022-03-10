# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 00:31:36 2022

@author: Victor Levy dit Vehel, victor.levy.vehel [at] gmail [dot] com
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter, Normalize

def seq_cmap(cmap, n):
    cs = 'rgb({},{},{})'
    mp_val = [cmap(i/(n-1)) for i in range(n)]
    return [cs.format(int(r*255), int(g*255), int(b*255)) for r, g, b, a in mp_val]

def sunbst_cmap(cmap, labels, values, norm = "index"):
    col = {}
    n = len(labels)
    cs = 'rgb({},{},{})'
    for i, (lab, val) in enumerate(zip(labels, values)):
        if norm == "index":
            v = i/(n-1)
        elif norm == "range":
            v = (val - values.min()) / (values.max() - values.min())
        elif norm == "zero":
            v = val / values.max()
        r, g, b, a = cmap(v)
        col[lab] = cs.format(int(r*255), int(g*255), int(b*255))
    return col

def cm_2_plotly(cmap):
    norm = Normalize(vmin=0, vmax=255)
    return [colorConverter.to_rgb(cmap(norm(i))) for i in range(255)]


def sym_cmap(cmap, value):
    """ """
    cs = 'rgb({},{},{})'
    out = []
    value_norm = value / value.abs().max()
    value_range = (value_norm+1)/2
    for val in value_range:
        r, g, b, a = cmap(val)
        out += [cs.format(int(r*255), int(g*255), int(b*255))]
    return out