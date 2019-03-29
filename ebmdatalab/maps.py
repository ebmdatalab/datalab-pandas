import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path


def ccg_map(df, title="", column=None, separate_london=False, cartogram=False,
            subplot_spec=None):
    """Draw a CCG map with London separated out
    """
    # Because this uses subplots to arrange London and England,
    # the only way to arrange nested subplots is via a subplotspec
    assert column, "You must specify a column name to plot"
    df = df.copy()
    # input df must have 'pct' column, plus others as specified
    data_dir = Path(__file__).parent / 'data'
    names = pd.read_csv(data_dir / 'ccg_for_map.csv')
    # Add names and if it's london
    df = df.merge(names[['code', 'name', 'is_london']], left_on="pct", right_on="code")
    # Normalise names so they match ccgs file
    df['name'] = df['name'].str.upper()
    df['name'] = df["name"].str.replace("&","AND")
    df = df.set_index('name')

    if cartogram:
        ccgs = gpd.read_file(data_dir / 'ccgs_cartogram.json')
    else:
        ccgs = gpd.read_file(data_dir / 'ccgs.json')

    # Normalise because the two GeoJSON files have a different format
    ccgs['name'] = ccgs['name'].str.upper()
    ccgs = ccgs.set_index('name')

    # remove ones without geometry - these are federations rather than
    # individual CCGs
    ccgs = ccgs[~ccgs['geometry'].isnull()]
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
        gs = gridspec.GridSpecFromSubplotSpec(
            nrows=2, ncols=1, height_ratios=[3, 1], subplot_spec=subplot_spec)
        roe_ax = fig.add_subplot(gs[0, 0])
        ldn_ax = fig.add_subplot(gs[1, 0])

        plot(gdf_roe, roe_ax, title="England (excluding London):\n{}".format(title))
        plot(gdf_london, ldn_ax, title="London:\n{}".format(title), legend=False)
    else:
        ax = plt.subplot(subplot_spec)
        plot(gdf, ax, title=title)
    return plt
