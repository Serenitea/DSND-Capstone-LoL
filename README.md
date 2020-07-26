# DSND-Capstone-LoL


### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

There should be no necessary libraries to run the code here beyond the Anaconda distribution of Python.  The code should run with no issues using Python versions 3.*.

## Project Motivation<a name="motivation"></a>

This project aims to provide insight on the relative importance of neutral objectives throughout the course of the MOBA game League of Legends, ultimately helping players make optimal in-game decisions. Although there are some predictive models for League, such as using champion selection and professional players to predict outcome, I have not found one focused on the importance of objectives nor one that is up-to-date with the latest objective changes for the current season.

The anaylzed match data was extracted via the Riot Games API and contains over 20,000 NA high elo solo/duo ranked matches from masters, Grandmasters, and Challenger tier players in the North American server from patch 10.11.

## File Descriptions <a name="files"></a>

I compiled all of my steps into one notebook along with an HTML version.  Markdown cells were used to assist in walking through the thought process for individual steps.

src folder - Almost all functions used in the notebook are stored in the 'data_preprocessing.py' and 'visuals.py' files located in this folder

Data folder - most of the original survey data and processed data are saved here. There are three files that were too large to be uploaded: the 2018 and 2019 survey results, and the preprocessed 2019 survey results. The survey results are publicly available at the links below.


## Results<a name="results"></a>
[Github](https://github.com/Serenitea/DSND-Capstone-LoL)
The main findings of the code can be found at the post available [here](https://medium.com/@themaryzhou/is-that-dragon-soul-worth-it-a85789f55c2f).

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

Credits to Riot Games for the data through the [Riot API](https://developer.riotgames.com/apis). Thanks to the [riotwatcher wrapper API](https://riot-watcher.readthedocs.io/en/) for facilitating data extraction.
