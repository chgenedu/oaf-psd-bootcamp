# oaf-psd-bootcamp
Repository for the Open Avenues: Professional Software Development Bootcamp

# project_weather_app
This project directory contains an application for downloading and displaying weather data for a given location.
## Motivation
This application provides forecasted weather condition information (such as rainfall information and wind speed) for planners of outdoor events. Event planners of outdoor events need to be aware of the weather condition of their venue. Downpours or storms may lead to the need to cancellation of events. This application downloads the weather information for a given location from an online API of a weather service. 

The program will plot the seven-day forecasted weather data, for the precipitation probability, the precipitation (rain + showers + snow), and the wind speed at 10 meters above ground.

## Summary of approach
The following are basic steps taken in creating a plot of the forecasted weather condition of a specified location.
1. Obtain the coordinate of a given location (specified by longitude and latitude)
2. Retrieves the weather information for that location from the database.
3. If the required weather information of that location is not in the database, then download that data from a weather API and store it in the database.
4. Display the weather data in a plot.

## My approach in details. / Implementation details
The weather service API information (such as the URL and the kinds of information to download) is specified in the file config/config.json. The data this program retrieves is the hourly forecasted weather projection for the next seven days. The retrieved data includes:
* time
* precipitation probability (in %)
* precipitation (in inches)
* wind speed at 10 meters above ground (in mph)
  
Weather data is retrieved via an the open-meteo.com API. ([Documentation for the open-meteo.com API](https://open-meteo.com/en/docs))

The location (specified by longitude and latitude) is specified in main.py. Currently, the location is set to LONGITUDE = 13.41, LATITUDE = 52.52, which is the default location for the example web app on the open-meteo documentation page. For future improvement, this can be specified in the command line. 

The program will lookup the weather data for the specified location in an sqlite3 database for previously retrieved data. 

If the requested data is not in the database or if the database does not exist, the program will download the requested data with the remote server API and store the data in the local sqlite3 database. (A database will be created if it does not exist.) 

The data will then sent to a visualization program. The matplotlib library is used to display the weather data. There are two subplots. The top plot is the precipitation probability and the precipitation. The bottom plot is the wind speed at 10 meters above ground. 

A mocked data service is also created for this program. This mocked service uses randomly generated numbers for weather data. 

## How to run the program
To run the program by the command line, go to the project_weather_app directory and type the following.

| Command | Description |
|-----|-----|
| `python main.py` | This will run the program in the basic mode. |
| `python main.py -h` | This will display the help information. |
| `python main.py --mode API` | This will use the data from an online weather API service. |
| `python main.py --mode MOCK` | This will use a randomly generated dataset. |
| `python main.py --reset --mode API` | This will clear the database and force the program to download new data from the remote weather API. |
| `python main.py --reset --mode MOCK` | This will clear the database and force the program to generate a new set of random data for the mocked service. |

## Example output file
Here is an example screenshot of the output plot.
![Weather App Plot Screenshot](https://github.com/chgenedu/oaf-psd-bootcamp/blob/43072e393388cf1dbd6534a848960e616f7ba068/images/plot_example_screenshot.jpg)

## What I learned
In this project, I learned some software engineering principles and techniques: 
* decouple components
* dependency injection  
* factory design pattern

Additionally, I learned to use some useful python modules. They include the following:
* logging
* argparse
* sqlite3
* matplotlib

Finally, I learned more about how to use the following tools:
* git / GitHub
* Visual Studio Code

## Future directions
Here are some directions for further development of this project.
* More command line arguments to specify the following:
  * The location (longitude and latitude)
  * The logging level
  * The forecasting period 
* Improve data downloading
  * Download only the data for the time period that is not in the database. (Currently, if there is any data for a specific location, the program will use the existing data, regardless of time.)
* Testing: unit testing, System testing.
* Use Continuous development methodology
* Improve visualization.
  * mark the time period on the plot for which there the precipitation probability is higher than a threshold value.
* Deployment to the web, perhaps with [streamlit](https://streamlit.io/).


