import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path


def ccg_map(df, title="", column=None, separate_london=True):
    """Draw a CCG map with London separated out
    """
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

    ccgs = gpd.read_file(data_dir / 'ccgs.json').set_index('name')

    # remove ones without geometry - these are federations rather than individual CCGs
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

    if separate_london:
        fig = plt.figure(figsize=(12, 12))
        gs = gridspec.GridSpec(
            ncols=2, nrows=2, figure=fig, height_ratios=[3, 1])
        roe_ax = fig.add_subplot(gs[0, 0])
        ldn_ax = fig.add_subplot(gs[1, 0])

        plot(gdf_roe, roe_ax, title="England (excluding London):\n{}".format(title))
        plot(gdf_london, ldn_ax, title="London:\n{}".format(title), legend=False)
    else:
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(1, 1, 1)
        plot(gdf, ax, title=title)
    return plt
