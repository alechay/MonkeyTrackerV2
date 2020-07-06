# MonkeyTrackerV2
 
## Objective

To generate a user-friendly primate weight tracker for my daily research log. The tracker is designed to record the daily water intake and weight for each individual primate. Graphs are then generated to visualize water consumption and weight trends over time.

## Purpose

In our research, it is extremely important to monitor the general well-being of our primates while they are performing tasks over long periods of time. We use water, food, and fruit in a controlled setting as motivation for them to learn and perform adequately on visual and physical tasks. A primate's weight is closely related to their intake of these rewards and a fine balance must be established between water/food intake and weight control. 

We cannot allow any primate to fall below a designated weight threshold, as it may be indicative of dehydration, fatigue, or illness, so a detailed daily log of this information must be kept. In our lab, we only have physical records of these logs, which are wasteful and limited in their capabilities. The purpose of this project is to digitize this process, allowing us to expand our ability to assess individual primates' trends through graphing and to create a more modernized method of saving, storing, and analyzing these key data sets.

## Repository Contents

1. aero.csv
2. gui.py

## How to use

*Prerequisite: Have a .csv file for your individual primate. The code works by reading and updating this .csv file*

### Launching the app

1. Launch the main menu in terminal using
`python gui.py`
2. Select a button to enter, view, or visualize the data
<br>
<img src="https://github.com/alechay/MonkeyTrackerV2/blob/master/pics/main_menu.png" width=50% height=50% />

### Enter data

Enter data for the current day
<br>
<img src="https://github.com/alechay/MonkeyTrackerV2/blob/master/pics/enter_data.png" width=50% height=50% />

### Enter missing data

Enter data for any missing days
<br>
<img src="https://github.com/alechay/MonkeyTrackerV2/blob/master/pics/enter_missing_data" width=50% height=50% />

### View table

View the data that is in your .csv file
<br>
<img src="https://github.com/alechay/MonkeyTrackerV2/blob/master/pics/view_table" width=50% height=50% />

### Trends in water and weight

View subplots showing trends in water and weight
<br>
<img src="https://github.com/alechay/MonkeyTrackerV2/blob/master/pics/daily_water_weight.png" width=50% height=50% />

### Trends in weight

View a plot showing trends in weight, with the size of the dot corresponding to the amount of water receieved
<br>
<img src="https://github.com/alechay/MonkeyTrackerV2/blob/master/pics/daily_weight" width=50% height=50% />

### Daily changes

View a plot showing the daily change in weight as a result of the amount of water given (and whether fruit was given)
<br>
<img src="https://github.com/alechay/MonkeyTrackerV2/blob/master/pics/daily_change.png" width=50% height=50% />

### Info and specs
Gives the equations for the best fit lines drawn in the daily change scatterplot. Calculates the ideal amount of water that needs to be given to your primate so that it maintains its weight.
<br>
<img src="https://github.com/alechay/MonkeyTrackerV2/blob/master/pics/info_specs.png" width=50% height=50% />

## Bugs
Tested on macOS Mojave, version 10.14.6. No known bugs at this time.

## Dependencies
* Python version 3.7.6
* PyQt5
* Datetime
* os
* Matplotlib
* Pandas
* Numpy

## References
* Python, PyQt5, Matplotlib, Pandas, Numpy Documentation
* Plus a lot of stack overflow
