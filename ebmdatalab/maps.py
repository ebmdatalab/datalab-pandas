import glob
import geopandas as gpd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path


def ccg_map(df,
            title="",
            column=None,
            separate_london=False,
            london_layout='horizontal',
            cartogram=False,
            subplot_spec=None,
            show_legend=True,
            map_year=None):
    """Draw a CCG map with London separated out
    """
    # Because this uses subplots to arrange London and England,
    # the only way to arrange nested subplots is via a subplotspec
    assert column, "You must specify a column name to plot"
    df = df.copy()
    # input df must have 'pct' column, plus others as specified
    data_dir = Path(__file__).parent / 'data'

    # Add names and if it's London. Note the names in ccg_for_map must
    # match names in the CCG geojson, as that doesn't include codes at
    # the momemt
    names = pd.read_csv(data_dir / 'ccg_for_map.csv')

    # Check we know about all the codes in the input data
    diff = np.setdiff1d(df["pct"], names['code'])
    if len(diff) > 0:
        raise BaseException("Data contains CCG codes we don't know about: {}".format(diff))

    df = df.merge(names[['code', 'name', 'is_london']],
                  left_on="pct",
                  right_on="code")
    df = df.set_index('name')

    # Load map data
    if cartogram:
        ccgs = gpd.read_file(data_dir / 'ccgs_cartogram.json')
    else:
        if map_year:
            map_file = data_dir / "ccgs_{}.json".format(map_year)
        else:
            map_file = sorted(glob.glob(str(data_dir / "ccgs_2*.json")))[-1]
        ccgs = gpd.read_file(map_file)
    # Normalise names to match `ccg_fo_map` format (above)
    ccgs['name'] = ccgs['name'].str.upper()
    ccgs = ccgs.set_index('name')
    # Remove ones without geometry - these are (usually) federations
    # rather than individual CCGs
    ccgs = ccgs[~ccgs['geometry'].isnull()]

    # Check we can map all the CCGs named in the input data
    diff = np.setdiff1d(df.index, ccgs.index)
    if len(diff) > 0:
        raise BaseException("Data contains CCG names we can't map: {}".format(diff))

    # Join map with data
    gdf = ccgs.join(df)

    # Split into london and rest of England
    gdf_london = gdf[gdf['is_london'] == True]
    gdf_roe = gdf[gdf['is_london'] == False]

    # set common value limits for colour scale
    vmin = df[column].min()
    vmax = df[column].max()
    edgecolor = 'black'
    linewidth = 0.1
    cmap = 'OrRd'

    def plot(gdf, ax, title="", legend=True):
        gdf.plot(ax=ax,
                 column=column,
                 edgecolor=edgecolor,
                 linewidth=linewidth,
                 legend=legend,
                 cmap=cmap,
                 vmin=vmin, vmax=vmax)
        ax.set_aspect(1.63)
        if title:
            ax.set_title(title, size=14)
        ax.axis('off')
    fig = plt.gcf()
    if not subplot_spec:
        subplot_spec = gridspec.GridSpec(1, 1)[0]
    if separate_london:
        if london_layout == 'horizontal':
            gs = gridspec.GridSpecFromSubplotSpec(
                nrows=1, ncols=2, width_ratios=[1, 2], subplot_spec=subplot_spec)
            ldn_ax = fig.add_subplot(gs[0, 0])
            roe_ax = fig.add_subplot(gs[0, 1])
        else:
            gs = gridspec.GridSpecFromSubplotSpec(
                nrows=2, ncols=1, height_ratios=[2, 1], subplot_spec=subplot_spec)
            roe_ax = fig.add_subplot(gs[0, 0])
            ldn_ax = fig.add_subplot(gs[1, 0])

        plot(gdf_roe,
             roe_ax,
             title="England (excluding London):\n{}".format(title),
             legend=show_legend)
        plot(gdf_london,
             ldn_ax,
             title="London:\n{}".format(title),
             legend=False)
    else:
        ax = plt.subplot(subplot_spec)
        plot(gdf,
             ax,
             title=title,
             legend=show_legend)
    return plt
