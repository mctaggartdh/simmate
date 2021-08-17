# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------------------

from simmate.configuration.django import setup_full  # ensures setup
from simmate.database.diffusion import Pathway as Pathway_DB

queryset = (
    Pathway_DB.objects.filter(
        vaspcalca__energy_barrier__isnull=False,
        empiricalmeasuresb__isnull=False,
        structure__e_above_hull__lte=0.05,
    )
    .select_related("vaspcalca", "empiricalmeasuresb", "structure")
    .all()
)
from django_pandas.io import read_frame

df = read_frame(
    queryset,
    fieldnames=[
        "id",
        "length",
        "structure__id",
        "structure__formula_full",
        "structure__spacegroup",
        "structure__formula_anonymous",
        "structure__e_above_hull",
        "empiricalmeasuresb__ewald_energya",
        "empiricalmeasuresb__ewald_energyb",
        "empiricalmeasuresb__ewald_energyc",
        "empiricalmeasuresb__ewald_energyd",
        "empiricalmeasuresb__ewald_energye",
        "empiricalmeasuresb__ewald_energyf",
        "empiricalmeasuresb__ewald_energyg",
        # "empiricalmeasuresb__ewald_energyh",
        # "empiricalmeasuresb__ewald_energyi",
        # "empiricalmeasuresb__ewald_energyj",
        "empiricalmeasuresb__bond_lengthx",
        "empiricalmeasuresb__bond_lengthy",
        "empiricalmeasuresb__bond_lengthz",
        "empiricalmeasuresb__csm_alpha",
        "empiricalmeasuresb__csm_beta",
        "empiricalmeasuresb__csm_gamma",
        "vaspcalca__energy_barrier",
    ],
)

import numpy
df["test"] = df["empiricalmeasuresb__ewald_energyb"] * ((numpy.exp(df["empiricalmeasuresb__bond_lengthx"] / 1.5) - 1)**2) - df["empiricalmeasuresb__ewald_energyb"]

# --------------------------------------------------------------------------------------

# The code below is for interactive plotting using Plotly
import plotly.express as px

fig = px.scatter(
    data_frame=df,
    x="empiricalmeasuresb__ewald_energyb",
    y="vaspcalca__energy_barrier",
    # color="vaspcalca__energy_barrier",
    # range_color=[0, 1.1],
    # log_x=True,
    # log_y=True,
    hover_data=[
        "id",
        "length",
        "structure__id",
        "structure__formula_full",
        "structure__spacegroup",
        "structure__formula_anonymous",
        "structure__e_above_hull",
        "empiricalmeasuresb__ewald_energya",
        "vaspcalca__energy_barrier",
    ],
)
fig.show(renderer="browser", config={"scrollZoom": True})
# fig.write_html("delta_ewald_normalized.html")

# --------------------------------------------------------------------------------------


import matplotlib.pyplot as plt

# start with a square Figure
fig = plt.figure(figsize=(8, 8))

# Add a gridspec (which sets up a total of 4 subplots for us -- and we use 3)
gs = fig.add_gridspec(
    # grid dimensions and column/row relative sizes
    nrows=2,
    ncols=2,
    width_ratios=(7, 2),
    height_ratios=(2, 7),
    #
    # size of the overall grid (all axes together)
    left=0.1,
    right=0.9,
    bottom=0.1,
    top=0.9,
    #
    # spacing between subplots (axes)
    wspace=0.05,
    hspace=0.05,
)

# HEXBIN SUBPLOT
# create the axes object
ax = fig.add_subplot(
    gs[1, 0],  # bottom left subplot
    xlabel=r"Pathway Length ($\AA$)",
    ylabel=r"$\Delta$ Ewald Energy (eV)",
    facecolor="lightgrey",  # background color
)
# add dashed lines at x=0 and y=0
# ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
# ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
# create the hexbin subplot
hb = ax.hexbin(
    x=df["length"],  # X
    y=df["empiricalmeasuresb__ewald_energyb"],  # Y
    C=df["vaspcalca__energy_barrier"],  # COLOR
    gridsize=20,  # size of hex bins
    cmap="RdYlGn_r",  # color scheme for colorbar
    vmin=0,
    vmax=7.5,  # upper limit of colorbar
    edgecolor="black",  # color between hex bins
)
# add the colorbar (for positioning we give it its own axes)
# where arg is [left, bottom, width, height]
cax = fig.add_axes([0.125, 0.65, 0.35, 0.03])
cb = fig.colorbar(
    hb,  # links color to hexbin
    cax=cax,  # links location to this axes
    orientation="horizontal",
    label="Energy Barrier (eV)",
)

# X-AXIS HISTOGRAM
ax_histx = fig.add_subplot(
    gs[0, 0],  # top left subplot
    sharex=ax,
    ylabel="Pathways (#)",
    # facecolor="lightgrey",  # background color
)
ax_histx.hist(
    x=df["length"],
    bins=75,
    color="black",
    edgecolor="white",
    linewidth=0.5,
)

# Y-AXIS HISTOGRAM
ax_histy = fig.add_subplot(
    gs[1, 1],  # bottom right subplot
    sharey=ax,
    xlabel="Pathways (#)",
    # xlim=(0,100),
    # facecolor="lightgrey",  # background color
)
ax_histy.hist(
    x=df["empiricalmeasuresb__ewald_energyb"],
    orientation="horizontal",
    bins=75,
    color="black",
    edgecolor="white",
    linewidth=0.5,
    log=True,
)


# setting subplot(xticklabels=[],) above doesn't work as intended so I do this here
ax_histx.tick_params(axis="x", labelbottom=False)
ax_histy.tick_params(axis="y", labelleft=False)

plt.show()


# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------


import matplotlib.pyplot as plt

# start with a square Figure
fig = plt.figure(figsize=(8, 8))

# Add a gridspec (which sets up a total of 4 subplots for us -- and we use 3)
gs = fig.add_gridspec(
    # grid dimensions and column/row relative sizes
    nrows=2,
    ncols=2,
    width_ratios=(7, 2),
    height_ratios=(2, 7),
    #
    # size of the overall grid (all axes together)
    left=0.1,
    right=0.9,
    bottom=0.1,
    top=0.9,
    #
    # spacing between subplots (axes)
    wspace=0.05,
    hspace=0.05,
)

# HEXBIN SUBPLOT
# create the axes object
ax = fig.add_subplot(
    gs[1, 0],  # bottom left subplot
    xlabel=r"Pathway Length ($\AA$)",
    ylabel=r"Initial Average Bond Length ($\AA$)",
    facecolor="lightgrey",  # background color
)
# add dashed lines at x=0 and y=0
# ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
# ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
# create the hexbin subplot
hb = ax.hexbin(
    x=df["length"],  # X
    y=df["empiricalmeasuresb__bond_lengthx"],  # Y
    C=df["vaspcalca__energy_barrier"],  # COLOR
    gridsize=20,  # size of hex bins
    cmap="RdYlGn_r",  # color scheme for colorbar
    vmin=0,
    vmax=5,  # upper limit of colorbar
    edgecolor="black",  # color between hex bins
)
# add the colorbar (for positioning we give it its own axes)
# where arg is [left, bottom, width, height]
cax = fig.add_axes([0.125, 0.65, 0.35, 0.03])
cb = fig.colorbar(
    hb,  # links color to hexbin
    cax=cax,  # links location to this axes
    orientation="horizontal",
    label="Energy Barrier (eV)",
)

# X-AXIS HISTOGRAM
ax_histx = fig.add_subplot(
    gs[0, 0],  # top left subplot
    sharex=ax,
    ylabel="Pathways (#)",
    # facecolor="lightgrey",  # background color
)
ax_histx.hist(
    x=df["length"],
    bins=75,
    color="black",
    edgecolor="white",
    linewidth=0.5,
)

# Y-AXIS HISTOGRAM
ax_histy = fig.add_subplot(
    gs[1, 1],  # bottom right subplot
    sharey=ax,
    xlabel="Pathways (#)",
    # xlim=(0,100),
    # facecolor="lightgrey",  # background color
)
ax_histy.hist(
    x=df["empiricalmeasuresb__bond_lengthx"],
    orientation="horizontal",
    bins=75,
    color="black",
    edgecolor="white",
    linewidth=0.5,
    # log=True,
)


# setting subplot(xticklabels=[],) above doesn't work as intended so I do this here
ax_histx.tick_params(axis="x", labelbottom=False)
ax_histy.tick_params(axis="y", labelleft=False)

plt.show()
