## PyFloraPots

Never know when to water your plant?

Thanks to the use of IoT and PyFloraPots app, you can now monitor the soil parameters in all of your pots and make sure your plants grow in optimal conditions.

# Usage
***PyFloraPots consists of the main program, which contains the GUI code (PyFloraPots.py) that is linked to modules handling database reading, saving and updating, data acquisition, generation and other.***

The GUI consists of two windows - first the Login, where the username and password are authenticated, and the second, where it is possible to use
all program functionalities.
The navigation bar on the left contains a list of sub-windows:
    - Pots
    - Plants
    - Measurements
    - My profile
    - Exit
<p align="center">
	<img src="https://github.com/LovelK7/PyFloraPots/blob/main/screenshots/01_257043342-bf500ddc-faca-4c05-8040-7268d670b5f1.png?raw=true" width="50%">
</p>


# POTS
***All pot information (location, plant name, plant picture and status) are shown in the boxes for all pots.***

The toolbar in the upper part allows:
    - adding a new pot or
    - status update (SYNC).
The toolbar in the upper right corner contains the current date and time values and the outside air temperature at the chosen weather station.

<p align="center">
	<img src="https://github.com/LovelK7/PyFloraPots/blob/main/screenshots/02_257042939-c5d5de31-8ad6-4b8f-9a0d-10c0cffb841c.png?raw=true" width="75%">
</p>

Clicking on any pot (image) opens a separate window for viewing the status and changing the pots's data.
In the left part is enabled to change:
    - location,
    - name, and
    - photo of the plant
Available optins are:
    - accept,
    - cancel,
    - empty the pot, and
    - delete the pot.
The right part shows the status of the plant (data and text) and continuous measurement graphs.
The Sync button refreshes the display of the value and status of the plant in the pot.

<p align="center">
	<img src="https://github.com/LovelK7/PyFloraPots/blob/main/screenshots/03_257043109-12789575-1faf-4123-b198-9e26126d380d.png?raw=true" width="75%">
</p>

# PLANTS
***Here is a list of available plants for planting (name and photo of the plant).*** 

A new plant can be added by clicking on "Add new plant" in the upper right corner, which opens a window for defining the name and path to the photo.
Clicking on any picture of a plant opens a window for changing the name or photo of the plant and option to delete the plant.
- Note that by deleting a plant already planted in a certain pot, the pot in which the plant was planted is emptied
- All plant photos are stored in "foto" directory

<p align="center">
	<img src="https://github.com/LovelK7/PyFloraPots/blob/main/screenshots/04_257043142-005de48c-3039-4e9f-8425-b4ce5f7de87c.png?raw=true" width="75%">
</p>
<p align="center">
	<img src="https://github.com/LovelK7/PyFloraPots/blob/main/screenshots/05_257043183-6d61e865-5e71-42e3-83d4-53a71b12cbce.png?raw=true" width="50%">
</p>

# MEASUREMENTS
***The program enables continuous monitoring and recording of sensor values (generated data).*** 

Data is recorded for all available containers and stored in CSV files for each pot. By default the CSV files are stored in the main directory.
Toolbar:
    - Reset - files are emptied and generated anew
    - Set interval - it is possible to set the measurement interval in seconds
    - Start - measurement of values from the sensor and saving to files is started
    - Stop - stops saving to files
    - Reload the graphs - the display is refreshed and the values from the files are read again
	
<p align="center">
	<img src="https://github.com/LovelK7/PyFloraPots/blob/main/screenshots/06_257043234-e2bbf629-5e2a-4ac8-b7f1-96df34ede9f5.png?raw=true" width="75%">
</p>

# MY PROFILE
***Here are stored all user data***.

It is possible to change user data:
    - Name
    - Surname
    - Username
    - Password, and
    - Weather station
	
<p align="center">
	<img src="https://github.com/LovelK7/PyFloraPots/blob/main/screenshots/07_257043281-985c14c0-8a39-402e-8f63-7eed51c24ac6.png?raw=true" width="40%">
</p>

# EXIT
Exit the program.

## MODULES
***The program works with the help of several modules, each with a separate function***

# database.py
This is where storage, reading, changing, updating and other activities for the "baza_pot-plant.db" database are performed.
The database consists of 3 tables:
    - Plants
    - PyPots
    - Status
Plants contains all information about plants (id, name, path to the photo), PyPots about containers (location and link to the id of the planted plant), and
Status of sensor parameter values (volumetric water content (vwc), ph, salinity and lux) for each vessel (connected via vessel id)
Relations:
    - each pot has one plant
    - one type of plant can be planted in several pots
    - one pot has one status
The status (textual form, for GUI) is generated depending on the values pulled from the sensors.py module.

# sensors.py
This module is used to generate sensor values either through Sync in the GUI or to generate continuous values through Measurements.
Sensor values are generated randomly, while continuous measurements take random walk values from the initial random value.

# file_manager.py
This module is used for storing and reading from files, i.e. storing and reading values from CSV files that contain continuous values
measurements from sensors.

# measurements.py
This module is used for reading data from files and importing it in the form of Pandas DataFrame.

# plots.py
This module reads data from measurements.py (Pandas DataFrame) and generates 4 graphs for each sensor value of a particular selected pot.

# meteo.py
This module is a webscrape program for retrieving outdoor air temperature values from the official Croatian meteorological institution website.

# user.py
Using this module, it is possible to change user data.
