import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from abc import ABC, abstractmethod

import logging
logger = logging.getLogger(__name__)

class IVisualizationHandler(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def visualize_data(self, data):
        pass

class VisualizationHandler(IVisualizationHandler):
    def __init__(self):
        pass

    def visualize_data(self, df: pd.DataFrame):
        """
        Visualize the weather data with matplotlib. 
        Shows two subplots.
        Top figure: Precipitation and Precipitation Probability.
        Bottom figure: Wind speed at 10m above ground.
        """
        logging.info("visualize_data()")

        # stop if dataframe is empty        
        if df.empty:
            logger.warning("cannot plot empty dataframe.")
            exit(0)
        
        # Setup plotting colors
        ax1_color = "lightblue" # precipitation probability
        ax2_color = "darkblue"  # precipitation
        ax3_color = "orange"    # wind speed

        # setup plotting area with two subplots
        fig, ax = plt.subplots(2, 1, figsize=(8,6))
        # setup second pair of axis for the top figure.
        ax0_twin = ax[0].twinx()

        # setup concise date formatter for x-axis. (This is done before plotting.)
        locator = mdates.AutoDateLocator(minticks=3, maxticks=9)
        formatter = mdates.ConciseDateFormatter(locator)    
        ax[0].xaxis.set_major_locator(locator)
        ax[0].xaxis.set_major_formatter(formatter)
        ax[1].xaxis.set_major_locator(locator)
        ax[1].xaxis.set_major_formatter(formatter)

        # plot the three data series
        df["precipitation_probability"].plot(ax=ax[0], color = ax1_color, 
                                             label="Precipitation Probability", rot=0)
        df["precipitation"].plot(ax=ax0_twin, color = ax2_color, 
                                 label="Precipitation", rot=0)
        df["wind_speed_10m"].plot(ax=ax[1], color=ax3_color, 
                                  label="Wind Speed", rot=0)

        # setup x-axis limits
        time = df.index.values
        ax[0].set_xlim((time[0], time[-1]))
        ax[1].set_xlim((time[0], time[-1]))

        # setup y-axis limits
        ax[0].set_ylim(ymin=0)
        ax0_twin.set_ylim(ymin=0)
        ax[1].set_ylim(ymin=0)

        # setup y-axes labels
        ax[0].set_ylabel("Precipitation Probability(%)")
        ax0_twin.set_ylabel("Precipitation(in)")
        ax[1].set_ylabel("Wind Speed(mph)")

        # setup misc plot settings and show the plots
        fig.legend(loc="center right")        
        fig.tight_layout()
        plt.show()
