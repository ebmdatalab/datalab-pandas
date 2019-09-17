import geopandas as gpd
import pandas as pd
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import datetime

plt.ioff()

class MapLoader():
    """ Map Loader for loading in python df and creating maps

    """

    def __init__(self, description=None, author="EBM DataLab", *args, **kwargs):
        """Map Loader is initiated with description and author for clarity

            Args:
                description (str): Description at a broad level of the dataset
                author (str): Author - set as EBM Datalab if left blank

        """

        self.description = description
        self.author = author

        self.date = datetime.datetime.now()
        """Datetime (obj): Automatically records datetime as time class is initiated"""

        self.plots = {}
        """dict: initally blank to allow plots to be saved"""

    def load_data(self, data, mapping_data_path, index_file_path=None):
        """
        Loads data from a pandas dataframe and combines with a mapping json file

        :param data: pd.dataframe file
        :param mapping_data_path (str): the path of the json file
        :param index_file_path (str): path of the index file. Index file contains additionally information
                about the geographical areas such as London False/True

        :return: self.final_df
        """

        self.map_data = gpd.read_file(mapping_data_path)
        if index_file_path == None:
            final = gpd.GeoDataFrame(
                pd.merge(left=data, right=self.map_data, how='inner', left_on='row_id', right_on='code'))
            self.final_df = final
        else:
            self.index_file = pd.read_csv(index_file_path)
            interim = gpd.GeoDataFrame(
                pd.merge(left=data, right=self.index_file, how='inner', left_on='row_id', right_on='code',
                         left_index=True))
            final = gpd.GeoDataFrame(
                pd.merge(left=interim, right=self.map_data, how='inner', left_on='row_id', right_on='code'))
            self.final_df = final

    def create_map(self, plot_value, title, description=None,
                   london_separate=True,
                   size=(12, 10),
                   cmap="OrRd",
                   legend=True, fit_legend=False,
                   edgecolor="black", linewidth=0.1, save=False):
        """

        :param plot_value (str): points to which column in the dataframe for plotting
        :param title (str): title of the plots
        :param description (str): description of the plots
        :param london_separate (bool): True or False
        :param size (2 item tuple): size of the plot
        :param cmap (str): colors - standard use is OrRd
        :param legend (bool): True or False
        :param fit_legend (bool): True or False. Scales the legend to the size of the map
        :param edgecolor (str): Set to black
        :param linewidth (float): Width of the line around geographical areas
        :param save (bool): True or False. If True, saves in self.plots as a dictionary with description as key, plot as value
        :return: Figure
        """

        subplot_spec = gridspec.GridSpec(1, 1)[0]
        if london_separate == True:
            lon_data = self.final_df[self.final_df["is_london"] == True]
            roe_data = self.final_df[self.final_df["is_london"] == False]
            gs = gridspec.GridSpecFromSubplotSpec(nrows=1, ncols=2, width_ratios=[1, 2], subplot_spec=subplot_spec)
            fig = plt.figure(figsize=size)
            ldn_ax = fig.add_subplot(gs[0, 0])
            ldn_ax.axis("off")
            ldn_ax.set_title("London:\n{}".format(title), size=14)
            roe_ax = fig.add_subplot(gs[0, 1])
            if fit_legend == True:
                divider = make_axes_locatable(roe_ax)
                cax = divider.append_axes("right", size="5%", pad=0.1)
            else:
                cax = None
            roe_ax.axis("off")
            roe_ax.set_title("England (excluding London):\n{}".format(title))
            roe_data.plot(column=plot_value, legend=legend, ax=roe_ax, cmap=cmap, cax=cax, edgecolor=edgecolor,
                          linewidth=linewidth)
            lon_data.plot(column=plot_value, legend=False, ax=ldn_ax, cmap=cmap, edgecolor=edgecolor,
                          linewidth=linewidth)
            if save == True:
                self.plots[description] = fig
            plt.close()
            return fig
        elif london_separate == False:
            dt = self.final_df
            fig = plt.figure(figsize=size)
            uk_ax = fig.add_subplot(111)
            uk_ax.axis("off")
            uk_ax.set_title("UK:\n{}".format(title), size=14)
            if fit_legend == True:
                divider = make_axes_locatable(uk_ax)
                cax = divider.append_axes("right", size="5%", pad=0.1)
            else:
                cax = None
            dt.plot(column=plot_value, legend=legend, ax=uk_ax, cmap=cmap, cax=cax, edgecolor=edgecolor,
                    linewidth=linewidth)
            if save == True:
                self.plots[description] = fig
            return fig
        else:
            pass

